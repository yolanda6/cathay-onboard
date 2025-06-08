import os
import vertexai
from dotenv import load_dotenv
from vertexai import agent_engines
from vertexai.preview import reasoning_engines

# Import the agent from our main module
from agent import root_agent

load_dotenv()
#PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "vital-octagon-19612")
#LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
#STORAGE_BUCKET = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET", "gs://2025-cathay-agentspace")
PROJECT_ID = "vital-octagon-19612"
LOCATION = "us-central1"
STORAGE_BUCKET = "gs://2025-cathay-agentspace"
GOOGLE_CLOUD_STORAGE_BUCKET= "gs://2025-cathay-agentspace"
def deploy_agent():
    """Deploy the multi-agent system to Google Cloud Agent Engine."""
    
    vertexai.init(
        project=PROJECT_ID,
        location=LOCATION,
        staging_bucket=STORAGE_BUCKET,
    )
    
    agent = root_agent
    app = reasoning_engines.AdkApp(
        agent=agent,
        enable_tracing=True,
    )
    
    try:
        remote_app = agent_engines.create(
            agent_engine=agent,
            display_name="Internal Chatbot Multi-Agent System",
            description="Access Workflow Orchestrator with ServiceNow and Active Directory integration",
            requirements=[
                "google-cloud-aiplatform[adk,agent_engines]>=1.50.0",
                "google-genai>=0.1.0",
                "google-adk",
                "python-dotenv>=1.0.0",
            ],
            extra_packages=["agent.py"],
            env_vars={
                "GOOGLE_GENAI_USE_VERTEXAI": "True",
            }
        )
        
        print("\n✅ Deployment successful!")
        print(f"Resource name: {remote_app.resource_name}")
        
        # Save deployment info
        with open("deployment_info.txt", "w") as f:
            f.write(f"RESOURCE_NAME={remote_app.resource_name}\n")
            f.write(f"PROJECT_ID={PROJECT_ID}\n")
            f.write(f"LOCATION={LOCATION}\n")
        
        # Extract just the ID for easier testing
        engine_id = remote_app.resource_name.split('/')[-1]
        print(f"Engine ID (for testing): {engine_id}")
        
        # Test the deployment
        try:
            remote_session = remote_app.create_session(user_id="remote_test")
            print(f"✅ Remote session created: {remote_session['id']}")
            
            response_count = 0
            for event in remote_app.stream_query(
                user_id="remote_test",
                session_id=remote_session["id"],
                message="Add user@company.com to finance_team",
            ):
                print(f"✅ Remote test response received")
                response_count += 1
                if response_count >= 1:
                    break
        except Exception as e:
            print(f"⚠️  Remote test warning: {e}")
        
        print("\n🎉 Deployment complete!")
        print(f"\nYour agent is deployed at:")
        print(f"  {remote_app.resource_name}")
        
        print("\nTo test your deployed agent, run:")
        print(f"python test.py {engine_id}")
        
        print("\nYou can also test it directly with:")
        print("```python")
        print("import vertexai")
        print("from vertexai import agent_engines")
        print(f'vertexai.init(project="{PROJECT_ID}", location="{LOCATION}")')
        print(f'agent = agent_engines.get("{remote_app.resource_name}")')
        print('session = agent.create_session(user_id="test")')
        print('for event in agent.stream_query(user_id="test", session_id=session["id"], message="Add user@company.com to finance_team"):')
        print('    print(event)')
        print("```")
        
        return remote_app
        
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        raise

def main():
    """Main deployment function."""
    print("Internal Chatbot Multi-Agent System Deployment")
    print("=" * 50)
    print(f"Project: {PROJECT_ID}")
    print(f"Location: {LOCATION}")
    print(f"Staging Bucket: {STORAGE_BUCKET}")
    
    # Environment variables are hardcoded above, so no validation needed
    print("Using hardcoded configuration values")
    
    # Confirm deployment
    response = input("\nProceed with deployment? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Deployment cancelled.")
        return 0
    
    try:
        deploy_agent()
        return 0
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
