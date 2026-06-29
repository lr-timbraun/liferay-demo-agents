#!/usr/bin/env python3
import os
import sys
import json
import argparse

def get_meta_url():
    """Reads `./meta` to parse and reconstruct the LDM project's LIFERAY_HOST URL."""
    meta_path = './meta'
    if not os.path.exists(meta_path):
        # Fallback if meta is in parent or other location
        meta_path = os.path.join(os.getcwd(), 'meta')
        
    if not os.path.exists(meta_path):
        return "https://localhost"
        
    meta = {}
    with open(meta_path, 'r', encoding='utf-8') as f:
        for line in f:
            line_stripped = line.strip()
            if line_stripped and '=' in line_stripped:
                key, val = line_stripped.split('=', 1)
                meta[key.strip()] = val.strip().strip('"').strip("'")
                
    host_name = meta.get('host_name', 'localhost')
    port = meta.get('port', '8080')
    ssl = meta.get('ssl', 'false').lower() == 'true'
    ssl_port = meta.get('ssl_port', '443')
    
    if ssl:
        url = f"https://{host_name}"
        if ssl_port != '443':
            url += f":{ssl_port}"
    else:
        url = f"http://{host_name}"
        if port != '80':
            url += f":{port}"
            
    return url

def parse_portal_ext():
    """Parses `./files/portal-ext.properties` for admin prefix and password."""
    properties_path = './files/portal-ext.properties'
    prefix = 'test'
    password = 'test'
    
    if os.path.exists(properties_path):
        with open(properties_path, 'r', encoding='utf-8') as f:
            for line in f:
                line_stripped = line.strip()
                if line_stripped and not line_stripped.startswith('#') and '=' in line_stripped:
                    key, val = line_stripped.split('=', 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key == 'default.admin.email.address.prefix':
                        prefix = val
                    elif key == 'default.admin.password':
                        password = val
                        
    return f"{prefix}@liferay.com", password

def enable_mcp_flag():
    """Ensures feature.flag.LPD-63311=true is set in portal-ext.properties."""
    properties_dir = './files'
    properties_path = './files/portal-ext.properties'
    flag = 'feature.flag.LPD-63311=true'
    
    os.makedirs(properties_dir, exist_ok=True)
    
    content = []
    has_flag = False
    
    if os.path.exists(properties_path):
        with open(properties_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith('feature.flag.LPD-63311'):
                    content.append(f"{flag}\n")
                    has_flag = True
                else:
                    content.append(line)
                    
    if not has_flag:
        # Append to file
        content.append(f"\n# Enable Liferay Model Context Protocol (MCP) Server\n{flag}\n")
        
    with open(properties_path, 'w', encoding='utf-8') as f:
        f.writelines(content)
    print(f"Verified and enabled Liferay MCP Server flag in {properties_path}")

def update_gitignore(file_path, exclusions):
    """Safely appends exclusions to a gitignore file without duplicating lines."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    existing_lines = set()
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                existing_lines.add(line.strip())
                
    append_lines = []
    for exc in exclusions:
        if exc.strip() and exc.strip() not in existing_lines:
            append_lines.append(f"{exc}\n")
            
    if append_lines:
        with open(file_path, 'a', encoding='utf-8') as f:
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                f.write("\n")
            f.writelines(append_lines)
        print(f"Appended missing exclusions to {file_path}")

def create_demo_plan():
    """Generates the standardized liferay/specs/DEMO_PLAN.md tracker if missing."""
    plan_path = './liferay/specs/DEMO_PLAN.md'
    if os.path.exists(plan_path):
        return
        
    content = """# Demo Experience & Progress Plan

## 1. Core Identity & Experience Strategy
*   **Prospect URL / Sourced Brand:** [Brand URL / Name]
*   **Demo Narrative Theme:** [The central story/narrative theme]
*   **Target Personas:**
    *   [Persona A] - [Roles & Objectives]
    *   [Persona B] - [Roles & Objectives]

## 2. Global Site Architecture & Navigation
- **Header:** [Global Header spec]
- **Footer:** [Global Footer spec]
- **Navigation Menu Structure:**
  - Homepage
  - [Demo Hub Page]
  - [Secondary Page]

## 3. Experience Map (Wow Moments)
*   `[ ]` **Wow Moment 1:** [Description]
*   `[ ]` **Wow Moment 2:** [Description]
*   `[ ]` **Wow Moment 3:** [Description]

## 4. Component Inventory & Status
| Component Type | Name / Scope | Location / Path | Status |
| :--- | :--- | :--- | :--- |
| Stylebook | Brand Identity mapping | `liferay/stylebooks/` | `[ ] Planned` |
| UI Layout | Homepage Copy / Redesign | `liferay/fragments/` | `[ ] Planned` |
| UI Component | [Custom Fragment] | `liferay/fragments/` | `[ ] Planned` |
| Data Model | [Liferay Object] | `liferay/specs/objects/` | `[ ] Planned` |

## 5. Deployment & Launch Checklist
- [ ] LDM Containers running and healthy
- [ ] Stylebooks successfully uploaded and linked
- [ ] Fragments collection imported via Site Builder UI
- [ ] Liferay Objects and populations successfully provisioned
- [ ] Pages created and fragments placed onto pages
- [ ] Live demo scenario validated via Playwright

---
*Status: In-Scaffolding. Ready for Phase 1 Centralized Planning.*
"""
    with open(plan_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created template {plan_path}")

def get_extension_version():
    """Attempts to read the version dynamically from gemini-extension.json."""
    try:
        curr = os.path.dirname(os.path.abspath(__file__))
        for _ in range(4):
            path = os.path.join(curr, 'gemini-extension.json')
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f).get('version', '0.0.0')
            curr = os.path.dirname(curr)
    except Exception:
        pass
    return '0.0.0'

def main():
    parser = argparse.ArgumentParser(description="LDA Workspace Scaffolding and Environment Config Orchestrator.")
    parser.add_argument('--mode', choices=['init', 'activate', 'check-version'], required=True, help="Orchestration mode")
    parser.add_argument('--host', help="Liferay Host URL (only required for init mode)")
    parser.add_argument('--lda-version', default=None, help="Liferay Demo Agent version")
    
    args = parser.parse_args()
    
    # Check version mode
    if args.mode == 'check-version':
        project_version = '0.1.0' # Default fallback if lda.properties is missing
        lda_prop_path = './lda.properties'
        if os.path.exists(lda_prop_path):
            try:
                with open(lda_prop_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip().startswith('lda.version'):
                            project_version = line.split('=', 1)[1].strip()
                            break
            except Exception:
                pass
                
        ext_version = get_extension_version()
        if project_version != ext_version:
            print("\n" + "!" * 80)
            print(f"⚠️  [WARNING] LDA Version Mismatch Detected!")
            print(f"   * This project was scaffolded with LDA version: {project_version}")
            print(f"   * Your active globally linked extension version is: {ext_version}")
            print("\n   👉 RECOMMENDED ACTION: Please run '/lda:project-upgrade' to safely")
            print("      upgrade your project workspace to the latest version!")
            print("!" * 80 + "\n")
        else:
            print(f"LDA Version Check: Project is up-to-date with active extension (version {ext_version}).")
        sys.exit(0)
        
    # 1. Resolve host
    if args.mode == 'init':
        host = args.host
        if not host:
            print("Error: --host parameter is required for init mode.")
            sys.exit(1)
            
        # Ensure it always starts with https:// (No HTTP allowed, HTTPS by default)
        if host.startswith('http://'):
            host = host.replace('http://', 'https://')
        elif not host.startswith('https://'):
            host = "https://" + host
    else: # activate
        host = get_meta_url()
        
        # Ensure activate mode URL is also upgraded/resolved with https:// by default
        if host.startswith('http://'):
            host = host.replace('http://', 'https://')
        elif not host.startswith('https://'):
            host = "https://" + host
        
    # 2. Enable LPD-63311 MCP Server Feature Flag
    enable_mcp_flag()
    
    # 3. Parse Portal Ext for Admin Credentials
    admin_email, admin_password = parse_portal_ext()
    print(f"Resolved default admin credentials: {admin_email}")
    
    # 4. Scaffold Folders (Created inside ./liferay so they are version-controlled and shared)
    os.makedirs('./liferay/specs/objects', exist_ok=True)
    os.makedirs('./liferay/specs/fragments', exist_ok=True)
    os.makedirs('./liferay/specs/client-extensions', exist_ok=True)
    os.makedirs('./liferay/specs/stylebooks', exist_ok=True)
    os.makedirs('./liferay/specs/pages', exist_ok=True)
    os.makedirs('./liferay/input', exist_ok=True)
    create_demo_plan()
    
    # 5. Git Exclusions Setup
    ai_exclusions = [
        "# AI & Agent Workspace Configurations",
        ".env",
        "scripts/",
        "dist/",
        ".claude/",
        ".cursor/",
        ".gemini/",
        ".github/",
        ".windsurf/",
        ".workspace-rules/"
    ]
    
    # Only update ./liferay/.gitignore, as the root directory is not versioned
    update_gitignore('./liferay/.gitignore', ai_exclusions)
    
    # 6. Generate local .env File
    env_path = './.env'
    env_content = [
        f"LIFERAY_HOST={host}\n",
        f"LIFERAY_ADMIN_EMAIL_ADDRESS={admin_email}\n",
        f"LIFERAY_ADMIN_PASSWORD={admin_password}\n"
    ]
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(env_content)
    print(f"Successfully generated/updated local configuration file {env_path}")
    
    # 7. Generate local lda.properties File
    lda_prop_path = './lda.properties'
    lda_version = args.lda_version or get_extension_version()
    lda_prop_content = [
        "# Liferay Demo Agent (LDA) Workspace Properties\n",
        f"lda.version={lda_version}\n"
    ]
    with open(lda_prop_path, 'w', encoding='utf-8') as f:
        f.writelines(lda_prop_content)
    print(f"Successfully generated/updated local configuration file {lda_prop_path}")
    
    print("Workspace Scaffolding and Scaffolding Orchestration Complete!")

if __name__ == '__main__':
    main()
