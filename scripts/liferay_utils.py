import os
import sys

def get_env_path():
    """
    Finds the .env file by searching upwards from the current directory.
    This ensures sub-agents in nested folders can always find the root config.
    """
    current_dir = os.getcwd()
    while current_dir != os.path.dirname(current_dir): # Stop at filesystem root
        env_path = os.path.join(current_dir, '.env')
        if os.path.exists(env_path):
            return env_path
        current_dir = os.path.dirname(current_dir)
    return None

def get_credentials():
    """
    Parses the .env file and returns (email, password, host).
    """
    env_path = get_env_path()
    if not env_path:
        print("Error: .env file not found in project root or any parent directory.")
        sys.exit(1)
        
    creds = {}
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                creds[key.strip()] = value.strip()
                
    email = creds.get("LIFERAY_ADMIN_EMAIL_ADDRESS")
    password = creds.get("LIFERAY_ADMIN_PASSWORD")
    
    # Read Liferay local/remote host from .env, fallback to standard LDM localhost
    host = creds.get("LIFERAY_HOST")
    if not host:
        host = "https://localhost"
    
    if not email or not password:
        print(f"Error: Credentials missing in {env_path}")
        sys.exit(1)
        
    return email, password, host

if __name__ == "__main__":
    # Test output (safe keys only)
    email, _, host = get_credentials()
    print(f"Found credentials for {email} targeting {host}")
