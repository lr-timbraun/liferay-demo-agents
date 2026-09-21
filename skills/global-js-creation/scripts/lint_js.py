#!/usr/bin/env python3
import os
import sys

def lint_js(extension_dir):
    """Lints Liferay JS Client Extension deliverables for syntax and best-practice compliance."""
    print(f"\n[LINTER] Auditing Global JS client-extension in: {extension_dir}")
    
    yaml_path = os.path.join(extension_dir, "client-extension.yaml")
    js_path = os.path.join(extension_dir, "custom.js")
    
    # Check 1: Verify mandatory files exist
    if not os.path.exists(yaml_path):
        print(f"Error: Mandatory 'client-extension.yaml' is missing.")
        return False
    if not os.path.exists(js_path):
        print(f"Error: Mandatory 'custom.js' is missing.")
        return False
        
    # Check 2: Parse client-extension.yaml line-by-line (No dependencies required)
    is_global_js_type = False
    has_custom_js_url = False
    
    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            for line in f:
                line_stripped = line.strip()
                if line_stripped.startswith("type:"):
                    ext_type = line_stripped.split(":", 1)[1].strip()
                    if ext_type == "globalJS":
                        is_global_js_type = True
                elif "- custom.js" in line_stripped:
                    has_custom_js_url = True
                    
        if not is_global_js_type:
            print("Error: Descriptor type is missing or invalid. It must be strictly 'type: globalJS'.")
            return False
        if not has_custom_js_url:
            print("Error: 'custom.js' is not registered under the 'urls' block inside client-extension.yaml.")
            return False
    except Exception as e:
        print(f"Error: Failed to read client-extension.yaml: {e}")
        return False
        
    # Check 3: Check custom.js syntax and DOMContentLoaded best practices
    try:
        with open(js_path, "r", encoding="utf-8") as f:
            js_content = f.read()
            
        open_braces = js_content.count("{")
        close_braces = js_content.count("}")
        
        if open_braces != close_braces:
            print(f"Error: Syntax Error in 'custom.js'. Braces are unbalanced! Found {open_braces} open braces '{{' and {close_braces} close braces '}}'.")
            return False
            
        # Best Practice Check: DOMContentLoaded listener
        # Ensure any script querying the DOM (document.querySelector, etc.) wraps execution safely
        if "document." in js_content or "window." in js_content or "$" in js_content:
            if "DOMContentLoaded" not in js_content and "addEventListener" not in js_content:
                print("Best Practice Violation: 'custom.js' performs DOM/window operations but does not wrap them inside a 'DOMContentLoaded' event listener. This can cause execution failures on slow connections.")
                return False
                
    except Exception as e:
        print(f"Error: Failed to read custom.js: {e}")
        return False
        
    print("[SUCCESS] Global JS deliverables passed syntax and best-practice checks.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lint_js.py <extension_directory>")
        sys.exit(1)
    success = lint_js(sys.argv[1])
    sys.exit(0 if success else 1)
