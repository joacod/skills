#!/usr/bin/env python3
"""
TypeScript Configuration Security Audit Script

Validates tsconfig.json for security-relevant compiler options and reports
any missing or insecure settings.

Usage:
    python3 audit-tsconfig.py [path/to/project]
    python3 audit-tsconfig.py  # Uses current directory

Exit codes:
    0 - All critical settings present
    1 - Missing critical settings
    2 - File not found or invalid JSON

Requires Python 3.10+
"""

import json
import re
import sys
from pathlib import Path
from typing import Any


# Security-relevant TypeScript compiler options
# Organized by severity: critical (must have), recommended (should have), optional (nice to have)

CRITICAL_OPTIONS = {
    "strict": {
        "expected": True,
        "description": "Enables all strict type-checking options",
        "risk": "Without strict mode, many type errors are silently ignored",
    },
    "noImplicitAny": {
        "expected": True,
        "description": "Errors on expressions/declarations with implied 'any' type",
        "risk": "Implicit any allows unsafe type assumptions",
    },
    "strictNullChecks": {
        "expected": True,
        "description": "Enables strict null checking",
        "risk": "Null/undefined values can cause runtime errors",
    },
}

RECOMMENDED_OPTIONS = {
    "strictFunctionTypes": {
        "expected": True,
        "description": "Enables strict checking of function types",
        "risk": "Incorrect function signatures can cause runtime errors",
    },
    "strictBindCallApply": {
        "expected": True,
        "description": "Enables strict checking of bind, call, and apply methods",
        "risk": "Incorrect binding can lead to unexpected behavior",
    },
    "strictPropertyInitialization": {
        "expected": True,
        "description": "Ensures class properties are initialized",
        "risk": "Uninitialized properties cause undefined values",
    },
    "noImplicitThis": {
        "expected": True,
        "description": "Errors on 'this' expressions with implied 'any' type",
        "risk": "Incorrect 'this' binding leads to runtime errors",
    },
    "useUnknownInCatchVariables": {
        "expected": True,
        "description": "Catch variables are typed as 'unknown' instead of 'any'",
        "risk": "Any type in catch blocks bypasses type safety",
    },
    "alwaysStrict": {
        "expected": True,
        "description": "Ensures 'use strict' is emitted in all output files",
        "risk": "Non-strict mode allows unsafe JavaScript patterns",
    },
    "noUncheckedIndexedAccess": {
        "expected": True,
        "description": "Adds 'undefined' to index signature results",
        "risk": "Array/object access without bounds checking",
    },
    "noImplicitReturns": {
        "expected": True,
        "description": "Errors on functions without return statements in all code paths",
        "risk": "Missing returns can cause undefined behavior",
    },
    "noFallthroughCasesInSwitch": {
        "expected": True,
        "description": "Errors on fallthrough cases in switch statements",
        "risk": "Fallthrough bugs can bypass logic",
    },
}

OPTIONAL_OPTIONS = {
    "noImplicitOverride": {
        "expected": True,
        "description": "Requires 'override' modifier for overridden methods",
        "risk": "Accidental method shadowing",
    },
    "exactOptionalPropertyTypes": {
        "expected": True,
        "description": "Differentiates between 'undefined' and missing properties",
        "risk": "Confusion between undefined and absent properties",
    },
    "noPropertyAccessFromIndexSignature": {
        "expected": True,
        "description": "Requires indexed access for index signature properties",
        "risk": "Typos in property names go undetected",
    },
    "forceConsistentCasingInFileNames": {
        "expected": True,
        "description": "Ensures consistent casing in file imports",
        "risk": "Case-insensitive file system issues",
    },
    "skipLibCheck": {
        "expected": False,
        "description": "Should NOT skip type checking of declaration files",
        "risk": "Type errors in dependencies go undetected",
    },
}


def load_tsconfig(project_path: Path) -> dict[str, Any] | None:
    """Load and parse tsconfig.json from the given path."""
    tsconfig_path = project_path / "tsconfig.json"

    if not tsconfig_path.exists():
        print(f"Error: tsconfig.json not found at {tsconfig_path}")
        return None

    try:
        with open(tsconfig_path, "r", encoding="utf-8") as f:
            content = f.read()

            # Remove block comments /* ... */
            content = re.sub(r"/\*[\s\S]*?\*/", "", content)

            # Remove single-line comments // ...
            # Be careful not to remove // inside strings
            lines = content.split("\n")
            cleaned_lines = []
            for line in lines:
                comment_idx = line.find("//")
                if comment_idx != -1:
                    before_comment = line[:comment_idx]
                    quote_count = before_comment.count('"') - before_comment.count('\\"')
                    if quote_count % 2 == 0:  # Not inside string
                        line = line[:comment_idx]
                cleaned_lines.append(line)
            cleaned_content = "\n".join(cleaned_lines)

            return json.loads(cleaned_content)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in tsconfig.json: {e}")
        return None
    except Exception as e:
        print(f"Error reading tsconfig.json: {e}")
        return None


