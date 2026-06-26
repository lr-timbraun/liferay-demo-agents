import os
import json

def run_upgrade(extension_dir, project_dir):
    """
    Upgrades a project from LDA 0.1.1 to 0.2.0-dev.
    Unregisters the legacy, un-proxied 'liferay' MCP server from the local .gemini/settings.json
    since we are now natively using the statically registered liferay-api-proxy instead.
    """
    print("Executing upgrade step: 0.1.1 -> 0.2.0-dev...")
    
    settings_path = os.path.join(project_dir, ".gemini", "settings.json")
    if os.path.exists(settings_path):
        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Check if liferay is registered under mcpServers
            mcp_servers = data.get('mcpServers', {})
            if 'liferay' in mcp_servers:
                print("  * Unregistering 'liferay' MCP server from local project settings...")
                del mcp_servers['liferay']
                data['mcpServers'] = mcp_servers
                
                # Write back the cleaned settings.json
                with open(settings_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                print("  * Successfully unregistered legacy MCP server!")
            else:
                print("  * Note: Legacy 'liferay' MCP server was not registered in this project. Skipping.")
                
        except Exception as e:
            print(f"  * Warning: Failed to clean up legacy MCP server from settings.json: {e}")
            return False
    else:
        print("  * Note: No local .gemini/settings.json file found. Skipping.")
        
    print("Successfully completed upgrade step: 0.1.1 -> 0.2.0-dev!")
    return True
