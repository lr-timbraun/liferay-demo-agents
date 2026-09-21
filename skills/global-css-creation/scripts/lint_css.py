#!/usr/bin/env python3
import os
import sys

def lint_css(extension_dir):
    """Lints Liferay CSS Client Extension deliverables for syntax and best-practice compliance."""
    print(f"\n[LINTER] Auditing Global CSS client-extension in: {extension_dir}")
    
    yaml_path = os.path.join(extension_dir, "client-extension.yaml")
    css_path = os.path.join(extension_dir, "custom.css")
    
    # Check 1: Verify mandatory files exist
    if not os.path.exists(yaml_path):
        print(f"Error: Mandatory 'client-extension.yaml' is missing.")
        return False
    if not os.path.exists(css_path):
        print(f"Error: Mandatory 'custom.css' is missing.")
        return False
        
    # Check 2: Parse client-extension.yaml line-by-line (No dependencies required)
    is_global_css_type = False
    has_custom_css_url = False
    
    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            for line in f:
                line_stripped = line.strip()
                if line_stripped.startswith("type:"):
                    ext_type = line_stripped.split(":", 1)[1].strip()
                    if ext_type == "globalCSS":
                        is_global_css_type = True
                elif "- custom.css" in line_stripped:
                    has_custom_css_url = True
                    
        if not is_global_css_type:
            print("Error: Descriptor type is missing or invalid. It must be strictly 'type: globalCSS'.")
            return False
        if not has_custom_css_url:
            print("Error: 'custom.css' is not registered under the 'urls' block inside client-extension.yaml.")
            return False
    except Exception as e:
        print(f"Error: Failed to read client-extension.yaml: {e}")
        return False
        
    # Check 3: Check custom.css syntax (brace balance)
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
            
        open_braces = css_content.count("{")
        close_braces = css_content.count("}")
        
        if open_braces != close_braces:
            print(f"Error: Syntax Error in 'custom.css'. Braces are unbalanced! Found {open_braces} open braces '{{' and {close_braces} close braces '}}'.")
            return False
            
    except Exception as e:
        print(f"Error: Failed to read custom.css: {e}")
        return False
        
    print("[SUCCESS] Global CSS deliverables passed syntax and best-practice checks.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lint_css.py <extension_directory>")
        sys.exit(1)
    success = lint_css(sys.argv[1])
    sys.exit(0 if success else 1)
