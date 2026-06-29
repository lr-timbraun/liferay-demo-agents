#!/usr/bin/env python3
import os
import sys
import json
import base64
import argparse
import secrets
import string
import urllib.request
import urllib.error

def get_env_path():
    """Finds the .env file by searching upwards from the current directory."""
    current_dir = os.path.abspath(os.getcwd())
    while current_dir != os.path.dirname(current_dir):
        env_path = os.path.join(current_dir, '.env')
        if os.path.exists(env_path):
            return env_path
        current_dir = os.path.dirname(current_dir)
    return os.path.join(os.path.abspath(os.getcwd()), '.env')

def generate_secure_password(length=16):
    """Generates a secure password containing uppercase, lowercase, digits, and punctuation."""
    alphabet = string.ascii_letters + string.digits + "!@#$%"
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in "!@#$%" for c in password)):
            return password

def make_request(url, payload=None, method='GET', auth_header=None):
    """Helper to perform standard urllib JSON requests."""
    headers = {
        'Accept': 'application/json',
    }
    if auth_header:
        headers['Authorization'] = auth_header
    
    data_bytes = None
    if payload is not None:
        headers['Content-Type'] = 'application/json'
        data_bytes = json.dumps(payload).encode('utf-8')
    elif method == 'POST':
        data_bytes = b''

    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            status = response.status
            body = response.read().decode('utf-8')
            return status, json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        try:
            err_json = json.loads(body)
        except Exception:
            err_json = {"title": body}
        return e.code, err_json
    except Exception as e:
        return 500, {"title": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Provision a dedicated Liferay administrator account for AI Agent use.")
    parser.add_argument('--host', help="Liferay host URL (e.g. https://localhost)")
    parser.add_argument('--default-email', required=True, help="Default administrator email address")
    parser.add_argument('--default-password', required=True, help="Default administrator password")
    parser.add_argument('--agent-email', default="shirley.temple@liferay.com", help="AI Agent admin email address")
    parser.add_argument('--agent-password', help="AI Agent secure password (generated automatically if omitted)")
    
    args = parser.parse_args()
    
    host = args.host
    if not host:
        # Fallback to reading host from .env
        env_path = get_env_path()
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip().startswith('LIFERAY_HOST='):
                        host = line.strip().split('=', 1)[1].strip()
                        break
        if not host:
            print("Error: LIFERAY_HOST is not defined in .env and no --host was provided.")
            sys.exit(1)
            
    # Always ensure it is https:// (No HTTP allowed, HTTPS by default)
    if host.startswith('http://'):
        host = host.replace('http://', 'https://')
    elif not host.startswith('https://'):
        host = "https://" + host
            
    host = host.rstrip('/')
    default_email = args.default_email
    default_password = args.default_password
    agent_email = args.agent_email
    
    agent_password = args.agent_password
    if not agent_password:
        agent_password = generate_secure_password()
        
    # Construct Basic Auth header for default credentials
    default_auth_str = f"{default_email}:{default_password}"
    default_auth_header = "Basic " + base64.b64encode(default_auth_str.encode('utf-8')).decode('utf-8')
    
    print(f"Connecting to Liferay instance at {host} using default credentials...")
    
    # 1. Test connectivity & authentication
    conn_url = f"{host}/o/headless-admin-user/v1.0/my-user-account"
    code, res = make_request(conn_url, auth_header=default_auth_header)
    if code != 200:
        print(f"Error: Unable to authenticate with default credentials. HTTP {code}: {res.get('title', 'Unknown error')}")
        sys.exit(1)
    print("Authentication with default administrator successful.")

    # 2. Search if the agent user already exists
    user_id = None
    search_url = f"{host}/o/headless-admin-user/v1.0/user-accounts?search=shirley"
    code, res = make_request(search_url, auth_header=default_auth_header)
    if code == 200:
        items = res.get('items', [])
        for item in items:
            if item.get('emailAddress') == agent_email:
                user_id = item.get('id')
                print(f"Found existing AI Agent user account '{agent_email}' with ID: {user_id}")
                break

    # 3. Create the agent user if they don't exist
    if not user_id:
        print(f"Creating dedicated agent administrator user '{agent_email}'...")
        create_url = f"{host}/o/headless-admin-user/v1.0/user-accounts"
        payload = {
            "alternateName": "shirley",
            "emailAddress": agent_email,
            "familyName": "Temple",
            "givenName": "Shirley",
            "password": agent_password
        }
        code, res = make_request(create_url, payload=payload, method='POST', auth_header=default_auth_header)
        if code == 201:
            user_id = res.get('id')
            print(f"Agent user created successfully! User ID: {user_id}")
        elif code == 409: # Conflict
            print("Conflict: A user with this alternate name or email already exists. Searching again...")
            code, res = make_request(search_url, auth_header=default_auth_header)
            if code == 200:
                for item in res.get('items', []):
                    if item.get('emailAddress') == agent_email:
                        user_id = item.get('id')
                        print(f"Resolved existing user ID: {user_id}")
                        break
            if not user_id:
                print("Error: Conflict detected but could not resolve existing user ID.")
                sys.exit(1)
        else:
            print(f"Error: Failed to create user account. HTTP {code}: {res.get('title', 'Unknown error')}")
            sys.exit(1)

    # 4. Resolve the 'Administrator' Role ID
    print("Resolving 'Administrator' role ID...")
    role_url = f"{host}/o/headless-admin-user/v1.0/roles?search=Administrator"
    code, res = make_request(role_url, auth_header=default_auth_header)
    admin_role_id = None
    if code == 200:
        for item in res.get('items', []):
            if item.get('name') == 'Administrator':
                admin_role_id = item.get('id')
                break
                
    if not admin_role_id:
        print("Error: Could not resolve 'Administrator' role ID dynamically.")
        sys.exit(1)
    print(f"Resolved 'Administrator' role ID: {admin_role_id}")

    # 5. Associate Administrator Role with User
    print(f"Assigning 'Administrator' role to agent user (ID {user_id})...")
    assoc_url = f"{host}/o/headless-admin-user/v1.0/roles/{admin_role_id}/association/user-account/{user_id}"
    code, res = make_request(assoc_url, method='POST', auth_header=default_auth_header)
    if code not in (200, 204):
        print(f"Error: Failed to assign role to agent user. HTTP {code}: {res.get('title', 'Unknown error')}")
        sys.exit(1)
    print("Role assigned successfully.")

    # 6. Verify Shirley Temple account works on the MCP Server endpoint
    print("Verifying newly created Shirley Temple account works on Liferay...")
    agent_auth_str = f"{agent_email}:{agent_password}"
    agent_auth_header = "Basic " + base64.b64encode(agent_auth_str.encode('utf-8')).decode('utf-8')
    
    code, res = make_request(conn_url, auth_header=agent_auth_header)
    if code != 200:
        print(f"Error: New Shirley Temple account failed verification. HTTP {code}: {res.get('title', 'Unknown error')}")
        sys.exit(1)
    print("Verification successful! Dedicated agent admin account is functional.")

    # 6b. Verify Liferay MCP Server is available
    print("Verifying Liferay MCP Server is active and available at /o/mcp...")
    mcp_url = f"{host}/o/mcp"
    mcp_code, mcp_res = make_request(mcp_url, auth_header=agent_auth_header)
    
    # Standard Liferay MCP Server returns HTTP 400 when GET requested without SSE headers,
    # or HTTP 200/204 when active. Any code in (200, 204, 400) proves the servlet is listening!
    if mcp_code not in (200, 204, 400):
        print(f"Error: Liferay MCP Server is NOT active at /o/mcp (HTTP {mcp_code}).")
        print("  👉 Please verify that 'feature.flag.LPD-63311=true' is set in 'files/portal-ext.properties'!")
        sys.exit(1)
    print("Liferay MCP Server verification successful! Server is responsive and listening.")

    # 7. Overwrite/update local .env file
    env_path = get_env_path()
    print(f"Saving agent admin credentials to {env_path}...")
    
    # Read existing env and rewrite with new agent credentials
    env_lines = []
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line_stripped = line.strip()
                if line_stripped.startswith('LIFERAY_ADMIN_EMAIL_ADDRESS='):
                    env_lines.append(f"LIFERAY_ADMIN_EMAIL_ADDRESS={agent_email}\n")
                elif line_stripped.startswith('LIFERAY_ADMIN_PASSWORD='):
                    env_lines.append(f"LIFERAY_ADMIN_PASSWORD={agent_password}\n")
                else:
                    env_lines.append(line)
    else:
        env_lines = [
            f"LIFERAY_HOST={host}\n",
            f"LIFERAY_ADMIN_EMAIL_ADDRESS={agent_email}\n",
            f"LIFERAY_ADMIN_PASSWORD={agent_password}\n"
        ]
        
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(env_lines)
        
    print("Credentials saved successfully.")
    print("AI Agent Admin Provisioning Complete!")

if __name__ == "__main__":
    main()
