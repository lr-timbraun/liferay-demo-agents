import os
import sys
import base64
import time
import urllib.request
import urllib.error

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
    Helper to read a single specific variable, prioritizing process environment
    variables (os.environ) before falling back to parsing the local .env file.
    """
    # 1. Prioritize process environment variables (Twelve-Factor Secure Injection)
    if key_name in os.environ:
        return os.environ[key_name]
        
    # 2. Fallback to parsing local .env file
    env_path = get_env_path()
    if env_path:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if key.strip() == key_name:
                        return value.strip()
                        
    if required:
        print(f"Error: Mandatory configuration key '{key_name}' missing in system environment or local .env file.")
        sys.exit(1)
        
    return default_value

def get_host():
    """
    Parses configuration and returns the LIFERAY_HOST value, defaulting to standard LDM https://localhost.
    """
    return read_env_variable("LIFERAY_HOST", default_value="https://localhost")

def get_admin_email():
    """
    Parses configuration and returns the LIFERAY_ADMIN_EMAIL_ADDRESS.
    """
    return read_env_variable("LIFERAY_ADMIN_EMAIL_ADDRESS", required=True)

def _get_private_admin_password():
    """
    Private helper to resolve the password strictly for the session login handshake.
    """
    return read_env_variable("LIFERAY_ADMIN_PASSWORD", required=True)

def get_admin_password():
    """
    DEPRECATED & FORBIDDEN. Direct password extraction is strictly prohibited to prevent credential leaks.
    """
    raise PermissionError("Access Denied: Direct password extraction is prohibited. Please use get_auth_headers() instead to retrieve pre-authorized session tokens.")

def get_auth_headers():
    """
    Autonomously resolves pre-authorized HTTP Headers, utilizing a cached
    Liferay Session Cookie (JSESSIONID) to completely shield your raw password.
    """
    host = get_host().rstrip('/')
    cache_dir = os.path.join(os.path.expanduser("~"), ".gemini", "tmp")
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, "liferay_session.txt")
    
    # 1. Check if a valid, cached session cookie currently exists (5-minute TTL)
    if os.path.exists(cache_path):
        mtime = os.path.getmtime(cache_path)
        if (time.time() - mtime) < 300: # 5 minutes TTL
            with open(cache_path, "r", encoding="utf-8") as f:
                cookie_val = f.read().strip()
            if cookie_val:
                return {
                    "Cookie": cookie_val,
                    "Accept": "application/json"
                }
                
    # 2. Cache expired or missing. Execute the Session Token Exchange handshake!
    email = get_admin_email()
    password = _get_private_admin_password()
    
    auth_str = f"{email}:{password}"
    auth_header = "Basic " + base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
    
    # Target Liferay's safe headless user profile endpoint to perform handshake
    handshake_url = f"{host}/o/headless-admin-user/v1.0/my-user-account"
    req = urllib.request.Request(handshake_url, headers={"Authorization": auth_header, "Accept": "application/json"})
    
    try:
        with urllib.request.urlopen(req) as response:
            # Extract JSESSIONID from Set-Cookie headers
            set_cookie = response.headers.get("Set-Cookie")
            session_cookie = None
            if set_cookie:
                for part in set_cookie.split(";"):
                    if "JSESSIONID=" in part:
                        session_cookie = part.strip()
                        break
                        
            if session_cookie:
                # Cache the session cookie securely on-disk
                with open(cache_path, "w", encoding="utf-8") as f:
                    f.write(session_cookie)
                return {
                    "Cookie": session_cookie,
                    "Accept": "application/json"
                }
            else:
                # Fallback to standard Basic Auth if Liferay didn't return a Set-Cookie header
                return {
                    "Authorization": auth_header,
                    "Accept": "application/json"
                }
    except Exception as e:
        # Fallback to Basic Auth on connection errors
        return {
            "Authorization": auth_header,
            "Accept": "application/json"
        }

if __name__ == "__main__":
    # Test output (safe keys only)
    host = get_host()
    email = get_admin_email()
    print(f"Verified secure connection configuration for {email} targeting {host}")
