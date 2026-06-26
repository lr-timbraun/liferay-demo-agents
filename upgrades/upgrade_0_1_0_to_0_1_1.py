import os
import shutil

def run_upgrade(extension_dir, project_dir):
    """
    Upgrades a project from LDA 0.1.0 to 0.1.1.
    Copies the newly added deployment and utility scripts to the project's ./scripts/ folder.
    """
    print("Executing upgrade step: 0.1.0 -> 0.1.1...")
    
    # 1. We copy the missing scripts from the extension's scripts folder
    scripts_to_copy = [
        "env_utils.py",
        "deploy-client-extensions.py",
        "deploy-fragments.py",
        "deploy-stylebook.py"
    ]
    
    src_scripts_dir = os.path.join(extension_dir, "scripts")
    dest_scripts_dir = os.path.join(project_dir, "scripts")
    
    os.makedirs(dest_scripts_dir, exist_ok=True)
    
    for s in scripts_to_copy:
        src_path = os.path.join(src_scripts_dir, s)
        dest_path = os.path.join(dest_scripts_dir, s)
        
        if os.path.exists(src_path):
            print(f"  * Copying {s} -> {os.path.relpath(dest_path)}...")
            shutil.copy2(src_path, dest_path)
        else:
            print(f"  * Error: Source script {src_path} not found inside extension.")
            return False
            
    print("Successfully completed upgrade step: 0.1.0 -> 0.1.1!")
    return True
