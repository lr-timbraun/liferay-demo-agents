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

# Add scripts directory to path to ensure env_utils import succeeds
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import env_utils

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
    parser.add_argument('--default-email', help="Default administrator email address")
    parser.add_argument('--default-password', help="Default administrator password")
    parser.add_argument('--agent-email', default="shirley.temple@liferay.com", help="AI Agent admin email address")
    parser.add_argument('--agent-password', help="AI Agent secure password (generated automatically if omitted)")
    
    args = parser.parse_args()
    
    # Resolve host and default credentials using env_utils
    host = args.host or env_utils.get_host()
            
    # Always ensure it is https:// (No HTTP allowed, HTTPS by default)
    if host.startswith('http://'):
        host = host.replace('http://', 'https://')
    elif not host.startswith('https://'):
        host = "https://" + host
            
    host = host.rstrip('/')
    
    default_email = args.default_email or env_utils.get_admin_email()
    default_password = args.default_password or env_utils.get_admin_password()
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
        if code in (200, 201):
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

    # 7. Overwrite/update local .env file
    env_path = env_utils.get_env_path() or './.env'
    print(f"Saving agent admin credentials to {env_path}...")
    
    # Read existing env and rewrite with new agent credentials
    env_lines = []
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line_stripped = line.strip()
                if line_stripped.startswith('LIFERAY_ADMIN_EMAIL_ADDRESS='):
                    env_lines.append(f"LIFERAY_ADMIN_EMAIL_ADDRESS={agent_email}" + os.linesep)
                elif line_stripped.startswith('LIFERAY_ADMIN_PASSWORD='):
                    env_lines.append(f"LIFERAY_ADMIN_PASSWORD={agent_password}" + os.linesep)
                else:
                    env_lines.append(line)
    else:
        env_lines = [
            f"LIFERAY_HOST={host}" + os.linesep,
            f"LIFERAY_ADMIN_EMAIL_ADDRESS={agent_email}" + os.linesep,
            f"LIFERAY_ADMIN_PASSWORD={agent_password}" + os.linesep
        ]
        
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(env_lines)
    print("Credentials saved successfully.")

    # 8. Verify the Liferay API Proxy MCP Server is active and communicating over JSON-RPC stdio
    import subprocess
    print("Verifying Liferay API Proxy MCP Server is active and available...")
    
    extension_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_path = os.path.join(extension_dir, 'index.js')
    
    if not os.path.exists(index_path):
        print(f"Error: MCP Proxy script not found at {index_path}")
        sys.exit(1)
        
    # Build environment containing WORKSPACE_PATH set to active CWD
    env = os.environ.copy()
    env['WORKSPACE_PATH'] = os.getcwd()
    env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0'
    
    try:
        proc = subprocess.Popen(
            ['node', index_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        
        # A. Send standard MCP 'initialize' JSON-RPC message
        init_req = json.dumps({
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "scaffold-verifier", "version": "1.0.0"}
            },
            "id": 1
        }) + "\n"
        
        proc.stdin.write(init_req)
        proc.stdin.flush()
        
        init_res_line = proc.stdout.readline()
        init_res = json.loads(init_res_line)
        
        if 'error' in init_res:
            print(f"Error: MCP Proxy initialization failed: {init_res['error'].get('message')}")
            sys.exit(1)
            
        # B. Send standard MCP 'tools/call' JSON-RPC message to execute 'liferay_get_openapis'
        call_req = json.dumps({
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "liferay_get_openapis",
                "arguments": {}
            },
            "id": 2
        }) + "\n"
        
        proc.stdin.write(call_req)
        proc.stdin.flush()
        
        call_res_line = proc.stdout.readline()
        call_res = json.loads(call_res_line)
        
        # Close the subprocess cleanly
        proc.terminate()
        
        if 'error' in call_res:
            print(f"Error: MCP Proxy failed to execute tool: {call_res['error'].get('message')}")
            sys.exit(1)
            
        # Parse the content returned by 'liferay_get_openapis'
        content = call_res.get('result', {}).get('content', [])
        if content and content[0].get('type') == 'text':
            text_val = content[0].get('text', '')
            # A successful response from the proxy includes standard OpenAPI categories/links
            if "headless-delivery" in text_val or "headless-admin-user" in text_val or "services" in text_val:
                print("Liferay API Proxy verification successful! Proxy is active, authenticated, and communicating.")
                print("AI Agent Admin Provisioning Complete!")
                return
                
        print("Error: MCP Proxy returned an unexpected response schema during verification.")
        sys.exit(1)
        
    except Exception as e:
        print(f"Error: Failed to verify connection via MCP Proxy: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
