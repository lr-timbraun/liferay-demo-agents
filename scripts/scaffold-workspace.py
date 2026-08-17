#!/usr/bin/env python3
import os
import sys
import json
import argparse

def parse_meta():
    """Reads `./meta` to parse and reconstruct LIFERAY_HOST, admin prefix, and admin password."""
    meta_path = './meta'
    if not os.path.exists(meta_path):
        meta_path = os.path.join(os.getcwd(), 'meta')
        
    meta = {}
    if os.path.exists(meta_path):
        with open(meta_path, 'r', encoding='utf-8') as f:
            try:
                meta = json.load(f)
            except Exception:
                # Fallback to key=value parsing if meta is not valid JSON
                f.seek(0)
                for line in f:
                    line_stripped = line.strip()
                    if line_stripped and '=' in line_stripped:
                        key, val = line_stripped.split('=', 1)
                        meta[key.strip()] = val.strip().strip('"').strip("'")
                    
    # 1. Resolve host url
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
            
    # Always upgrade to HTTPS by default
    if url.startswith('http://'):
        url = url.replace('http://', 'https://')
    elif not url.startswith('https://'):
        url = "https://" + url
        
    # 2. Resolve default admin credentials
    admin_email = 'test@liferay.com'
    admin_password = 'test'
    
    credentials = meta.get('credentials', [])
    if isinstance(credentials, list):
        for cred in credentials:
            if isinstance(cred, dict) and cred.get('type') == 'admin':
                admin_email = cred.get('email', admin_email)
                admin_password = cred.get('password', admin_password)
                break
    else:
        # Fallback to key=value resolving if credentials is not a list
        admin_prefix = meta.get('admin_prefix', 'test')
        admin_password = meta.get('admin_password', 'test')
        admin_email = f"{admin_prefix}@liferay.com"
    
    return url, admin_email, admin_password

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

def create_demo_plan(extension_dir):
    """Generates the standardized liferay/specs/DEMO_PLAN.md tracker if missing."""
    plan_path = './liferay/specs/DEMO_PLAN.md'
    if os.path.exists(plan_path):
        return
        
    template_path = os.path.join(extension_dir, 'templates', 'workspace-demo-plan.md')
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(plan_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created progress plan template {plan_path}")

def create_workspace_gemini_md(extension_dir):
    """Generates the workspace root GEMINI.md enforcing strict Orchestrator-Delegator boundaries."""
    gemini_path = './GEMINI.md'
    if os.path.exists(gemini_path):
        return
        
    template_path = os.path.join(extension_dir, 'templates', 'workspace-gemini.md')
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(gemini_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created workspace template {gemini_path}")

def get_extension_version():
    """Attempts to read the version dynamically from gemini-extension.json."""
    try:
        # __file__ is scripts/scaffold-workspace.py, so grandparent is the extension root
        extension_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(extension_dir, 'gemini-extension.json')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f).get('version', '0.0.0')
    except Exception:
        pass
    return '0.0.0'

def main():
    parser = argparse.ArgumentParser(description="LDA Workspace Scaffolding and Environment Config Orchestrator.")
    parser.add_argument('--mode', choices=['init', 'activate'], required=True, help="Orchestration mode")
    parser.add_argument('--host', help="Liferay Host URL (only required for init mode)")
    parser.add_argument('--lda-version', default=None, help="Liferay Demo Agent version")
    
    args = parser.parse_args()
    
    # 1. Resolve LDM meta configurations dynamically
    meta_url, admin_email, admin_password = parse_meta()
    
    # Resolve host based on mode
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
        host = meta_url
        
    # 2. Enable LPD-63311 MCP Server Feature Flag
    enable_mcp_flag()
    
    # 3. Print resolved administrator credentials
    print(f"Resolved default admin credentials from LDM meta: {admin_email}")
    
    # 4. Scaffold Folders (Created inside ./liferay so they are version-controlled and shared)
    os.makedirs('./liferay/specs/objects', exist_ok=True)
    os.makedirs('./liferay/specs/fragments', exist_ok=True)
    os.makedirs('./liferay/specs/client-extensions', exist_ok=True)
    os.makedirs('./liferay/specs/stylebooks', exist_ok=True)
    os.makedirs('./liferay/specs/pages', exist_ok=True)
    os.makedirs('./liferay/input', exist_ok=True)
    
    # Resolve global extension root directory
    extension_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    create_demo_plan(extension_dir)
    create_workspace_gemini_md(extension_dir)
    
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
    
    # 6. Generate local .env File (Only if missing to protect custom configurations on resume)
    env_path = './.env'
    if not os.path.exists(env_path):
        env_content = f"""LIFERAY_HOST={host}
LIFERAY_ADMIN_EMAIL_ADDRESS={admin_email}
LIFERAY_ADMIN_PASSWORD={admin_password}
"""
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print(f"Successfully generated local configuration file {env_path}")
    else:
        print(f"Local configuration file {env_path} already exists. Skipping generation to protect your active settings.")
    
    # 7. Generate local lda.properties File
    lda_prop_path = './lda.properties'
    lda_version = args.lda_version or get_extension_version()
    lda_prop_content = f"""# Liferay Demo Agent (LDA) Workspace Properties
lda.version={lda_version}
"""
    with open(lda_prop_path, 'w', encoding='utf-8') as f:
        f.write(lda_prop_content)
    print(f"Successfully generated/updated local configuration file {lda_prop_path}")
    
    print("Workspace Scaffolding and Scaffolding Orchestration Complete!")

if __name__ == '__main__':
    main()
