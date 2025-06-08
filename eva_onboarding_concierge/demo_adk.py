#!/usr/bin/env python3
"""
Eva ADK Demo Script
Demonstrates Eva working with ADK CLI commands.
"""

import subprocess
import sys
import time
import os

def run_command(cmd, timeout=10):
    """Run a command with timeout."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"

def test_agent_import():
    """Test that the agent can be imported correctly."""
    print("🧪 Testing Agent Import...")
    
    returncode, stdout, stderr = run_command(
        'python -c "import agent; print(f\'Agent: {agent.root_agent.name} - {agent.root_agent.description}\')"'
    )
    
    if returncode == 0:
        print("✅ Agent import successful!")
        print(f"   {stdout.strip()}")
        return True
    else:
        print("❌ Agent import failed!")
        print(f"   Error: {stderr}")
        return False

def test_adk_run():
    """Test ADK run command."""
    print("\n🚀 Testing ADK Run Command...")
    
    # Test with --help first
    returncode, stdout, stderr = run_command("adk run --help", timeout=5)
    
    if returncode == 0:
        print("✅ ADK run command is available")
        
        # Test agent discovery
        print("🔍 Testing agent discovery...")
        returncode, stdout, stderr = run_command("adk run --agent agent --dry-run", timeout=10)
        
        if returncode == 0:
            print("✅ ADK can discover and load Eva agent")
            return True
        else:
            print("⚠️ ADK agent discovery had issues:")
            print(f"   stdout: {stdout}")
            print(f"   stderr: {stderr}")
            return False
    else:
        print("❌ ADK run command not available")
        print(f"   Error: {stderr}")
        return False

def test_adk_web():
    """Test ADK web command."""
    print("\n🌐 Testing ADK Web Command...")
    
    # Test with --help first
    returncode, stdout, stderr = run_command("adk web --help", timeout=5)
    
    if returncode == 0:
        print("✅ ADK web command is available")
        return True
    else:
        print("❌ ADK web command not available")
        print(f"   Error: {stderr}")
        return False

def show_usage_examples():
    """Show usage examples."""
    print("\n📚 Eva ADK Usage Examples:")
    print("=" * 40)
    
    print("\n🖥️ Interactive Console Mode:")
    print("   cd eva_onboarding_concierge")
    print("   adk run")
    print("   # or")
    print("   adk run --agent agent")
    
    print("\n🌐 Web Interface Mode:")
    print("   cd eva_onboarding_concierge")
    print("   adk web")
    print("   # Then open http://localhost:8080 in your browser")
    
    print("\n⚙️ Custom Configuration:")
    print("   adk web --port 9000        # Custom port")
    print("   adk run --verbose          # Verbose logging")
    
    print("\n🧪 Testing:")
    print("   python demo_adk.py         # This demo script")
    print("   python setup.py            # Setup wizard")
    print("   python test_eva_system.py  # Full test suite")

def main():
    """Main demo function."""
    print("🤖 Eva Onboarding Concierge - ADK CLI Demo")
    print("=" * 50)
    
    # Test sequence
    tests = [
        ("Agent Import", test_agent_import),
        ("ADK Run Command", test_adk_run),
        ("ADK Web Command", test_adk_web),
    ]
    
    results = {}
    for test_name, test_func in tests:
        results[test_name] = test_func()
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Eva is ready for ADK CLI usage.")
        show_usage_examples()
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
        print("   You may need to:")
        print("   1. Ensure Google ADK is installed: pip install google-adk")
        print("   2. Set up environment variables (see setup.py)")
        print("   3. Install dependencies: pip install -r requirements.txt")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
