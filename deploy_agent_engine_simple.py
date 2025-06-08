import os
import vertexai
from dotenv import load_dotenv
from vertexai import agent_engines
from vertexai.preview import reasoning_engines
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from typing import Optional
from google.genai import types

from google.adk.agents import llm_agent
from google.cloud import bigquery

load_dotenv()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
STORAGE_BUCKET = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")


def list_datasets(project_id: str) -> str:
    """Lists all BigQuery datasets in the specified project.
    
    Args:
        project_id: The Google Cloud project ID
        
    Returns:
        A string listing all datasets found in the project
    """
    try:
        # Create BigQuery client - let it use whatever credentials are available
        client = bigquery.Client(project=project_id)
        
        # List all datasets
        datasets = list(client.list_datasets())
        
        if not datasets:
            return f"No datasets found in project '{project_id}'"
        
        # Format the output
        dataset_info = []
        for dataset in datasets:
            dataset_info.append(f"- {dataset.dataset_id}")
        
        return f"Found {len(datasets)} dataset(s) in project '{project_id}':\n" + "\n".join(dataset_info)
        
    except Exception as e:
        return f"Error listing datasets: {str(e)}"


def get_dataset_info(project_id: str, dataset_id: str) -> str:
    """Gets information about a specific BigQuery dataset.
    
    Args:
        project_id: The Google Cloud project ID
        dataset_id: The dataset ID
        
    Returns:
        Information about the dataset including tables
    """
    try:
        client = bigquery.Client(project=project_id)
        
        # Get dataset reference
        dataset_ref = client.dataset(dataset_id)
        dataset = client.get_dataset(dataset_ref)
        
        # Get basic info
        info = [
            f"Dataset: {dataset.dataset_id}",
            f"Project: {dataset.project}",
            f"Location: {dataset.location}",
            f"Created: {dataset.created}",
            f"Description: {dataset.description or 'No description'}",
            "\nTables:"
        ]
        
        # List tables in the dataset
        tables = list(client.list_tables(dataset))
        if tables:
            for table in tables:
                info.append(f"  - {table.table_id}")
        else:
            info.append("  No tables found")
        
        return "\n".join(info)
        
    except Exception as e:
        return f"Error getting dataset info: {str(e)}"

def test_auth(callback_context: CallbackContext, 
                       llm_request: LlmRequest) -> Optional[LlmResponse]:
    result = list_datasets(PROJECT_ID)
    print("olivierzhang: test_auth result:", result, flush=True)
    if result.startswith("Error") or result.startswith("No datasets found"):
        print("❌ Authentication failed or no datasets found. Please check your credentials.", flush=True)
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text=f"Authentication failed or no datasets found. Please check your credentials: {result}")],
            )
        )
    return None

# Create the agent
root_agent = llm_agent.Agent(
    model="gemini-2.0-flash",
    name="simple_bigquery_agent",
    description=(
        "A simple agent that can list and get information about BigQuery datasets"
    ),
    instruction="""\
        You are a helpful BigQuery assistant. You can help users:
        1. List all datasets in a project
        2. Get information about specific datasets
        
        When users ask about BigQuery data, use the available tools to help them.
        Always specify the project_id when calling tools.
    """,
    before_model_callback=test_auth,
    tools=[list_datasets, get_dataset_info],
)

def deploy_agent():
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
            display_name="Simple BigQuery Agent",
            description="A simple agent that lists BigQuery datasets without handling auth",
            requirements=[
                "google-cloud-aiplatform[adk,agent_engines]>=1.50.0",
                "google-genai>=0.1.0",
                "google-cloud-bigquery>=3.0.0",
                "python-dotenv>=1.0.0",
            ],
            env_vars={
                "GOOGLE_GENAI_USE_VERTEXAI": "True",
            }
        )
        
        print("\n✅ Deployment successful!")
        print(f"Resource name: {remote_app.resource_name}")
        
        with open("deployment_info.txt", "w") as f:
            f.write(f"RESOURCE_NAME={remote_app.resource_name}\n")
            f.write(f"PROJECT_ID={PROJECT_ID}\n")
            f.write(f"LOCATION={LOCATION}\n")
                
        try:
            remote_session = remote_app.create_session(user_id="remote_test")
            print(f"✅ Remote session created: {remote_session['id']}")
            
            response_count = 0
            for event in remote_app.stream_query(
                user_id="remote_test",
                session_id=remote_session["id"],
                message=f"List datasets in project {PROJECT_ID}",
            ):
                print(f"✅ Remote test response received")
                response_count += 1
                if response_count >= 1:
                    break
        except Exception as e:
            print(f"⚠️  Remote test warning: {e}")
        
        print("\n🎉 Deployment complete!")
        print(f"\nYour simple agent is deployed at:")
        print(f"  {remote_app.resource_name}")
        
        return remote_app
        
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        raise


def main():
    required_vars = ["GOOGLE_CLOUD_PROJECT", "GOOGLE_CLOUD_STORAGE_BUCKET"]
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        print(f"❌ Missing required environment variables: {', '.join(missing)}")
        print("\nPlease set these in your .env file:")
        for var in missing:
            print(f"  {var}=your-value")
        return 1
    
    try:
        deploy_agent()
        return 0
    except Exception as e:
        return 1


if __name__ == "__main__":
    exit(main())
