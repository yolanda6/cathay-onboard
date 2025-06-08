#!/usr/bin/env python3
"""
Deployment script for Eva Onboarding Concierge to GCP Agent Engine.
This script deploys the root agent (Eva Orchestrator) to Google Cloud Platform.
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path

# Configuration
PROJECT_ID = "vital-octagon-19612"
LOCATION = "us-central1"
STAGING_BUCKET = "gs://2025-cathay-agentspace"
AGENT_NAME = "eva-onboarding-concierge"
AGENT_DISPLAY_NAME = "Eva - AI Onboarding Concierge"
AGENT_DESCRIPTION = "Comprehensive AI-powered employee onboarding orchestrator with 6 specialist agents"

def run_command(command, check=True, capture_output=True):
    """Run a shell command and return the result."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=check,
            capture_output=capture_output,
            text=True
        )
        if capture_output:
            print(f"Output: {result.stdout}")
            if result.stderr:
                print(f"Error: {result.stderr}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        if capture_output:
            print(f"Error output: {e.stderr}")
        raise

def check_prerequisites():
    """Check if all prerequisites are installed and configured."""
    print("🔍 Checking prerequisites...")
    
    # Check if gcloud is installed
    try:
        result = run_command("gcloud version")
        print("✅ Google Cloud CLI is installed")
    except subprocess.CalledProcessError:
        print("❌ Google Cloud CLI is not installed. Please install it first.")
        sys.exit(1)
    
    # Check if authenticated
    try:
        result = run_command("gcloud auth list --filter=status:ACTIVE --format='value(account)'")
        if result.stdout.strip():
            print(f"✅ Authenticated as: {result.stdout.strip()}")
        else:
            print("❌ Not authenticated. Please run 'gcloud auth login'")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print("❌ Authentication check failed")
        sys.exit(1)
    
    # Check if ADK is installed
    try:
        result = run_command("adk --help")
        print("✅ Google ADK is installed")
    except subprocess.CalledProcessError:
        print("❌ Google ADK is not installed. Please install it first.")
        sys.exit(1)
    
    # Check if project is set
    try:
        result = run_command("gcloud config get-value project")
        current_project = result.stdout.strip()
        if current_project != PROJECT_ID:
            print(f"⚠️  Current project is {current_project}, setting to {PROJECT_ID}")
            run_command(f"gcloud config set project {PROJECT_ID}")
        print(f"✅ Project set to: {PROJECT_ID}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to set project to {PROJECT_ID}")
        sys.exit(1)

def enable_apis():
    """Enable required Google Cloud APIs."""
    print("🔧 Enabling required APIs...")
    
    apis = [
        "aiplatform.googleapis.com",
        "storage.googleapis.com",
        "cloudbuild.googleapis.com",
        "run.googleapis.com"
    ]
    
    for api in apis:
        try:
            run_command(f"gcloud services enable {api}")
            print(f"✅ Enabled {api}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to enable {api}")
            sys.exit(1)

def create_staging_bucket():
    """Create staging bucket if it doesn't exist."""
    print("📦 Setting up staging bucket...")
    
    try:
        # Check if bucket exists
        run_command(f"gsutil ls {STAGING_BUCKET}")
        print(f"✅ Staging bucket {STAGING_BUCKET} already exists")
    except subprocess.CalledProcessError:
        # Create bucket
        try:
            bucket_name = STAGING_BUCKET.replace("gs://", "")
            run_command(f"gsutil mb -p {PROJECT_ID} -l {LOCATION} {STAGING_BUCKET}")
            print(f"✅ Created staging bucket {STAGING_BUCKET}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to create staging bucket {STAGING_BUCKET}")
            sys.exit(1)

def prepare_deployment():
    """Prepare the deployment package."""
    print("📋 Preparing deployment package...")
    
    # Ensure we're in the right directory
    os.chdir(Path(__file__).parent)
    
    # Check if agent.py exists (root agent)
    if not os.path.exists("agent.py"):
        print("❌ agent.py not found. Make sure you're in the eva_onboarding_concierge directory")
        sys.exit(1)
    
    # Check if all sub-agents exist
    required_agents = [
        "eva_orchestrator_agent",
        "id_master_agent", 
        "device_depot_agent",
        "hr_helper_agent",
        "access_workflow_orchestrator_agent",
        "meeting_maven_agent"
    ]
    
    for agent in required_agents:
        if not os.path.exists(f"{agent}/agent.py"):
            print(f"❌ {agent}/agent.py not found")
            sys.exit(1)
    
    print("✅ All agent files found")
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("⚠️  requirements.txt not found, creating one...")
        create_requirements_file()
    
    print("✅ Deployment package ready")

def create_requirements_file():
    """Create requirements.txt file if it doesn't exist."""
    requirements_content = """
google-adk>=0.1.0
google-cloud-aiplatform>=1.38.0
google-cloud-storage>=2.10.0
google-genai>=0.3.0
vertexai>=1.38.0
pydantic>=2.0.0
typing-extensions>=4.0.0
PyPDF2>=3.0.0
""".strip()
    
    with open("requirements.txt", "w") as f:
        f.write(requirements_content)
    
    print("✅ Created requirements.txt")

def deploy_agent():
    """Deploy the agent to GCP Agent Engine."""
    print("🚀 Deploying Eva Onboarding Concierge to GCP Agent Engine...")
    
    try:
        # Deploy using ADK
        deploy_command = f"""
        adk deploy \
            --project-id {PROJECT_ID} \
            --location {LOCATION} \
            --staging-bucket {STAGING_BUCKET} \
            --agent-name {AGENT_NAME} \
            --display-name "{AGENT_DISPLAY_NAME}" \
            --description "{AGENT_DESCRIPTION}" \
            .
        """
        
        result = run_command(deploy_command.strip().replace('\n', ' ').replace('  ', ' '))
        
        print("✅ Deployment initiated successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        return False

def check_deployment_status():
    """Check the deployment status."""
    print("📊 Checking deployment status...")
    
    try:
        # List agents to check if deployment was successful
        result = run_command(f"gcloud ai agents list --location={LOCATION} --format='value(name,displayName)'")
        
        if AGENT_NAME in result.stdout:
            print("✅ Agent deployed successfully!")
            
            # Get agent details
            agent_list_command = f"gcloud ai agents list --location={LOCATION} --filter='displayName:\"{AGENT_DISPLAY_NAME}\"' --format='value(name)'"
            agent_result = run_command(agent_list_command)
            
            if agent_result.stdout.strip():
                agent_resource_name = agent_result.stdout.strip()
                print(f"🎯 Agent Resource Name: {agent_resource_name}")
                
                # Construct the agent URL
                agent_url = f"https://console.cloud.google.com/ai/agents/{agent_resource_name.split('/')[-1]}?project={PROJECT_ID}"
                print(f"🌐 Agent Console URL: {agent_url}")
                
                return True
        else:
            print("⏳ Deployment may still be in progress...")
            return False
            
    except subprocess.CalledProcessError:
        print("❌ Failed to check deployment status")
        return False

def create_deployment_info():
    """Create a deployment info file with useful details."""
    deployment_info = {
        "project_id": PROJECT_ID,
        "location": LOCATION,
        "agent_name": AGENT_NAME,
        "agent_display_name": AGENT_DISPLAY_NAME,
        "staging_bucket": STAGING_BUCKET,
        "deployment_time": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "console_url": f"https://console.cloud.google.com/ai/agents?project={PROJECT_ID}",
        "agent_capabilities": [
            "Employee Identity Management",
            "IT Equipment Provisioning", 
            "Access Control & Security",
            "HR Policy Assistance",
            "Meeting Scheduling",
            "Multi-Agent Orchestration"
        ],
        "sub_agents": [
            "Eva Orchestrator (Root Agent)",
            "ID Master Agent",
            "Device Depot Agent", 
            "HR Helper Agent",
            "Access Workflow Orchestrator Agent",
            "Meeting Maven Agent"
        ]
    }
    
    with open("deployment_info.json", "w") as f:
        json.dump(deployment_info, f, indent=2)
    
    print("✅ Created deployment_info.json")

def main():
    """Main deployment function."""
    print("🚀 Eva Onboarding Concierge - GCP Agent Engine Deployment")
    print("=" * 60)
    
    try:
        # Step 1: Check prerequisites
        check_prerequisites()
        
        # Step 2: Enable APIs
        enable_apis()
        
        # Step 3: Create staging bucket
        create_staging_bucket()
        
        # Step 4: Prepare deployment
        prepare_deployment()
        
        # Step 5: Deploy agent
        if deploy_agent():
            # Step 6: Check deployment status
            time.sleep(10)  # Wait a bit for deployment to process
            check_deployment_status()
            
            # Step 7: Create deployment info
            create_deployment_info()
            
            print("\n🎉 Deployment completed successfully!")
            print("\n📋 Next Steps:")
            print("1. Check the Google Cloud Console for your deployed agent")
            print("2. Test the agent through the Agent Engine interface")
            print("3. Configure any additional settings as needed")
            print("4. Monitor agent performance and usage")
            
            print(f"\n🌐 Access your agent at:")
            print(f"   https://console.cloud.google.com/ai/agents?project={PROJECT_ID}")
            
        else:
            print("\n❌ Deployment failed. Please check the error messages above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️  Deployment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
