#!/usr/bin/env python3
"""
Deployment script for the Internal Chatbot Multi-Agent System.
This script handles the deployment to Google Cloud Agent Engine.
"""

import os
import sys
import vertexai
from vertexai.preview import reasoning_engines
from vertexai import agent_engines

# Import the agent from our main module
from agent import root_agent

def deploy_agent():
    """Deploy the multi-agent system to Google Cloud Agent Engine."""
    
    # Configuration
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "hello-world-418507")
    LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    STAGING_BUCKET = os.environ.get("STAGING_BUCKET", "gs://2025-wy-agentspace")
    
    print(f"Deploying to Project: {PROJECT_ID}")
    print(f"Location: {LOCATION}")
    print(f"Staging Bucket: {STAGING_BUCKET}")
    
    # Initialize Vertex AI
    vertexai.init(
        project=PROJECT_ID,
        location=LOCATION,
        staging_bucket=STAGING_BUCKET,
    )
    
    # Create the ADK app
    app = reasoning_engines.AdkApp(
        agent=root_agent,
        enable_tracing=True,
    )
    
    print("Creating Agent Engine deployment...")
    print("This may take 1-2 minutes to complete...")
    
    try:
        # Deploy to Agent Engine
        remote_app = agent_engines.create(
            app,
            requirements=[
                "google-cloud-aiplatform[agent_engines,adk]>=1.88",
                "google-adk",
                "pysqlite3-binary",
                "toolbox-langchain==0.1.0",
                "pdfplumber",
                "google-cloud-aiplatform",
                "cloudpickle==3.1.1",
                "pydantic==2.10.6",
                "pytest",
                "overrides",
                "scikit-learn",
                "reportlab",
                "google-auth",
                "google-cloud-storage",
            ],
        )
        
        print("\n" + "="*60)
        print("DEPLOYMENT SUCCESSFUL!")
        print("="*60)
        print(f"Agent Engine ID: {remote_app.resource_name}")
        print(f"Full Resource Name: {remote_app.resource_name}")
        
        # Extract just the ID for easier testing
        engine_id = remote_app.resource_name.split('/')[-1]
        print(f"Engine ID (for testing): {engine_id}")
        
        print("\nTo test your deployed agent, run:")
        print(f"python test.py {engine_id}")
        
        print("\nYou can also test it directly with:")
        print("```python")
        print("import vertexai")
        print("from vertexai import agent_engines")
        print(f'vertexai.init(project="{PROJECT_ID}", location="{LOCATION}")')
        print(f'agent = agent_engines.get("{remote_app.resource_name}")')
        print('for event in agent.stream_query(user_id="test", message="Add user@company.com to finance_team"):')
        print('    print(event)')
        print("```")
        
        return remote_app
        
    except Exception as e:
        print(f"\nDeployment failed with error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Ensure you're authenticated: gcloud auth application-default login")
        print("2. Check your project ID and permissions")
        print("3. Verify the staging bucket exists and is accessible")
        return None

def main():
    """Main deployment function."""
    print("Internal Chatbot Multi-Agent System Deployment")
    print("=" * 50)
    
    # Check environment variables
    required_vars = ["GOOGLE_CLOUD_PROJECT"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print("Warning: Missing environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nUsing default values. Set these variables for production deployment.")
    
    # Confirm deployment
    response = input("\nProceed with deployment? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Deployment cancelled.")
        return
    
    # Deploy the agent
    remote_app = deploy_agent()
    
    if remote_app:
        print("\nDeployment completed successfully!")
    else:
        print("\nDeployment failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
