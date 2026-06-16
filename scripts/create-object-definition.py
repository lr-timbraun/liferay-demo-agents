import os
import sys
import requests
import json
# Import standard credential utility
sys.path.append(os.path.dirname(__file__))
from liferay_utils import get_credentials

def create_and_publish_object(payload):
    email, password, host = get_credentials()
    auth = (email, password)
    
    # 1. Create Definition
    create_url = f"{host}/o/object-admin/v1.0/object-definitions"
    print(f"Creating object definition at {create_url}...")
    
    try:
        response = requests.post(create_url, auth=auth, json=payload)
        response.raise_for_status()
        
        obj_def = response.json()
        obj_id = obj_def.get("id")
        print(f"Successfully created Object: {obj_def.get('name')} (ID: {obj_id})")
        
        # 2. Publish Definition
        publish_url = f"{host}/o/object-admin/v1.0/object-definitions/{obj_id}/publish"
        print(f"Publishing object (ID: {obj_id})...")
        
        pub_response = requests.post(publish_url, auth=auth)
        pub_response.raise_for_status()
        
        print("Object published successfully.")
        
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Liferay: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create-object-definition.py <path_to_payload_json>")
        sys.exit(1)
        
    payload_path = sys.argv[1]
    if not os.path.exists(payload_path):
        print(f"Error: Payload file {payload_path} not found.")
        sys.exit(1)
        
    with open(payload_path, 'r', encoding='utf-8') as f:
        payload = json.load(f)
        
    create_and_publish_object(payload)
