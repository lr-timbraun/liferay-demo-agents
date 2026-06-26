#!/usr/bin/env python3
import os
import sys
import json
import importlib.util

def get_extension_dir():
    """Resolves the directory path of this globally linked extension."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_extension_version(ext_dir):
    """Reads the current global extension version from gemini-extension.json."""
    ext_json_path = os.path.join(ext_dir, 'gemini-extension.json')
    if os.path.exists(ext_json_path):
        try:
            with open(ext_json_path, 'r', encoding='utf-8') as f:
                return json.load(f).get('version', '0.0.0')
        except Exception:
            pass
    return '0.0.0'

def get_project_version():
    """Reads the current local project's scaffolded version from lda.properties."""
    project_version = '0.1.0' # Default fallback for legacy scaffoldings
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
    return project_version

def update_project_properties(target_version):
    """Writes the upgraded version into lda.properties at the project root."""
    lda_prop_path = './lda.properties'
    content = [
        "# Liferay Demo Agent (LDA) Workspace Properties\n",
        f"lda.version={target_version}\n"
    ]
    with open(lda_prop_path, 'w', encoding='utf-8') as f:
        f.writelines(content)
    print(f"  * Updated local lda.properties with version: {target_version}")

def main():
    print("====================================================")
    print("        Liferay Demo Agents Project Upgrader        ")
    print("====================================================")
    
    # 1. Resolve extension and project directories
    ext_dir = get_extension_dir()
    project_dir = os.getcwd()
    
    # 2. Extract versions
    ext_version = get_extension_version(ext_dir)
    project_version = get_project_version()
    
    print(f"Active Extension Version: {ext_version}")
    print(f"Current Project Version:   {project_version}")
    
    if project_version == ext_version:
        print("\nYour project workspace is already up-to-date with the latest version!")
        sys.exit(0)
        
    # 3. Define the sequential upgrade path
    # E.g. key represents (source_version, target_version) and value represents the upgrade script name
    upgrade_path = [
        ("0.1.0", "0.1.1", "upgrade_0_1_0_to_0_1_1.py"),
        ("0.1.1", "0.2.0", "upgrade_0_1_1_to_0_2_0.py")
    ]
    
    # Find all steps needed to migrate from project_version to ext_version
    steps_to_run = []
    current = project_version
    
    # Extensible sequential path finder
    while current != ext_version:
        step_found = False
        for src, dest, script_name in upgrade_path:
            if src == current:
                steps_to_run.append((src, dest, script_name))
                current = dest
                step_found = True
                break
        if not step_found:
            print(f"\nError: No upgrade path defined to migrate from version {current} to {ext_version}.")
            sys.exit(1)
            
    print(f"\nFound {len(steps_to_run)} upgrade step(s) to apply:")
    for src, dest, _ in steps_to_run:
        print(f"  * Upgrade {src} -> {dest}")
        
    print("\nStarting upgrade execution...")
    for src, dest, script_name in steps_to_run:
        script_path = os.path.join(ext_dir, "upgrades", script_name)
        if not os.path.exists(script_path):
            print(f"Error: Upgrade script {script_path} not found inside extension.")
            sys.exit(1)
            
        try:
            # Dynamically load and run the upgrade script
            spec = importlib.util.spec_from_file_location("upgrade_step", script_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Execute step
            success = module.run_upgrade(ext_dir, project_dir)
            if not success:
                print(f"\nError: Upgrade step {src} -> {dest} failed.")
                sys.exit(1)
                
            # Update local lda.properties to mark successful completion of this step
            update_project_properties(dest)
            
        except Exception as e:
            print(f"\nError executing upgrade script {script_name}: {e}")
            sys.exit(1)
            
    print("\n====================================================")
    print(f"🎉 Project successfully upgraded to LDA version {ext_version}!")
    print("====================================================")

if __name__ == '__main__':
    main()
