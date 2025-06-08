#!/usr/bin/env python3
"""
Setup verification script for the Internal Chatbot Multi-Agent System.
This script checks if all required files and dependencies are in place.
"""

import os
import sys
import importlib.util

def check_file_exists(filepath, description):
    """Check if a file exists and print status."""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (MISSING)")
        return False

def check_import(module_name, description):
    """Check if a Python module can be imported."""
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            print(f"✅ {description}: {module_name}")
            return True
        else:
            print(f"❌ {description}: {module_name} (NOT FOUND)")
            return False
    except ImportError:
        print(f"❌ {description}: {module_name} (IMPORT ERROR)")
        return False

def check_environment_variables():
    """Check important environment variables."""
    print("\n📋 Environment Variables:")
    
    env_vars = [
        ("GOOGLE_CLOUD_PROJECT", "Google Cloud Project ID"),
        ("GOOGLE_CLOUD_LOCATION", "Google Cloud Location"),
        ("GOOGLE_GENAI_USE_VERTEXAI", "Use Vertex AI flag")
    ]
    
    all_good = True
    for var_name, description in env_vars:
        value = os.environ.get(var_name)
        if value:
            print(f"✅ {description}: {value}")
        else:
            print(f"⚠️  {description}: {var_name} (NOT SET - using defaults)")
            all_good = False
    
    return all_good

def check_project_structure():
    """Check if all required project files exist."""
    print("📁 Project Structure:")
    
    required_files = [
        ("agent.py", "Main agent implementation"),
        ("requirements.txt", "Python dependencies"),
        ("test.py", "Test script"),
        ("deploy.py", "Deployment script"),
        ("README.md", "Documentation"),
        (".env.example", "Environment variables example"),
        ("workflow_diagram.md", "Workflow documentation")
    ]
    
    all_files_exist = True
    for filename, description in required_files:
        if not check_file_exists(filename, description):
            all_files_exist = False
    
    return all_files_exist

def check_dependencies():
    """Check if required Python packages are available."""
    print("\n📦 Python Dependencies:")
    
    required_packages = [
        ("google.adk", "Google ADK"),
        ("google.genai", "Google GenAI"),
        ("vertexai", "Vertex AI"),
        ("pydantic", "Pydantic")
    ]
    
    all_deps_available = True
    for package_name, description in required_packages:
        if not check_import(package_name, description):
            all_deps_available = False
    
    return all_deps_available

def check_agent_configuration():
    """Check if the agent can be imported and configured."""
    print("\n🤖 Agent Configuration:")
    
    try:
        # Try to import the main agent module
        from agent import root_agent, servicenow_agent, ad_agent
        print("✅ Agent modules imported successfully")
        
        # Check agent names
        agents = [
            (root_agent, "Root Orchestrator Agent"),
            (servicenow_agent, "ServiceNow Agent"),
            (ad_agent, "Active Directory Agent")
        ]
        
        for agent, description in agents:
            print(f"✅ {description}: {agent.name}")
        
        # Check sub-agent relationships
        if hasattr(root_agent, 'sub_agents') and root_agent.sub_agents:
            print(f"✅ Sub-agents configured: {[agent.name for agent in root_agent.sub_agents]}")
        else:
            print("❌ Sub-agents not properly configured")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import agent modules: {e}")
        return False
    except Exception as e:
        print(f"❌ Agent configuration error: {e}")
        return False

def main():
    """Main setup verification function."""
    print("Internal Chatbot Multi-Agent System - Setup Verification")
    print("=" * 60)
    
    checks = [
        ("Project Structure", check_project_structure),
        ("Environment Variables", check_environment_variables),
        ("Python Dependencies", check_dependencies),
        ("Agent Configuration", check_agent_configuration)
    ]
    
    all_checks_passed = True
    
    for check_name, check_function in checks:
        print(f"\n🔍 Checking {check_name}...")
        if not check_function():
            all_checks_passed = False
    
    print("\n" + "=" * 60)
    
    if all_checks_passed:
        print("🎉 All checks passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Run local tests: python test.py")
        print("2. Deploy to cloud: python deploy.py")
        print("3. Test deployed agent: python test.py <engine_id>")
    else:
        print("⚠️  Some checks failed. Please review the issues above.")
        print("\nTroubleshooting:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set environment variables (see .env.example)")
        print("3. Ensure Google Cloud authentication is set up")
        
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
