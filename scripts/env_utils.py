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

def read_env_variable(key_name, default_value=None, required=False):
    """
    Helper to read a single specific variable from the .env file on-demand.
    """
    env_path = get_env_path()
    if not env_path:
        print("Error: .env file not found in project root or any parent directory.")
        sys.exit(1)
        
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                if key.strip() == key_name:
                    return value.strip()
                    
    if required:
        print(f"Error: Mandatory configuration key '{key_name}' missing in {env_path}")
        sys.exit(1)
        
    return default_value

def get_host():
    """
    Parses .env and returns the LIFERAY_HOST value on-demand, defaulting to standard LDM https://localhost.
    """
    return read_env_variable("LIFERAY_HOST", default_value="https://localhost")

def get_admin_email():
    """
    Parses .env and returns the LIFERAY_ADMIN_EMAIL_ADDRESS on-demand.
    """
    return read_env_variable("LIFERAY_ADMIN_EMAIL_ADDRESS", required=True)

def get_admin_password():
    """
    Parses .env and returns the LIFERAY_ADMIN_PASSWORD on-demand.
    """
    return read_env_variable("LIFERAY_ADMIN_PASSWORD", required=True)

if __name__ == "__main__":
    # Test output (safe keys only)
    host = get_host()
    email = get_admin_email()
    print(f"Verified connection configuration for {email} targeting {host}")
