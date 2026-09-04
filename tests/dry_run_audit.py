#!/usr/bin/env python3
import os
import sys
import re
import py_compile

# Regex pattern matching graphical emojis/pictographs
emoji_pattern = re.compile(
    "["
    "\U0001f600-\U0001f64f"  # emoticons
    "\U0001f300-\U0001f5ff"  # symbols & pictographs
    "\U0001f680-\U0001f6ff"  # transport & map
    "\U0001f1e0-\U0001f1ff"  # flags
    "\U00002700-\U000027bf"  # dingbats
    "\U00002600-\U000026ff"  # misc symbols
    "\u2934-\u2935"          # arrows
    "\u2b05-\u2b07"
    "\u2b1b-\u2b1c"
    "\u2b50"
    "\u3297"
    "\u3299"
    "\u303d"
    "\u3030"
    "\u2b55"
    "\u2194-\u2199"
    "\u21a9-\u21aa"
    "]+", 
    flags=re.UNICODE
)

def check_for_emojis(content, file_path):
    """Verifies that no graphical emojis or pictographs are present in the file."""
    matches = emoji_pattern.findall(content)
    if matches:
        print(f"[✗] {file_path}: Found prohibited emoji(s) {set(matches)}")
        return False
    return True

def check_markdown_code_blocks(content, file_path):
    """Ensures that no Markdown file contains prohibited ```markdown or ```text code block highlights, as they cause previewer rendering bugs."""
    if "```markdown" in content:
        print(f"[✗] {file_path}: Found prohibited '```markdown' nested highlight tag (use plain empty '```' block instead to prevent previewer styling failures)")
        return False
    if "```text" in content:
        print(f"[✗] {file_path}: Found prohibited '```text' nested highlight tag (use plain empty '```' block instead to prevent previewer styling failures)")
        return False
    return True

def log_header(title):
    print("\n" + "="*80)
    print(f" {title.upper()} ")
    print("="*80)

def parse_front_matter(content):
    """Simple parser for YAML front matter without external yaml library dependency."""
    parts = content.split("---")
    if len(parts) < 3:
        return None
    meta = {}
    for line in parts[1].splitlines():
        line = line.strip()
        if line and ":" in line:
            key, val = line.split(":", 1)
            meta[key.strip()] = val.strip().strip('"').strip("'")
    return meta

def audit_agents():
    log_header("Auditing Agent Definitions")
    agents = [
        {"name": "Conductor", "file": "templates/GEMINI.template.md", "is_orchestrator": True},
        {"name": "Site Copy", "file": "agents/site-copy-agent.md"},
        {"name": "Site Design", "file": "agents/site-design-agent.md"},
        {"name": "Fragment", "file": "agents/fragment-agent.md"},
        {"name": "Object", "file": "agents/object-agent.md"},
        {"name": "Custom Element", "file": "agents/custom-element-agent.md"},
        {"name": "Commerce", "file": "agents/commerce-agent.md"},
        {"name": "Microservice", "file": "agents/microservice-agent.md"},
        {"name": "Content", "file": "agents/content-agent.md"},
        {"name": "Workflow", "file": "agents/workflow-agent.md"},
        {"name": "Administration", "file": "agents/administration-agent.md"},
    ]
    
    passed = 0
    failed = 0
    
    for agent in agents:
        fpath = agent["file"]
        if not os.path.exists(fpath):
            print(f"[✗] {agent['name']}: File missing ({fpath})")
            failed += 1
            continue
            
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Prohibit Emojis Check
        if not check_for_emojis(content, fpath):
            failed += 1
            continue
            
        # Prohibit Nested Markdown Code Block Highlight Checks
        if not check_markdown_code_blocks(content, fpath):
            failed += 1
            continue
            
        # Parse front matter for sub-agents
        if not agent.get("is_orchestrator"):
            meta = parse_front_matter(content)
            if meta is None:
                print(f"[✗] {agent['name']}: Missing YAML front matter boundaries")
                failed += 1
                continue
            if "name" not in meta or "description" not in meta:
                print(f"[✗] {agent['name']}: Front matter must contain 'name' and 'description'")
                failed += 1
                continue
                
        # Structural Section Checks (only for sub-agents)
        if not agent.get("is_orchestrator"):
            required_headers = [
                "Core Mindset",
                "Isolation Mandate",
                "Delivery Mandate",
                "Responsibilities",
                "Implementation Standard",
                "Strict Grounded Execution"
            ]
            
            missing_headers = []
            for header in required_headers:
                if header not in content:
                    missing_headers.append(header)
                    
            if missing_headers:
                print(f"[✗] {agent['name']}: Missing sections: {', '.join(missing_headers)}")
                failed += 1
            else:
                print(f"[✓] {agent['name']}: Validated successfully")
                passed += 1
        else:
            print(f"[✓] {agent['name']}: Validated successfully (Orchestrator)")
            passed += 1
            
    print(f"\nAgents Validation Results: {passed} Passed, {failed} Failed")
    return failed == 0

