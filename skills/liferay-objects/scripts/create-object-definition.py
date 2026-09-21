#!/usr/bin/env python3
import os
import sys
import json
import argparse
import urllib.request
import urllib.error

# Append scripts directory to path to ensure env_utils import succeeds
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from scripts import env_utils

def make_request(url, payload=None, method='POST', headers=None):
    """Helper to perform urllib JSON requests using pre-authorized session headers."""
    req_headers = {
        'Accept': 'application/json',
    }
    # Inherit secure session headers from env_utils
    if headers:
        req_headers.update(headers)
    
    data_bytes = None
    if payload is not None:
        req_headers['Content-Type'] = 'application/json'
        data_bytes = json.dumps(payload).encode('utf-8')
    elif method in ('POST', 'PUT'):
        data_bytes = b''

    req = urllib.request.Request(url, data=data_bytes, headers=req_headers, method=method)
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
    parser = argparse.ArgumentParser(description="Create and publish a Liferay Object Definition.")
    parser.add_argument("payload_path", type=str, help="Path to the object-definition.json payload")
    parser.add_argument("--host", help="Override Liferay host URL")
    
    args = parser.parse_args()
    
    # Resolve host
    host = args.host or env_utils.get_host()
    if not host:
        print("Error: Missing target host.")
        sys.exit(1)
        
    host = host.rstrip('/')
    
    # Check payload file
    if not os.path.exists(args.payload_path):
        print(f"Error: Payload file missing at {args.payload_path}")
        sys.exit(1)
        
    with open(args.payload_path, "r", encoding="utf-8") as f:
        try:
            payload = json.load(f)
        except Exception as e:
            print(f"Error: Failed to parse JSON payload ({e})")
            sys.exit(1)
            
    # Retrieve secure, pre-authorized session headers (Completely shields password!)
    auth_headers = env_utils.get_auth_headers()
    
    print(f"Connecting to Liferay instance at {host}...")
    
    # 1. Create the Object Definition
    create_url = f"{host}/o/object-admin/v1.0/object-definitions"
    print(f"Submitting Object Definition creation request for: {payload.get('name', 'Unnamed Object')}")
    
    code, res = make_request(create_url, payload=payload, method='POST', headers=auth_headers)
    
    if code in (200, 201):
        definition_id = res.get("id")
        print(f"[SUCCESS] Object Definition created! ID: {definition_id}")
    elif code == 409: # Conflict - Object already exists
        print(f"[INFO] Object already exists (Conflict 409). Attempting to resolve details...")
        
        # Search URL
        search_url = f"{host}/o/object-admin/v1.0/object-definitions"
        search_code, search_res = make_request(search_url, method='GET', headers=auth_headers)
        definition_id = None
        if search_code == 200:
            for item in search_res.get("items", []):
                if item.get("name") == payload.get("name") or item.get("externalReferenceCode") == payload.get("externalReferenceCode"):
                    definition_id = item.get("id")
                    print(f"Found existing Object Definition ID: {definition_id}")
                    break
        if not definition_id:
            print("Error: Conflict detected but could not resolve existing definition ID.")
            sys.exit(1)
    else:
        print(f"Error: Failed to create Object Definition. HTTP {code}: {res.get('title', 'Unknown error')}")
        sys.exit(1)
        
    # 2. Publish the Object Definition
    publish_url = f"{host}/o/object-admin/v1.0/object-definitions/{definition_id}/publish"
    print(f"Publishing Object Definition (ID: {definition_id})...")
    
    pub_code, pub_res = make_request(publish_url, method='POST', headers=auth_headers)
    
    if pub_code in (200, 202):
         print("[SUCCESS] Object Definition published and synchronized successfully!")
    elif pub_code == 409:
         print("[INFO] Object Definition is already published.")
    else:
         print(f"Error: Failed to publish Object Definition. HTTP {pub_code}: {pub_res.get('title', 'Unknown error')}")
         sys.exit(1)

if __name__ == "__main__":
    main()
