#!/usr/bin/env python3
"""Collect conservative, machine-readable testing evidence from a repository.

This helper intentionally reports signals rather than maturity judgments or
recommendations. It uses only the Python standard library and treats missing
manifests, runners, Git history, and optional tools as normal conditions.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Optional

SCHEMA_VERSION = 1
MAX_TEXT_BYTES = 512_000
DEFAULT_MAX_FILES = 50_000
DEFAULT_SAMPLE_SIZE = 12

# These directories are dependency trees, generated output, caches, or vendored
# code. Keeping this list conservative makes the helper useful in mixed repos
# without requiring a project-specific ignore file.
IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".bzr",
    "node_modules",
    "bower_components",
    ".pnpm-store",
    ".yarn",
    ".venv",
    "venv",
    "env",
    ".env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".nox",
    ".gradle",
    ".idea",
    ".vscode",
    "target",
    "build",
    "dist",
    "out",
    "coverage",
    "htmlcov",
    ".nyc_output",
    ".next",
    ".nuxt",
    ".turbo",
    ".parcel-cache",
    "vendor",
    "generated",
    "gen",
    "obj",
    "bin",
    "Pods",
}

MANIFEST_NAMES = {
    "package.json",
    "pyproject.toml",
    "pytest.ini",
    "tox.ini",
    "setup.cfg",
    "setup.py",
    "requirements.txt",
    "requirements-dev.txt",
    "Pipfile",
    "Directory.Packages.props",
    "go.mod",
    "go.work",
    "Cargo.toml",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "settings.gradle",
    "settings.gradle.kts",
    "Directory.Build.props",
    "Directory.Build.targets",
    "composer.json",
    "Gemfile",
    "Package.swift",
    "Makefile",
    "Taskfile.yml",
    "Taskfile.yaml",
}

LOCKFILE_NAMES = {
    "package-lock.json": "npm",
    "npm-shrinkwrap.json": "npm",
    "yarn.lock": "yarn",
    "pnpm-lock.yaml": "pnpm",
    "bun.lock": "bun",
    "bun.lockb": "bun",
    "poetry.lock": "Poetry",
    "uv.lock": "uv",
    "Pipfile.lock": "Pipenv",
    "go.sum": "Go modules",
    "Cargo.lock": "Cargo",
    "Gemfile.lock": "Bundler",
    "composer.lock": "Composer",
}

CI_FILE_NAMES = {
    ".gitlab-ci.yml",
    ".gitlab-ci.yaml",
    "Jenkinsfile",
    "azure-pipelines.yml",
    "azure-pipelines.yaml",
    ".circleci/config.yml",
    ".circleci/config.yaml",
    "bitbucket-pipelines.yml",
    "bitbucket-pipelines.yaml",
    "appveyor.yml",
    "appveyor.yaml",
}

INSTRUCTION_NAMES = {
    "AGENTS.md",
    "CONTRIBUTING.md",
    "CONTRIBUTING.rst",
    "DEVELOPMENT.md",
    "DEVELOPING.md",
    "README.md",
}

CONFIG_PREFIXES = (
    "jest.config",
    "vitest.config",
    "mocha.config",
    "playwright.config",
    "cypress.config",
    "karma.conf",
    "pytest",
    "tox",
    "noxfile",
    "coverage",
    ".nycrc",
    "babel.config",
    "webpack.config",
    "vite.config",
)

REPORT_DIR_NAMES = {"coverage", "htmlcov", ".nyc_output"}

SOURCE_EXTENSIONS = {
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".css",
    ".fs",
    ".fsx",
    ".go",
    ".graphql",
    ".h",
    ".hpp",
    ".html",
    ".java",
    ".js",
    ".jsx",
    ".json",
    ".kt",
    ".kts",
    ".mjs",
    ".php",
    ".py",
    ".rb",
    ".rs",
    ".scss",
    ".sh",
    ".sql",
    ".swift",
    ".ts",
    ".tsx",
    ".vue",
}

CI_COMMAND_RE = re.compile(
    r"(?:"
    r"(?:npm|pnpm|yarn|bun)\s+(?:run\s+)?[A-Za-z0-9_:.@/-]*test[A-Za-z0-9_:.@/-]*(?:\s+[^|;&]+)?"
    r"|(?:python(?:3)?\s+-m\s+)?pytest(?:\s+[^|;&]+)?"
    r"|go\s+test(?:\s+[^|;&]+)?"
    r"|cargo\s+test(?:\s+[^|;&]+)?"
    r"|(?:mvn|gradle|\.\/gradlew)\s+(?:[^|;&]*\s+)?test(?:\s+[^|;&]+)?"
    r"|dotnet\s+test(?:\s+[^|;&]+)?"
    r"|(?:bundle\s+exec\s+)?(?:rspec|rake\s+test)(?:\s+[^|;&]+)?"
    r"|(?:vendor/bin/)?phpunit(?:\s+[^|;&]+)?"
    r"|(?:npx\s+)?(?:jest|vitest|mocha|playwright\s+test|cypress\s+run)(?:\s+[^|;&]+)?"
    r")",
    re.IGNORECASE,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect repository testing evidence as JSON. No recommendations are made."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="repository root to inspect (default: current directory)",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=DEFAULT_MAX_FILES,
        help=f"maximum files to scan (default: {DEFAULT_MAX_FILES})",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=DEFAULT_SAMPLE_SIZE,
        help=f"maximum representative test samples (default: {DEFAULT_SAMPLE_SIZE})",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="pretty-print JSON instead of emitting one compact line",
    )
    return parser.parse_args()


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def read_text(path: Path, errors: list[str]) -> str:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            return handle.read(MAX_TEXT_BYTES)
    except (OSError, UnicodeError) as exc:
        errors.append(f"could not read {path}: {exc}")
        return ""


def walk_files(
    root: Path, max_files: int, errors: list[str]
) -> tuple[list[Path], bool, list[Path]]:
    files: list[Path] = []
    skipped_reports: list[Path] = []
    truncated = False

    def record_walk_error(exc: OSError) -> None:
        errors.append(f"could not inspect {exc.filename or root}: {exc}")

    for current, dirs, names in os.walk(
        root, topdown=True, followlinks=False, onerror=record_walk_error
    ):
        kept_dirs: list[str] = []
        for name in sorted(dirs):
            if name.lower() in REPORT_DIR_NAMES:
                skipped_reports.append(Path(current) / name)
            elif name not in IGNORED_DIRS and name not in {".git"}:
                kept_dirs.append(name)
        dirs[:] = kept_dirs
        for name in sorted(names):
            path = Path(current) / name
            if path.is_symlink():
                continue
            files.append(path)
            if len(files) >= max_files:
                truncated = True
                return files, truncated, skipped_reports
    return files, truncated, skipped_reports


def is_test_file(path: Path) -> bool:
    name = path.name.lower()
    if path.suffix.lower() not in SOURCE_EXTENSIONS:
        return False
    parts = {part.lower() for part in path.parts}
    if any(part in {"tests", "test", "spec", "__tests__", "integration", "e2e", "acceptance"} for part in parts):
        return True
    if re.search(r"(^test[_-]|[_-]test\.|\.test\.|\.spec\.|_test\.)", name):
        return True
    if name.startswith("test") and path.suffix.lower() in SOURCE_EXTENSIONS:
        return True
    return False


def test_kind(path: Path) -> str:
    lowered = "/".join(part.lower() for part in path.parts)
    if any(token in lowered for token in ("e2e", "browser", "playwright", "cypress")):
        return "e2e"
    if any(token in lowered for token in ("integration", "acceptance", "contract")):
        return "integration"
    if "unit" in lowered:
        return "unit"
    return "other"


def is_config_path(path: Path) -> bool:
    name = path.name.lower()
    if path.name in MANIFEST_NAMES or path.name in LOCKFILE_NAMES or path.name in CI_FILE_NAMES:
        return True
    if (name.startswith("requirements") and name.endswith(".txt")) or path.suffix.lower() in {".csproj", ".fsproj", ".sln"}:
        return True
    if name.startswith(CONFIG_PREFIXES):
        return True
    if name in {".nycrc", ".nycrc.json", ".coveragerc", "coverage.yml", "coverage.yaml"}:
        return True
    return False


def is_ci_path(path: Path) -> bool:
    name = path.name
    lowered = path.as_posix().lower()
    return (
        name in CI_FILE_NAMES
        or ".github/workflows/" in lowered
        or ".buildkite/" in lowered
        or ".github/actions/" in lowered
        or ".circleci/" in lowered
        or name.startswith(".travis.")
    )


def json_object(path: Path, text: str) -> Optional[dict[str, Any]]:
    if path.name != "package.json":
        return None
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def command_for_script(manager: str, name: str) -> str:
    if name == "test":
        return f"{manager} test"
    if manager == "npm":
        return f"npm run {name}"
    return f"{manager} run {name}"


def add_command(commands: list[dict[str, str]], command: str, source: str) -> None:
    normalized = " ".join(command.strip().split())
    if not normalized:
        return
    if not any(item["command"] == normalized and item["source"] == source for item in commands):
        commands.append({"command": normalized, "source": source})


def detect_languages(paths: Iterable[Path]) -> tuple[list[str], list[str]]:
    extensions = {path.suffix.lower() for path in paths}
    names = {path.name for path in paths}
    languages: list[str] = []
    ecosystems: list[str] = []
    if ".js" in extensions or ".jsx" in extensions or ".mjs" in extensions or ".cjs" in extensions or "package.json" in names:
        languages.append("JavaScript")
        ecosystems.append("JavaScript/TypeScript")
    if ".ts" in extensions or ".tsx" in extensions:
        languages.append("TypeScript")
        if "JavaScript/TypeScript" not in ecosystems:
            ecosystems.append("JavaScript/TypeScript")
    if "package.json" in names or any(name in names for name in ("package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lock", "bun.lockb")):
        ecosystems.append("Node.js")
    if ".py" in extensions or any(name in names for name in ("pyproject.toml", "pytest.ini", "setup.py", "setup.cfg")):
        languages.append("Python")
        ecosystems.append("Python")
    if ".go" in extensions or "go.mod" in names or "go.work" in names:
        languages.append("Go")
        ecosystems.append("Go")
    if ".java" in extensions or ".kt" in extensions or ".kts" in extensions or any(name in names for name in ("pom.xml", "build.gradle", "build.gradle.kts")):
        if ".java" in extensions:
            languages.append("Java")
        if ".kt" in extensions or ".kts" in extensions:
            languages.append("Kotlin")
        ecosystems.append("Java/Kotlin")
    if ".cs" in extensions or ".fs" in extensions or any(path.suffix.lower() in {".sln", ".csproj", ".fsproj"} for path in paths):
        languages.append("C#/.NET")
        ecosystems.append(".NET")
    if ".rs" in extensions or "Cargo.toml" in names:
        languages.append("Rust")
        ecosystems.append("Rust")
    if ".rb" in extensions or "Gemfile" in names:
        languages.append("Ruby")
        ecosystems.append("Ruby")
    if ".php" in extensions or "composer.json" in names:
        languages.append("PHP")
        ecosystems.append("PHP")
    if ".swift" in extensions or "Package.swift" in names:
        languages.append("Swift")
        ecosystems.append("Swift")
    return sorted(set(languages)), sorted(set(ecosystems))


def detect_package_managers(paths: Iterable[Path]) -> list[str]:
    managers: set[str] = set()
    names = {path.name for path in paths}
    for name, manager in LOCKFILE_NAMES.items():
        if name in names:
            managers.add(manager)
    if "package.json" in names and not managers.intersection({"npm", "yarn", "pnpm", "bun"}):
        managers.add("npm")
    if "pyproject.toml" in names or "requirements.txt" in names or "setup.py" in names:
        managers.add("Python packaging")
    if "go.mod" in names or "go.work" in names:
        managers.add("Go modules")
    if "Cargo.toml" in names:
        managers.add("Cargo")
    if "pom.xml" in names:
        managers.add("Maven")
    if any(name in names for name in ("build.gradle", "build.gradle.kts")):
        managers.add("Gradle")
    if any(path.suffix.lower() in {".sln", ".csproj", ".fsproj"} for path in paths):
        managers.add(".NET CLI")
    if "Gemfile" in names:
        managers.add("Bundler")
    if "composer.json" in names:
        managers.add("Composer")
    if "Package.swift" in names:
        managers.add("Swift Package Manager")
    return sorted(managers)


def detect_build_systems(paths: list[Path], contents: dict[str, str]) -> list[str]:
    names = {path.name for path in paths}
    systems: set[str] = set()
    if "package.json" in names:
        systems.add("package scripts")
    if "Makefile" in names:
        systems.add("Make")
    if "Taskfile.yml" in names or "Taskfile.yaml" in names:
        systems.add("Task")
    if "pyproject.toml" in names or "setup.py" in names:
        systems.add("Python packaging")
    if "go.mod" in names or "go.work" in names:
        systems.add("Go modules")
    if "Cargo.toml" in names:
        systems.add("Cargo")
    if "pom.xml" in names:
        systems.add("Maven")
    if "build.gradle" in names or "build.gradle.kts" in names:
        systems.add("Gradle")
    if any(path.suffix.lower() in {".sln", ".csproj", ".fsproj"} for path in paths):
        systems.add(".NET")
    if "Package.swift" in names:
        systems.add("Swift Package Manager")
    # These are configuration signals, not claims that a build was executed.
    combined = "\n".join(contents.values()).lower()
    for token, label in (("vite", "Vite"), ("webpack", "Webpack"), ("rollup", "Rollup"), ("esbuild", "esbuild")):
        if token in combined:
            systems.add(label)
    return sorted(systems)


def detect_workspaces(paths: list[Path], contents: dict[str, str], package_data: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    signals: list[dict[str, str]] = []
    for path in paths:
        rel = path.as_posix()
        text = contents.get(rel, "")
        if path.name == "pnpm-workspace.yaml":
            signals.append({"path": rel, "type": "pnpm workspace"})
        elif path.name == "go.work":
            signals.append({"path": rel, "type": "Go workspace"})
        elif path.name == "Cargo.toml" and re.search(r"(?m)^\s*\[workspace\]", text):
            signals.append({"path": rel, "type": "Cargo workspace"})
        elif path.name in {"settings.gradle", "settings.gradle.kts"} and re.search(r"(?m)^\s*include", text):
            signals.append({"path": rel, "type": "Gradle multi-project"})
    for rel, data in package_data.items():
        if "workspaces" in data:
            signals.append({"path": rel, "type": "package.json workspaces"})
    return sorted(signals, key=lambda item: (item["path"], item["type"]))


def detect_test_configs(paths: list[Path]) -> list[str]:
    result = []
    for path in paths:
        name = path.name.lower()
        if (
            name.startswith(CONFIG_PREFIXES)
            or name in {".coveragerc", "coverage.yml", "coverage.yaml", ".nycrc", ".nycrc.json"}
        ):
            result.append(path.as_posix())
    return sorted(set(result))


def detect_frameworks(
    paths: list[Path], contents: dict[str, str], package_data: dict[str, dict[str, Any]]
) -> list[str]:
    names = {path.name for path in paths}
    combined = "\n".join(contents.values()).lower()
    frameworks: set[str] = set()
    package_deps: set[str] = set()
    for data in package_data.values():
        for section in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
            values = data.get(section, {})
            if isinstance(values, dict):
                package_deps.update(str(key).lower() for key in values)
    def has(token: str) -> bool:
        return token.lower() in combined or token.lower() in package_deps
    if has("jest") or any(name.startswith("jest.config") for name in names):
        frameworks.add("Jest")
    if has("vitest") or any(name.startswith("vitest.config") for name in names):
        frameworks.add("Vitest")
    if has("mocha") or any(name.startswith("mocha.config") for name in names):
        frameworks.add("Mocha")
    if has("ava"):
        frameworks.add("AVA")
    if has("@playwright/test") or any(name.startswith("playwright.config") for name in names):
        frameworks.add("Playwright")
    if has("cypress") or any(name.startswith("cypress.config") for name in names):
        frameworks.add("Cypress")
    if has("@testing-library"):
        frameworks.add("Testing Library")
    if has("pytest") or "pytest.ini" in names or "pytest-cov" in combined:
        frameworks.add("pytest")
    if has("unittest"):
        frameworks.add("unittest")
    if "go.mod" in names or any(path.name.endswith("_test.go") for path in paths):
        frameworks.add("Go testing")
    if "testify" in combined or "github.com/stretchr/testify" in combined:
        frameworks.add("Testify")
    if has("junit") or "src/test" in combined:
        frameworks.add("JUnit")
    if has("testng"):
        frameworks.add("TestNG")
    if has("kotest"):
        frameworks.add("Kotest")
    if has("spock"):
        frameworks.add("Spock")
    if has("xunit"):
        frameworks.add("xUnit")
    if has("nunit"):
        frameworks.add("NUnit")
    if has("mstest"):
        frameworks.add("MSTest")
    if "Cargo.toml" in names:
        frameworks.add("cargo test")
    if has("rstest"):
        frameworks.add("rstest")
    if has("proptest"):
        frameworks.add("proptest")
    if has("rspec"):
        frameworks.add("RSpec")
    if has("minitest"):
        frameworks.add("Minitest")
    if has("phpunit"):
        frameworks.add("PHPUnit")
    if has("pest"):
        frameworks.add("Pest")
    if "Package.swift" in names or ".swift" in {path.suffix.lower() for path in paths} and "XCTest" in "\n".join(contents.values()):
        frameworks.add("XCTest")
    return sorted(frameworks)


def discover_manifest_commands(
    paths: list[Path],
    contents: dict[str, str],
    package_data: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    commands: list[dict[str, str]] = []
    lock_managers: dict[str, str] = {}
    for path in paths:
        manager = LOCKFILE_NAMES.get(path.name)
        if manager in {"npm", "yarn", "pnpm", "bun"}:
            lock_managers[path.parent.as_posix()] = manager

    for rel, data in sorted(package_data.items()):
        scripts = data.get("scripts", {})
        if not isinstance(scripts, dict):
            continue
        package_path = Path(rel)
        package_dir = str(package_path.parent)
        package_dir = "" if package_dir == "." else package_dir
        manager = "npm"
        declared_manager = data.get("packageManager")
        if isinstance(declared_manager, str) and declared_manager:
            declared_name = declared_manager.split("@", 1)[0].lower()
            if declared_name in {"npm", "yarn", "pnpm", "bun"}:
                manager = declared_name
        else:
            search_dir = package_path.parent
            while True:
                candidate = lock_managers.get(search_dir.as_posix())
                if candidate:
                    manager = candidate
                    break
                if search_dir == Path("."):
                    break
                search_dir = search_dir.parent
        for script_name, value in sorted(scripts.items()):
            if not isinstance(value, str):
                continue
            lower_name = script_name.lower()
            lower_value = value.lower()
            if lower_name == "test" or lower_name.startswith("test:") or re.search(r"\b(test|pytest|jest|vitest|mocha|playwright|cypress)\b", lower_value):
                invocation = command_for_script(manager, script_name)
                if package_dir:
                    invocation = f"cd {package_dir} && {invocation}"
                add_command(commands, invocation, f"{rel}#scripts.{script_name}")
    for path in paths:
        rel = path.as_posix()
        text = contents.get(rel, "")
        if path.name == "Makefile":
            for match in re.finditer(r"(?m)^([A-Za-z0-9_.-]*(?:test|check|verify|ci)[A-Za-z0-9_.-]*):", text, re.IGNORECASE):
                add_command(commands, f"make {match.group(1)}", rel)
        elif path.name in {"Taskfile.yml", "Taskfile.yaml"}:
            for match in re.finditer(r"(?m)^\s{0,4}([A-Za-z0-9_.-]*(?:test|check|verify|ci)[A-Za-z0-9_.-]*):\s*$", text, re.IGNORECASE):
                add_command(commands, f"task {match.group(1)}", rel)
    names = {path.name for path in paths}
    combined = "\n".join(contents.values()).lower()
    if "pytest.ini" in names or "pytest" in combined:
        add_command(commands, "pytest", "pytest configuration or dependency")
    if "go.mod" in names or any(path.name.endswith("_test.go") for path in paths):
        add_command(commands, "go test ./...", "Go testing convention")
    if "Cargo.toml" in names:
        add_command(commands, "cargo test", "Cargo testing convention")
    if "pom.xml" in names and ("junit" in combined or "src/test" in combined):
        add_command(commands, "mvn test", "Maven test configuration")
    if "build.gradle" in names or "build.gradle.kts" in names:
        add_command(commands, "./gradlew test", "Gradle test task")
    if any(path.suffix.lower() in {".sln", ".csproj", ".fsproj"} for path in paths) and any(framework in combined for framework in ("xunit", "nunit", "mstest", "microsoft.net.test.sdk")):
        add_command(commands, "dotnet test", ".NET test configuration")
    return commands


def clean_ci_line(line: str) -> str:
    value = line.strip()
    value = re.sub(r"^[-*]\s*", "", value)
    value = re.sub(r"^(?:run|command|script):\s*", "", value, flags=re.IGNORECASE)
    value = value.strip().strip('"\'')
    return value


def discover_ci_commands(paths: list[Path], contents: dict[str, str]) -> tuple[list[str], list[dict[str, str]]]:
    configs: list[str] = []
    commands: list[dict[str, str]] = []
    for path in paths:
        if not is_ci_path(path):
            continue
        rel = path.as_posix()
        configs.append(rel)
        for line in contents.get(rel, "").splitlines():
            cleaned = clean_ci_line(line)
            for match in CI_COMMAND_RE.finditer(cleaned):
                add_command(commands, match.group(0), rel)
    return sorted(set(configs)), commands


def discover_coverage(
    paths: list[Path], contents: dict[str, str], skipped_reports: list[Path]
) -> dict[str, Any]:
    tools: set[str] = set()
    config_paths: set[str] = set()
    reports: list[str] = []
    for path in paths:
        rel = path.as_posix()
        name = path.name.lower()
        text = contents.get(rel, "").lower()
        if name in {".coveragerc", "coverage.yml", "coverage.yaml", "coverage.xml"}:
            config_paths.add(rel)
            tools.add("coverage.py")
        if name in {".nycrc", ".nycrc.json", ".nyc_output"} or "nyc" in text or "istanbul" in text:
            config_paths.add(rel)
            tools.add("Istanbul/nyc")
        if "pytest-cov" in text:
            tools.add("pytest-cov")
        if "c8" in text:
            tools.add("c8")
        if "jacoco" in text:
            tools.add("JaCoCo")
        if "coverlet" in text:
            tools.add("coverlet")
        if "tarpaulin" in text or "llvm-cov" in text:
            tools.add("Rust coverage tooling")
        if path.suffix.lower() in {".info", ".coverage", ".xml"} and any(token in name for token in ("lcov", "coverage", "jacoco", "cobertura")):
            reports.append(rel)
        if name in {"lcov.info", "jacoco.xml", "cobertura.xml"}:
            reports.append(rel)
        if name in {"coverage", "htmlcov", ".nyc_output"}:
            reports.append(rel)
    reports.extend(path.as_posix() for path in skipped_reports if path.name.lower() in REPORT_DIR_NAMES)
    combined = "\n".join(contents.values()).lower()
    if "go test -cover" in combined:
        tools.add("Go coverage")
    return {
        "tools": sorted(tools),
        "config_paths": sorted(config_paths),
        "reports": sorted(set(reports)),
    }


def discover_supporting_artifacts(paths: list[Path], sample_size: int) -> dict[str, Any]:
    categories: dict[str, list[str]] = defaultdict(list)
    for path in paths:
        lowered = "/".join(part.lower() for part in path.parts)
        name = path.name.lower()
        if "snapshot" in lowered or name.endswith(".snap"):
            categories["snapshots"].append(path.as_posix())
        elif any(token in lowered for token in ("fixture", "fixtures")):
            categories["fixtures"].append(path.as_posix())
        elif any(token in lowered for token in ("mock", "mocks")):
            categories["mocks"].append(path.as_posix())
        elif any(token in lowered for token in ("fake", "fakes")):
            categories["fakes"].append(path.as_posix())
        elif any(token in lowered for token in ("stub", "stubs")):
            categories["stubs"].append(path.as_posix())
    return {
        category: {"count": len(values), "samples": sorted(values)[:sample_size]}
        for category, values in sorted(categories.items())
    }


def discover_test_files(paths: list[Path], sample_size: int) -> tuple[dict[str, Any], list[dict[str, str]]]:
    test_paths = sorted(path for path in paths if is_test_file(path))
    by_kind = Counter(test_kind(path) for path in test_paths)
    locations = Counter(path.parent.as_posix() for path in test_paths)
    samples: list[dict[str, str]] = []
    for kind in ("unit", "integration", "e2e", "other"):
        for path in (candidate for candidate in test_paths if test_kind(candidate) == kind):
            if len(samples) >= sample_size:
                break
            samples.append({"path": path.as_posix(), "kind": kind})
    inventory = {
        "total": len(test_paths),
        "by_kind": dict(sorted(by_kind.items())),
        "locations": [
            {"path": path, "count": count}
            for path, count in sorted(locations.items())
        ],
        "samples": samples,
    }
    return inventory, samples


def discover_instructions(paths: list[Path]) -> list[str]:
    return sorted(
        path.as_posix()
        for path in paths
        if path.name in INSTRUCTION_NAMES or path.name.lower().startswith("readme")
    )


def git_history(root: Path, paths: list[Path]) -> dict[str, Any]:
    try:
        check = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"available": False, "reason": f"Git unavailable: {exc}", "commits_sampled": 0, "hotspots": []}
    if check.returncode != 0 or check.stdout.strip() != "true":
        return {"available": False, "reason": "not a Git work tree", "commits_sampled": 0, "hotspots": []}
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "log", "--format=%H", "--name-only", "-n", "100"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"available": False, "reason": f"could not read Git history: {exc}", "commits_sampled": 0, "hotspots": []}
    if result.returncode != 0:
        return {"available": False, "reason": result.stderr.strip() or "Git history unavailable", "commits_sampled": 0, "hotspots": []}
    counts: Counter[str] = Counter()
    commits = 0
    current: Optional[set[str]] = None
    for line in result.stdout.splitlines():
        line = line.strip()
        if re.fullmatch(r"[0-9a-fA-F]{7,64}", line):
            if current is not None:
                for name in current:
                    counts[name] += 1
            current = set()
            commits += 1
        elif line and current is not None:
            path = Path(line)
            if not is_test_file(path) and not any(part in IGNORED_DIRS for part in path.parts):
                current.add(path.as_posix())
    if current is not None:
        for name in current:
            counts[name] += 1
    hotspots = [
        {"path": path, "commits": count}
        for path, count in counts.most_common(20)
    ]
    return {"available": True, "commits_sampled": commits, "hotspots": hotspots}


def collect(root: Path, max_files: int, sample_size: int) -> dict[str, Any]:
    errors: list[str] = []
    files, truncated, skipped_reports = walk_files(root, max(1, max_files), errors)
    files = sorted(files, key=lambda path: path.as_posix())
    rel_files = [Path(relative(path, root)) for path in files]
    rel_skipped_reports = [Path(relative(path, root)) for path in skipped_reports]
    contents: dict[str, str] = {}
    package_data: dict[str, dict[str, Any]] = {}
    for path, rel_path in zip(files, rel_files):
        if is_config_path(rel_path) or is_ci_path(rel_path):
            rel = rel_path.as_posix()
            text = read_text(path, errors)
            contents[rel] = text
            data = json_object(rel_path, text)
            if data is not None:
                package_data[rel] = data
    languages, ecosystems = detect_languages(rel_files)
    package_managers = detect_package_managers(rel_files)
    test_inventory, samples = discover_test_files(rel_files, max(0, sample_size))
    ci_configs, ci_commands = discover_ci_commands(rel_files, contents)
    test_commands = discover_manifest_commands(rel_files, contents, package_data)
    coverage = discover_coverage(rel_files, contents, rel_skipped_reports)
    workspaces = detect_workspaces(rel_files, contents, package_data)
    test_configs = detect_test_configs(rel_files)
    framework_contents = dict(contents)
    for test_path in sorted(path for path in rel_files if is_test_file(path))[:50]:
        framework_contents[test_path.as_posix()] = read_text(root / test_path, errors)
    frameworks = detect_frameworks(rel_files, framework_contents, package_data)
    history = git_history(root, rel_files)
    return {
        "schema_version": SCHEMA_VERSION,
        "root": str(root),
        "scanned_files": len(files),
        "scan_limit_reached": truncated,
        "languages": languages,
        "ecosystems": ecosystems,
        "package_managers": package_managers,
        "build_systems": detect_build_systems(rel_files, contents),
        "workspaces": workspaces,
        "test_frameworks": frameworks,
        "test_commands": test_commands,
        "ci": {
            "config_paths": ci_configs,
            "test_commands": ci_commands,
        },
        "ci_test_commands": ci_commands,
        "test_files": test_inventory,
        "candidate_test_samples": samples,
        "test_configs": test_configs,
        "coverage": coverage,
        "supporting_artifacts": discover_supporting_artifacts(rel_files, max(0, sample_size)),
        "instructions": discover_instructions(rel_files),
        "history": history,
        "hotspots": history["hotspots"],
        "errors": errors,
    }


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    if not root.exists() or not root.is_dir():
        payload = {
            "schema_version": SCHEMA_VERSION,
            "root": str(root),
            "errors": ["inspection root does not exist or is not a directory"],
        }
        print(json.dumps(payload, indent=2 if args.pretty else None, sort_keys=True))
        return 2
    payload = collect(root, args.max_files, args.sample_size)
    print(json.dumps(payload, indent=2 if args.pretty else None, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("inspection interrupted", file=sys.stderr)
        raise SystemExit(130)
