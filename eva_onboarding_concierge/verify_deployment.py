#!/usr/bin/env python3
"""
Verification script for Eva Onboarding Concierge deployment.
This script checks if the agent is properly deployed and functional.
"""

import subprocess
import json
import sys

# Configuration
PROJECT_ID = "vital-octagon-19612"
LOCATION = "us-central1"
AGENT_NAME = "eva-onboarding-concierge"

def run_command(command, capture_output=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=capture_output,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {command}")
        print(f"Error: {e.stderr if capture_output else 'See output above'}")
        return None

def check_agent_deployment():
    """Check if the agent is deployed."""
    print("🔍 Checking agent deployment...")
    
    # List agents
    result = run_command(f"gcloud ai agents list --location={LOCATION} --format=json")
    if not result:
        return False
    
    try:
        agents = json.loads(result.stdout)
        eva_agent = None
        
        for agent in agents:
            if AGENT_NAME in agent.get('name', ''):
                eva_agent = agent
                break
        
        if eva_agent:
            print("✅ Eva Onboarding Concierge found!")
            print(f"   Agent ID: {eva_agent['name'].split('/')[-1]}")
            print(f"   Display Name: {eva_agent.get('displayName', 'N/A')}")
            print(f"   State: {eva_agent.get('state', 'N/A')}")
            return True
        else:
            print("❌ Eva Onboarding Concierge not found in deployed agents")
            return False
            
    except json.JSONDecodeError:
        print("❌ Failed to parse agent list")
        return False

def check_apis():
    """Check if required APIs are enabled."""
    print("🔧 Checking required APIs...")
    
    required_apis = [
        "aiplatform.googleapis.com",
        "storage.googleapis.com"
    ]
    
    all_enabled = True
    for api in required_apis:
        result = run_command(f"gcloud services list --enabled --filter='name:{api}' --format='value(name)'")
        if result and api in result.stdout:
            print(f"✅ {api} is enabled")
        else:
            print(f"❌ {api} is not enabled")
            all_enabled = False
    
    return all_enabled

def check_staging_bucket():
    """Check if staging bucket exists."""
    print("📦 Checking staging bucket...")
    
    result = run_command("gsutil ls gs://2025-cathay-agentspace")
    if result:
        print("✅ Staging bucket exists and is accessible")
        return True
    else:
        print("❌ Staging bucket not accessible")
        return False

def test_local_agent():
    """Test if the local agent runs without errors."""
    print("🧪 Testing local agent...")
    
    try:
        # Try to import the agent
        result = run_command("python -c 'from agent import root_agent; print(\"Agent import successful\")'")
        if result:
            print("✅ Local agent imports successfully")
            return True
        else:
            print("❌ Local agent import failed")
            return False
    except Exception as e:
        print(f"❌ Local agent test failed: {e}")
        return False

def generate_deployment_report():
    """Generate a deployment verification report."""
    print("\n📊 Generating deployment report...")
    
    report = {
        "verification_time": subprocess.run("date", shell=True, capture_output=True, text=True).stdout.strip(),
        "project_id": PROJECT_ID,
        "location": LOCATION,
        "agent_name": AGENT_NAME,
        "checks": {
            "agent_deployed": check_agent_deployment(),
            "apis_enabled": check_apis(),
            "staging_bucket": check_staging_bucket(),
            "local_agent": test_local_agent()
        }
    }
    
    # Save report
    with open("deployment_verification.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("✅ Verification report saved to deployment_verification.json")
    return report

def main():
    """Main verification function."""
    print("🔍 Eva Onboarding Concierge - Deployment Verification")
    print("=" * 55)
    
    # Check authentication
    print("🔐 Checking authentication...")
    result = run_command("gcloud auth list --filter=status:ACTIVE --format='value(account)'")
    if result and result.stdout.strip():
        print(f"✅ Authenticated as: {result.stdout.strip()}")
    else:
        print("❌ Not authenticated. Please run 'gcloud auth login'")
        sys.exit(1)
    
    # Generate report
    report = generate_deployment_report()
    
    # Summary
    print("\n📋 Verification Summary:")
    print("-" * 25)
    
    all_passed = True
    for check_name, passed in report["checks"].items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{check_name.replace('_', ' ').title()}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 55)
    if all_passed:
        print("🎉 All verification checks passed!")
        print("Your Eva Onboarding Concierge is ready for use!")
        print(f"\n🌐 Access your agent at:")
        print(f"   https://console.cloud.google.com/ai/agents?project={PROJECT_ID}")
    else:
        print("⚠️  Some verification checks failed.")
        print("Please review the issues above and re-run deployment if needed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
