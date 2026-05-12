#!/usr/bin/env python3
"""Audit CSS/Tailwind style token debt in a repository.

Usage:
    python scripts/audit_style_tokens.py <project-root> --output style-token-audit.md

The script intentionally uses only the Python standard library. It is a first-pass
inventory, not a replacement for manual design review.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

STYLE_EXTENSIONS = {
    ".css",
    ".scss",
    ".sass",
    ".less",
    ".html",
    ".htm",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".vue",
    ".svelte",
    ".astro",
    ".mdx",
}

IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".cache",
    ".parcel-cache",
    ".vite",
    ".next",
    ".nuxt",
    ".output",
    ".svelte-kit",
    ".turbo",
    ".vercel",
    "out",
    "storybook-static",
    "vendor",
}

IGNORE_FILES = {
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "bun.lockb",
    "style-token-audit.md",
}

PATTERNS = {
    "hex_colors": re.compile(r"(?<![A-Za-z0-9_-])#[0-9a-fA-F]{3,8}\b"),
    "rgb_hsl_colors": re.compile(r"\b(?:rgb|rgba|hsl|hsla|oklch|oklab|color-mix)\([^;{}<>\n]+\)"),
    "px_values": re.compile(r"(?<![A-Za-z0-9_-])-?\d*\.?\d+px\b"),
    "rem_values": re.compile(r"(?<![A-Za-z0-9_-])-?\d*\.?\d+rem\b"),
    "font_size_decls": re.compile(r"font-size\s*:\s*[^;\n]+"),
    "line_height_decls": re.compile(r"line-height\s*:\s*[^;\n]+"),
    "box_shadow_decls": re.compile(r"box-shadow\s*:\s*[^;\n]+"),
    "z_index_decls": re.compile(r"z-index\s*:\s*-?\d+"),
    "important": re.compile(r"!important\b"),
    "tailwind_arbitrary": re.compile(r"\b(?:bg|text|border|ring|from|via|to|p|px|py|m|mx|my|gap|w|h|min-w|min-h|max-w|max-h|rounded|shadow|grid-cols|top|right|bottom|left|inset)-\[[^\]\n]+\]"),
    "tailwind_color_utils": re.compile(r"\b(?:bg|text|border|ring|fill|stroke|decoration|from|via|to)-(?:slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose|white|black)(?:-\d{2,3})?(?:/[0-9]+)?\b"),
    "tailwind_dark_pairs": re.compile(r"\bdark:[A-Za-z0-9_:\-/\[\]\.]+"),
}


@dataclass(frozen=True)
class Finding:
    file: Path
    line_no: int
    value: str
    line: str


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.name in IGNORE_FILES:
            continue
        if ".min." in path.name:
            continue
        if path.suffix.lower() not in STYLE_EXTENSIONS:
            continue
        yield path


def scan_file(path: Path, root: Path) -> dict[str, list[Finding]]:
    results: dict[str, list[Finding]] = defaultdict(list)
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return results

    for line_no, line in enumerate(text.splitlines(), start=1):
        for name, pattern in PATTERNS.items():
            for match in pattern.finditer(line):
                value = match.group(0).strip()
                rel = path.relative_to(root)
                results[name].append(Finding(rel, line_no, value, line.strip()))
    return results


def add_counter_section(lines: list[str], title: str, findings: list[Finding], max_items: int) -> None:
    lines.append(f"## {title}")
    lines.append("")
    if not findings:
        lines.append("No matches found.")
        lines.append("")
        return

    counter = Counter(f.value for f in findings)
    lines.append(f"Total matches: {len(findings)}")
    lines.append(f"Unique values: {len(counter)}")
    lines.append("")
    lines.append("| Value | Count | Example |")
    lines.append("|---|---:|---|")
    for value, count in counter.most_common(max_items):
        example = next(f for f in findings if f.value == value)
        escaped_value = value.replace("|", "\\|")
        escaped_example = f"`{example.file}:{example.line_no}`".replace("|", "\\|")
        lines.append(f"| `{escaped_value}` | {count} | {escaped_example} |")
    lines.append("")


def add_file_hotspot_section(lines: list[str], all_findings: dict[str, list[Finding]], max_items: int) -> None:
    file_counter: Counter[str] = Counter()
    for findings in all_findings.values():
        for finding in findings:
            file_counter[str(finding.file)] += 1

    lines.append("## Files with the most style-token debt")
    lines.append("")
    if not file_counter:
        lines.append("No matches found.")
        lines.append("")
        return

    lines.append("| File | Matches |")
    lines.append("|---|---:|")
    for file, count in file_counter.most_common(max_items):
        lines.append(f"| `{file}` | {count} |")
    lines.append("")


def add_sample_section(lines: list[str], title: str, findings: list[Finding], max_samples: int) -> None:
    lines.append(f"## Sample lines: {title}")
    lines.append("")
    if not findings:
        lines.append("No samples.")
        lines.append("")
        return

    for finding in findings[:max_samples]:
        safe_line = finding.line.replace("`", "\\`")
        lines.append(f"- `{finding.file}:{finding.line_no}`: `{safe_line}`")
    lines.append("")


def build_report(root: Path, all_findings: dict[str, list[Finding]], file_count: int, max_items: int, max_samples: int) -> str:
    lines: list[str] = []
    lines.append("# Style token audit")
    lines.append("")
    lines.append(f"Scanned root: `{root}`")
    lines.append(f"Files scanned: {file_count}")
    lines.append("")
    lines.append("This is a first-pass inventory of hardcoded styling values and Tailwind utility patterns. Review findings manually before changing code.")
    lines.append("")

    total = sum(len(v) for v in all_findings.values())
    lines.append("## Summary")
    lines.append("")
    lines.append("| Category | Matches |")
    lines.append("|---|---:|")
    for name in PATTERNS:
        lines.append(f"| `{name}` | {len(all_findings.get(name, []))} |")
    lines.append(f"| **total** | **{total}** |")
    lines.append("")

    add_file_hotspot_section(lines, all_findings, max_items)

    add_counter_section(lines, "Hardcoded hex colors", all_findings.get("hex_colors", []), max_items)
    add_counter_section(lines, "Functional colors", all_findings.get("rgb_hsl_colors", []), max_items)
    add_counter_section(lines, "Pixel values", all_findings.get("px_values", []), max_items)
    add_counter_section(lines, "REM values", all_findings.get("rem_values", []), max_items)
    add_counter_section(lines, "Tailwind arbitrary utilities", all_findings.get("tailwind_arbitrary", []), max_items)
    add_counter_section(lines, "Tailwind palette utilities", all_findings.get("tailwind_color_utils", []), max_items)
    add_counter_section(lines, "Dark variant utilities", all_findings.get("tailwind_dark_pairs", []), max_items)
    add_counter_section(lines, "Important declarations", all_findings.get("important", []), max_items)

    for name in ["font_size_decls", "line_height_decls", "box_shadow_decls", "z_index_decls"]:
        add_sample_section(lines, name, all_findings.get(name, []), max_samples)

    lines.append("## Recommended next steps")
    lines.append("")
    lines.append("1. Group repeated raw colors into primitive and semantic color tokens.")
    lines.append("2. Map repeated text/background/border pairs to semantic roles.")
    lines.append("3. Normalize common spacing and radius values onto a small scale.")
    lines.append("4. Replace repeated Tailwind light/dark class pairs with semantic utilities where appropriate.")
    lines.append("5. Keep one-off art direction local unless it repeats or needs theme behavior.")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit CSS/Tailwind style token debt.")
    parser.add_argument("root", type=Path, help="Project root to scan")
    parser.add_argument("--output", "-o", type=Path, default=Path("style-token-audit.md"), help="Markdown report output path")
    parser.add_argument("--max-items", type=int, default=25, help="Maximum table rows per section")
    parser.add_argument("--max-samples", type=int, default=20, help="Maximum sample lines per section")
    args = parser.parse_args()

    if args.max_items < 0:
        parser.error("--max-items must be non-negative")
    if args.max_samples < 0:
        parser.error("--max-samples must be non-negative")

    root = args.root.resolve()
    if not root.exists() or not root.is_dir():
        parser.error(f"root must be an existing directory: {root}")

    all_findings: dict[str, list[Finding]] = defaultdict(list)
    file_count = 0
    for file in iter_files(root):
        file_count += 1
        file_results = scan_file(file, root)
        for name, findings in file_results.items():
            all_findings[name].extend(findings)

    report = build_report(root, all_findings, file_count, args.max_items, args.max_samples)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
