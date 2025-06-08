#!/usr/bin/env python3
"""
Eva Onboarding Concierge Setup Script
Quick setup and validation for the Eva system.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_adk_installation():
    """Check if Google ADK is installed."""
    try:
        result = subprocess.run(['adk', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Google ADK installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ Google ADK not found")
            return False
    except FileNotFoundError:
        print("❌ Google ADK not installed")
        print("   Install with: pip install google-adk")
        return False

def check_environment_variables():
    """Check if required environment variables are set."""
    required_vars = [
        'GOOGLE_CLOUD_PROJECT',
        'GOOGLE_CLOUD_LOCATION',
        'GOOGLE_GENAI_USE_VERTEXAI'
    ]
    
    missing_vars = []
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var}: {os.getenv(var)}")
        else:
            missing_vars.append(var)
            print(f"⚠️  {var}: Not set")
    
    if missing_vars:
        print("\n📝 To set missing environment variables:")
        for var in missing_vars:
            if var == 'GOOGLE_CLOUD_PROJECT':
                print(f'   export {var}="your-project-id"')
            elif var == 'GOOGLE_CLOUD_LOCATION':
                print(f'   export {var}="us-central1"')
            elif var == 'GOOGLE_GENAI_USE_VERTEXAI':
                print(f'   export {var}="TRUE"')
        return False
    
    return True

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def validate_agent_structure():
    """Validate that all agent files are present."""
    print("\n🔍 Validating agent structure...")
    
    required_files = [
        'agent.py',
        'pyproject.toml',
        'requirements.txt',
        'README.md',
        '__init__.py',
        'eva_orchestrator_agent/agent.py',
        'access_workflow_orchestrator_agent/agent.py',
        'id_master_agent/agent.py',
        'device_depot_agent/agent.py',
        'hr_helper_agent/agent.py',
        'meeting_maven_agent/agent.py',
        'hr_helper_agent/data/timeoff-policy.pdf',
        'hr_helper_agent/data/performance-policy.pdf'
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path}")
    
    if missing_files:
        print(f"\n⚠️  Missing {len(missing_files)} required files")
        return False
    
    print("✅ All agent files present")
    return True

def test_agent_import():
    """Test that the main agent can be imported."""
    print("\n🧪 Testing agent import...")
    try:
        from eva_onboarding_concierge.agent import agent
        print("✅ Main agent imported successfully")
        print(f"   Agent name: {agent.name}")
        print(f"   Agent description: {agent.description}")
        return True
    except Exception as e:
        print(f"❌ Failed to import agent: {e}")
        return False

def run_quick_test():
    """Run a quick functionality test."""
    print("\n🚀 Running quick functionality test...")
    try:
        from eva_onboarding_concierge import process_onboarding_request
        
        response = process_onboarding_request(
            "Hi Eva! Can you help me test the system?", 
            "setup_test_user"
        )
        
        if response and len(response) > 10:
            print("✅ Quick test passed")
            print(f"   Response preview: {response[:100]}...")
            return True
        else:
            print("❌ Quick test failed - no response")
            return False
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False

def show_usage_instructions():
    """Show usage instructions."""
    print("\n🎯 Eva is ready! Here's how to use it:")
    print("\n📱 ADK CLI Commands:")
    print("   adk run                    # Interactive console mode")
    print("   adk web                    # Web interface mode")
    print("   adk web --port 9000        # Custom port")
    print("\n🐍 Python Usage:")
    print("   from eva_onboarding_concierge import process_onboarding_request")
    print("   response = process_onboarding_request('Hi Eva!')")
    print("\n🧪 Testing:")
    print("   python test_eva_system.py              # Full test suite")
    print("   python test_eva_system.py demo         # Quick demo")
    print("\n📚 Documentation:")
    print("   README.md                  # Complete documentation")
    print("   UPGRADE_SUMMARY.md         # System overview")

def main():
    """Main setup function."""
    print("🤖 Eva Onboarding Concierge - Setup & Validation")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Google ADK", check_adk_installation),
        ("Environment Variables", check_environment_variables),
        ("Agent Structure", validate_agent_structure),
    ]
    
    # Run basic checks
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n🔍 Checking {check_name}...")
        if not check_func():
            all_passed = False
    
    if not all_passed:
        print("\n⚠️  Some checks failed. Please address the issues above.")
        return False
    
    # Install dependencies if needed
    install_deps = input("\n📦 Install/update dependencies? (y/N): ").lower().strip()
    if install_deps in ['y', 'yes']:
        if not install_dependencies():
            return False
    
    # Test agent import
    if not test_agent_import():
        return False
    
    # Run quick test
    run_test = input("\n🧪 Run quick functionality test? (y/N): ").lower().strip()
    if run_test in ['y', 'yes']:
        if not run_quick_test():
            print("⚠️  Quick test failed, but Eva might still work")
    
    print("\n🎉 Setup completed successfully!")
    show_usage_instructions()
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
