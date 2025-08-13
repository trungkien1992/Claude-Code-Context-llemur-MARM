#!/usr/bin/env python3
"""
Validation script for CLI refactoring
Based on lessons learned from the refactoring process

@ai-context: Automated validation to ensure refactoring was successful
@usage: python validate_refactoring.py
"""

import sys
from pathlib import Path
from src.cli_utils import detect_unicode_issues

def validate_no_duplicate_patterns():
    """Check that duplicate CLI patterns have been eliminated"""
    issues = []
    
    # Files that should have been refactored
    files_to_check = [
        "main.py",
        "src/memory/notebook.py", 
        "src/memory/compiler.py",
        "src/ai_context.py",
        "src/claude_integration.py"
    ]
    
    # Patterns that should no longer exist (or be minimal)
    duplicate_patterns = [
        "from ..ctx_core import CtxCore",
        "core = CtxCore()",
        "ctx_path = core.get_active_ctx_path()",
        "import pyperclip",
        "pyperclip.copy("
    ]
    
    for file_path in files_to_check:
        path = Path(file_path)
        if path.exists():
            with open(path, 'r') as f:
                content = f.read()
                for pattern in duplicate_patterns:
                    count = content.count(pattern)
                    if count > 1:  # Allow 1 occurrence, flag multiples
                        issues.append(f"❌ {file_path}: '{pattern}' found {count} times")
                    elif count == 0 and pattern in ["from ..ctx_core import CtxCore"]:
                        # This is good - should be eliminated
                        pass
    
    return issues

def validate_shared_utilities_usage():
    """Check that shared utilities are being used"""
    issues = []
    
    # Check that cli_utils is imported where expected
    files_to_check = [
        "main.py",
        "src/memory/notebook.py",
        "src/memory/compiler.py", 
        "src/ai_context.py",
        "src/claude_integration.py"
    ]
    
    for file_path in files_to_check:
        path = Path(file_path)
        if path.exists():
            with open(path, 'r') as f:
                content = f.read()
                if "from .cli_utils import" not in content and "from ..cli_utils import" not in content and "from src.cli_utils import" not in content:
                    issues.append(f"❌ {file_path}: Missing cli_utils import")
    
    return issues

def validate_decorator_usage():
    """Check that @require_context_llemur decorator is being used"""
    issues = []
    
    # Files that should have the decorator
    files_with_cli = [
        "src/memory/notebook.py",
        "src/memory/compiler.py",
        "src/ai_context.py"
    ]
    
    for file_path in files_with_cli:
        path = Path(file_path)
        if path.exists():
            with open(path, 'r') as f:
                content = f.read()
                decorator_count = content.count("@require_context_llemur")
                if decorator_count == 0:
                    issues.append(f"❌ {file_path}: No @require_context_llemur decorators found")
    
    return issues

def validate_unicode_cleanliness():
    """Check for Unicode issues that might cause problems"""
    issues = []
    
    files_to_check = [
        "src/memory/compiler.py",  # This had the most Unicode issues
        "src/memory/notebook.py",
        "src/ai_context.py"
    ]
    
    for file_path in files_to_check:
        path = Path(file_path)
        if path.exists():
            unicode_issues = detect_unicode_issues(path)
            # Filter out expected Unicode (emojis and bullet points in messages are OK)
            problematic = [issue for issue in unicode_issues 
                          if not any(char in issue[1] for char in ["✅", "❌", "📋", "📔", "💡", "📝", "•"])]
            if problematic:
                issues.append(f"⚠️  {file_path}: Unexpected Unicode characters found")
                for line_num, line in problematic[:3]:  # Show first 3
                    issues.append(f"   Line {line_num}: {line[:50]}...")
    
    return issues

def main():
    """Run all validation checks"""
    print("🔍 Validating CLI Refactoring...")
    print("=" * 50)
    
    all_issues = []
    
    # Run all validation checks
    checks = [
        ("Duplicate Patterns", validate_no_duplicate_patterns),
        ("Shared Utilities Usage", validate_shared_utilities_usage), 
        ("Decorator Usage", validate_decorator_usage),
        ("Unicode Cleanliness", validate_unicode_cleanliness)
    ]
    
    for check_name, check_func in checks:
        print(f"\n📋 {check_name}:")
        issues = check_func()
        if issues:
            all_issues.extend(issues)
            for issue in issues:
                print(f"  {issue}")
        else:
            print("  ✅ All checks passed")
    
    # Summary
    print("\n" + "=" * 50)
    if all_issues:
        print(f"❌ Validation completed with {len(all_issues)} issues found")
        return 1
    else:
        print("✅ All validation checks passed! Refactoring is successful.")
        return 0

if __name__ == "__main__":
    sys.exit(main())