def check_option(
    compiler_options: dict[str, Any],
    option_name: str,
    expected_value: Any,
) -> tuple[bool, Any]:
    """Check if a compiler option is set correctly."""
    actual_value = compiler_options.get(option_name)

    if actual_value is None:
        return False, None

    return actual_value == expected_value, actual_value


def audit_tsconfig(project_path: Path) -> int:
    """Audit tsconfig.json for security settings."""
    print(f"\n{'='*60}")
    print("TypeScript Configuration Security Audit")
    print(f"{'='*60}")
    print(f"Project: {project_path.absolute()}\n")

    tsconfig = load_tsconfig(project_path)
    if tsconfig is None:
        return 2

    compiler_options = tsconfig.get("compilerOptions", {})

    critical_issues: list[str] = []
    recommended_issues: list[str] = []
    optional_issues: list[str] = []

    # Check critical options
    print("Critical Settings (Required):")
    print("-" * 40)
    for option, config in CRITICAL_OPTIONS.items():
        is_correct, actual = check_option(
            compiler_options, option, config["expected"]
        )
        icon = "✓" if is_correct else "✗"

        if actual is None:
            value_str = "not set"
        else:
            value_str = str(actual)

        print(f"  {icon} {option}: {value_str} (expected: {config['expected']})")

        if not is_correct:
            critical_issues.append(
                f"  - {option}: {config['description']}\n"
                f"    Risk: {config['risk']}"
            )

    # Check recommended options
    print("\nRecommended Settings:")
    print("-" * 40)
    for option, config in RECOMMENDED_OPTIONS.items():
        is_correct, actual = check_option(
            compiler_options, option, config["expected"]
        )
        icon = "✓" if is_correct else "!"

        if actual is None:
            value_str = "not set"
        else:
            value_str = str(actual)

        print(f"  {icon} {option}: {value_str} (expected: {config['expected']})")

        if not is_correct:
            recommended_issues.append(
                f"  - {option}: {config['description']}\n"
                f"    Risk: {config['risk']}"
            )

    # Check optional options
    print("\nOptional Settings:")
    print("-" * 40)
    for option, config in OPTIONAL_OPTIONS.items():
        is_correct, actual = check_option(
            compiler_options, option, config["expected"]
        )
        icon = "✓" if is_correct else "-"

        if actual is None:
            value_str = "not set"
        else:
            value_str = str(actual)

        print(f"  {icon} {option}: {value_str} (expected: {config['expected']})")

        if not is_correct:
            optional_issues.append(
                f"  - {option}: {config['description']}\n"
                f"    Risk: {config['risk']}"
            )

    # Summary
    print(f"\n{'='*60}")
    print("Summary")
    print(f"{'='*60}")

    total_critical = len(CRITICAL_OPTIONS)
    total_recommended = len(RECOMMENDED_OPTIONS)
    total_optional = len(OPTIONAL_OPTIONS)

    critical_pass = total_critical - len(critical_issues)
    recommended_pass = total_recommended - len(recommended_issues)
    optional_pass = total_optional - len(optional_issues)

    print(f"  Critical:    {critical_pass}/{total_critical} passed")
    print(f"  Recommended: {recommended_pass}/{total_recommended} passed")
    print(f"  Optional:    {optional_pass}/{total_optional} passed")

    if critical_issues:
        print(f"\n{'!'*60}")
        print("CRITICAL ISSUES (Must Fix):")
        print("!" * 60)
        for issue in critical_issues:
            print(issue)
            print()

    if recommended_issues:
        print(f"\n{'-'*60}")
        print("Recommended Improvements:")
        print("-" * 60)
        for issue in recommended_issues:
            print(issue)
            print()

    # Generate fix suggestion
    if critical_issues or recommended_issues:
        print(f"\n{'='*60}")
        print("Suggested tsconfig.json compilerOptions:")
        print("=" * 60)
        print('"compilerOptions": {')
        for option, config in {**CRITICAL_OPTIONS, **RECOMMENDED_OPTIONS}.items():
            is_correct, _ = check_option(compiler_options, option, config["expected"])
            if not is_correct:
                value = "true" if config["expected"] else "false"
                print(f'  "{option}": {value},')
        print("}")

    if critical_issues:
        print(f"\n{'!'*60}")
        print("AUDIT FAILED: Critical settings are missing or incorrect")
        print("!" * 60)
        return 1

    if not recommended_issues:
        print(f"\n{'='*60}")
        print("AUDIT PASSED: All critical and recommended settings are correct")
        print("=" * 60)
    else:
        print(f"\n{'='*60}")
        print("AUDIT PASSED: All critical settings correct (recommendations above)")
        print("=" * 60)

    return 0


def main() -> int:
    """Main entry point."""
    if len(sys.argv) > 1:
        project_path = Path(sys.argv[1])
    else:
        project_path = Path.cwd()

    if not project_path.is_dir():
        print(f"Error: {project_path} is not a directory")
        return 2

    return audit_tsconfig(project_path)


if __name__ == "__main__":
    sys.exit(main())