def audit_skills():
    log_header("Auditing Skill Declarations")
    skills = [
        # Group A
        {"name": "browser-use", "dir": "skills/browser-use"},
        {"name": "image-generation", "dir": "skills/generate-images"},
        {"name": "content-generation", "dir": "skills/content-generation"},
        # Group B
        {"name": "style-book-creation", "dir": "skills/style-book-creation"},
        {"name": "global-css-creation", "dir": "skills/global-css-creation"},
        {"name": "global-js-creation", "dir": "skills/global-js-creation"},
        {"name": "page-creation", "dir": "skills/page-creation"},
        {"name": "fragment-creation", "dir": "skills/create-fragment"},
        {"name": "custom-element-creation", "dir": "skills/create-custom-element"},
        {"name": "content-structure-creation", "dir": "skills/liferay-content"},
        {"name": "object-creation", "dir": "skills/liferay-objects"},
        {"name": "object-action-creation", "dir": "skills/liferay-microservices"},
        {"name": "workflow-action-creation", "dir": "skills/liferay-microservices"},
        {"name": "workflow-creation", "dir": "skills/liferay-workflows"},
        # Group C
        {"name": "api-usage", "dir": "skills/api-usage"},
        {"name": "catalog-management", "dir": "skills/catalog-management"},
        {"name": "product-creation", "dir": "skills/product-creation"},
        {"name": "space-site-management", "dir": "skills/space-site-management"},
        {"name": "user-permission-management", "dir": "skills/user-permission-management"},
        # Group D
        {"name": "demo-planning", "dir": "skills/demo-planning"},
        {"name": "ldm-administration", "dir": "skills/ldm-sysadmin"},
        {"name": "spec-creation", "dir": "skills/spec-creation"},
    ]
    
    # Track checked directories to avoid redundant SKILL.md parsing
    checked_dirs = {}
    passed = 0
    failed = 0
    
    for skill in skills:
        sdir = skill["dir"]
        if not os.path.exists(sdir):
            print(f"[✗] Skill '{skill['name']}': Directory missing ({sdir})")
            failed += 1
            continue
            
        skill_md_path = os.path.join(sdir, "SKILL.md")
        if not os.path.exists(skill_md_path):
            print(f"[✗] Skill '{skill['name']}': SKILL.md missing in {sdir}")
            failed += 1
            continue
            
        if sdir in checked_dirs:
            print(f"[✓] Skill '{skill['name']}': Validated successfully (Shared Skill Bundle: {sdir})")
            passed += 1
            continue
            
        # Parse SKILL.md
        with open(skill_md_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Prohibit Emojis Check
        if not check_for_emojis(content, skill_md_path):
            failed += 1
            continue
            
        # Prohibit Nested Markdown Code Block Highlight Checks
        if not check_markdown_code_blocks(content, skill_md_path):
            failed += 1
            continue
            
        meta = parse_front_matter(content)
        if meta is None:
            print(f"[✗] Skill '{skill['name']}': SKILL.md in {sdir} lacks YAML boundaries")
            failed += 1
            continue
            
        if "name" not in meta or "description" not in meta:
            print(f"[✗] Skill '{skill['name']}': SKILL.md lacks 'name' or 'description' meta")
            failed += 1
            continue
            
        # Verify references mentioned inside STRICT EXECUTION PROTOCOL or available resources actually exist
        lines = content.splitlines()
        ref_fpath_checked = 0
        ref_fpath_errors = []
        for line in lines:
            # Skip lines talking about mock populator script generation
            if any(term in line for term in ["e.g. ", "Place any generated", "Place your generated", "Placeholder", "example"]):
                continue
                
            if "references/" in line or "scripts/" in line or "skills/" in line:
                # Extract file path
                start_idx = line.find("references/")
                if start_idx == -1:
                    start_idx = line.find("skills/")
                if start_idx == -1:
                    start_idx = line.find("scripts/")
                if start_idx != -1:
                    end_idx = len(line)
                    for term in [")", "]", " ", "`", "*", "\"", "'", "<", ">"]:
                        idx = line.find(term, start_idx)
                        if idx != -1 and idx < end_idx:
                            end_idx = idx
                    rel_path = line[start_idx:end_idx].strip()
                    
                    # Resolve checked path using multi-level search:
                    # 1. Workspace root path
                    # 2. Skill folder relative path
                    # 3. If rel_path starts with skills/
                    workspace_path = os.path.join(os.getcwd(), rel_path)
                    skill_rel_path = os.path.join(sdir, rel_path)
                    
                    exists_on_disk = False
                    if os.path.exists(workspace_path):
                        exists_on_disk = True
                    elif os.path.exists(skill_rel_path):
                        exists_on_disk = True
                    elif rel_path.startswith("<skill_dir>/"):
                        # Resolve by stripping <skill_dir>/
                        stripped = rel_path.replace("<skill_dir>/", "")
                        if os.path.exists(os.path.join(sdir, stripped)):
                            exists_on_disk = True
                            
                    ref_fpath_checked += 1
                    if not exists_on_disk:
                        ref_fpath_errors.append(f"Missing referenced asset: {rel_path} (Unresolved in workspace/skill context)")
                    elif rel_path.endswith(".md"):
                        # Ensure referenced guide is emoji-free and nested-markdown-free
                        target_ref_path = workspace_path if os.path.exists(workspace_path) else skill_rel_path
                        with open(target_ref_path, "r", encoding="utf-8") as rf:
                            ref_content = rf.read()
                        if not check_for_emojis(ref_content, rel_path):
                            ref_fpath_errors.append(f"Found prohibited emojis inside reference guide: {rel_path}")
                        if not check_markdown_code_blocks(ref_content, rel_path):
                            ref_fpath_errors.append(f"Found prohibited nested markdown code blocks inside reference guide: {rel_path}")
                        
        if ref_fpath_errors:
            print(f"[✗] Skill '{skill['name']}': Asset Reference Failures in SKILL.md:")
            for err in ref_fpath_errors:
                print(f"    - {err}")
            failed += 1
        else:
            print(f"[✓] Skill '{skill['name']}': Validated successfully ({ref_fpath_checked} references verified)")
            passed += 1
            checked_dirs[sdir] = True
            
    print(f"\nSkills Validation Results: {passed} Passed, {failed} Failed")
    return failed == 0

def compile_python_scripts():
    log_header("Compiling System Scripts")
    scripts = [
        "scripts/env_utils.py",
        "scripts/provision-agent-admin.py",
        "scripts/scaffold-workspace.py",
        "skills/browser-use/scripts/get_dom.py",
        "skills/liferay-objects/scripts/create-object-definition.py",
    ]
    
    passed = 0
    failed = 0
    
    for script in scripts:
        if not os.path.exists(script):
            print(f"[✗] Script '{script}': File missing")
            failed += 1
            continue
            
        try:
            py_compile.compile(script, doraise=True)
            print(f"[✓] Script '{script}': Syntactically correct")
            passed += 1
        except py_compile.PyCompileError as e:
            print(f"[✗] Script '{script}': Compilation failed:")
            print(e)
            failed += 1
            
    print(f"\nScripts Compilation Results: {passed} Passed, {failed} Failed")
    return failed == 0

def main():
    success = True
    success &= audit_agents()
    success &= audit_skills()
    success &= compile_python_scripts()
    
    log_header("Verification Summary")
    if success:
        print("ALL DRY-RUN VERIFICATION TASKS COMPLETED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print("ERRORS DETECTED DURING THE VERIFICATION PROCESS. PLEASE RE-EXAMINE THE FAILING ENTRIES.")
        sys.exit(1)

if __name__ == "__main__":
    main()
