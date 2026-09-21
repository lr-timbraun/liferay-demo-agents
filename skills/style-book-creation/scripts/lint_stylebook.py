#!/usr/bin/env python3
import os
import sys
import json
import re

def lint_stylebook(stylebook_dir):
    """Lints Liferay Stylebook deliverables for syntax and best-practice compliance."""
    print(f"\n[LINTER] Auditing Stylebook deliverables in: {stylebook_dir}")
    
    sb_json_path = os.path.join(stylebook_dir, "style-book.json")
    tokens_json_path = os.path.join(stylebook_dir, "frontend-tokens-values.json")
    
    # Check 1: Verify mandatory files exist
    if not os.path.exists(sb_json_path):
        print(f"Error: Mandatory 'style-book.json' is missing.")
        return False
    if not os.path.exists(tokens_json_path):
        print(f"Error: Mandatory 'frontend-tokens-values.json' is missing.")
        return False
        
    # Check 2: Parse style-book.json
    try:
        with open(sb_json_path, "r", encoding="utf-8") as f:
            sb_data = json.load(f)
        if "name" not in sb_data or "styleBookDefinitionKey" not in sb_data:
            print("Error: 'style-book.json' is missing required keys ('name' or 'styleBookDefinitionKey').")
            return False
    except Exception as e:
        print(f"Error: Failed to parse 'style-book.json' as valid JSON: {e}")
        return False
        
    # Check 3: Parse and validate frontend-tokens-values.json (Uppercase HEX best practices)
    try:
        with open(tokens_json_path, "r", encoding="utf-8") as f:
            tokens_data = json.load(f)
            
        if not isinstance(tokens_data, dict):
            print("Error: 'frontend-tokens-values.json' root must be a JSON object/dictionary.")
            return False
            
        # Recursive variable checker
        errors = []
        def check_values(data, path=""):
            for k, v in data.items():
                current_path = f"{path}.{k}" if path else k
                if isinstance(v, dict):
                    check_values(v, current_path)
                elif isinstance(v, str):
                    # Enforce strict uppercase HEX for color values
                    if v.startswith("#"):
                        if not re.match(r"^#[0-9A-F]{6}$", v):
                            errors.append(f"Best Practice Violation: Color token '{current_path}' has value '{v}'. Color values must be strictly uppercase 6-character HEX strings (e.g. '#FFFFFF', not '#ffffff' or '#FFF').")
                            
        check_values(tokens_data)
        if errors:
            print("\n".join(errors))
            return False
            
    except Exception as e:
        print(f"Error: Failed to parse 'frontend-tokens-values.json' as valid JSON: {e}")
        return False
        
    print("[SUCCESS] Stylebook deliverables passed syntax and best-practice checks.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lint_stylebook.py <stylebook_directory>")
        sys.exit(1)
    success = lint_stylebook(sys.argv[1])
    sys.exit(0 if success else 1)
