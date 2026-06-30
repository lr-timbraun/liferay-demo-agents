#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil

def get_workspace_dir():
    """Returns the main project root directory."""
    return os.getcwd()

def get_client_extensions_dir():
    """Locates the liferay/client-extensions folder in the workspace."""
    cwd = get_workspace_dir()
    cx_path = os.path.join(cwd, 'liferay', 'client-extensions')
    if os.path.exists(cx_path):
        return cx_path
    return None

def find_gradle_built_zip(project_path):
    """Searches the project's dist/ directory for Gradle-built client-extension ZIP files."""
    dist_dir = os.path.join(project_path, 'dist')
    if not os.path.exists(dist_dir):
        return None
        
    for root, _, files in os.walk(dist_dir):
        for file in files:
            if file.endswith('.zip'):
                return os.path.join(root, file)
    return None

def main():
    print("====================================================")
    print("     Liferay Client Extensions Deployer Script      ")
    print("====================================================")
    
    workspace_dir = get_workspace_dir()
    cx_dir = get_client_extensions_dir()
    if not cx_dir:
        print("Error: Could not find 'liferay/client-extensions/' directory. Please run this from the project root.")
        sys.exit(1)
        
    # 1. Scan custom client extensions
    projects = [d for d in os.listdir(cx_dir) if os.path.isdir(os.path.join(cx_dir, d)) and os.path.exists(os.path.join(cx_dir, d, 'client-extension.yaml'))]
    if not projects:
        print("No custom client extensions found under 'liferay/client-extensions/'.")
        sys.exit(0)
        
    print(f"Found {len(projects)} client extension(s): {', '.join(projects)}")
    
    # 2. Trigger Gradle clean build inside the Liferay Workspace
    print("\n--- Triggering Liferay Workspace Gradle Build ---")
    liferay_dir = os.path.join(workspace_dir, 'liferay')
    gradle_cmd = 'gradlew.bat' if sys.platform == 'win32' else './gradlew'
    
    if not os.path.exists(os.path.join(liferay_dir, gradle_cmd)):
        # Fallback to general gradlew
        gradle_cmd = 'gradlew'
        
    try:
        use_shell = sys.platform == 'win32'
        print(f"Executing: {gradle_cmd} clean build inside {os.path.relpath(liferay_dir)}")
        subprocess.run([gradle_cmd, 'clean', 'build'], cwd=liferay_dir, shell=use_shell, check=True)
        print("Liferay Workspace Gradle Build completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌  [ERROR] Liferay Workspace Gradle Build failed: {e}")
        print("Aborting hot-deploy to prevent deploying incomplete/broken assets.")
        sys.exit(1)
        
    # 3. Locate built ZIP files and copy them to LDM hot-deploy directory
    print("\n--- Copying Gradle-Built Archives to LDM Hot-Deploy Path ---")
    ldm_cx_dir = os.path.join(workspace_dir, 'client-extensions')
    os.makedirs(ldm_cx_dir, exist_ok=True)
    
    deploy_count = 0
    for project in projects:
        project_path = os.path.join(cx_dir, project)
        built_zip = find_gradle_built_zip(project_path)
        
        if built_zip:
            dest_zip = os.path.join(ldm_cx_dir, f"{project}.zip")
            print(f"  * Copying {os.path.relpath(built_zip)} -> {os.path.relpath(dest_zip)}...")
            shutil.copy2(built_zip, dest_zip)
            deploy_count += 1
        else:
            print(f"⚠️  [WARNING] Could not find any Gradle-built ZIP output inside {project_path}/build/")
            
    if deploy_count == 0:
        print("\n❌  [ERROR] No compiled client extension ZIP files were found to deploy.")
        sys.exit(1)
        
    # 4. Trigger LDM Deploy to sync and refresh the active stack
    print("\n--- Triggering LDM Deploy to Sync and Refresh Stack ---")
    try:
        use_shell = sys.platform == 'win32'
        subprocess.run(['ldm', 'deploy'], shell=use_shell, check=True)
        print("\nAll Liferay Client Extensions deployed and synchronized successfully!")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"\n❌  [ERROR] LDM Deploy command failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
