import vertexai
from vertexai.preview import reasoning_engines
from vertexai import agent_engines
import os
import warnings
from dotenv import load_dotenv

# Load environment variables if .env file exists
try:
    load_dotenv()
except:
    pass

# Configuration - Update these with your actual values
GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "hello-world-418507")
GOOGLE_CLOUD_LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
GOOGLE_GENAI_USE_VERTEXAI = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI", "TRUE")
AGENT_NAME = "internal_chatbot_agent"
MODEL_NAME = "gemini-2.0-flash-exp"

warnings.filterwarnings("ignore")
PROJECT_ID = GOOGLE_CLOUD_PROJECT

def test_deployed_agent(reasoning_engine_id: str):
    """
    Test a deployed agent engine.
    
    Args:
        reasoning_engine_id: The ID of the deployed reasoning engine
    """
    vertexai.init(project=PROJECT_ID, location="us-central1")
    agent = agent_engines.get(reasoning_engine_id)
    
    print("**********************")
    print(f"Testing Agent: {agent}")
    print("**********************")
    
    test_queries = [
        "I need to add john.new@company.com to the finance_team group",
        "Please add sarah.dev@company.com to engineering_team", 
        "Can you help me get access to hr_team for mike.hr@company.com?",
        "Add test.user@company.com to finance_team please"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Test Query {i} ---")
        print(f"Query: {query}")
        print("Response:")
        
        try:
            for event in agent.stream_query(
                user_id="test_user",
                message=query,
            ):
                print(event)
        except Exception as e:
            print(f"Error: {e}")
        
        print("-" * 50)

def test_local_agent():
    """Test the agent locally before deployment."""
    try:
        from agent import process_request
    except ImportError as e:
        print(f"Failed to import agent module: {e}")
        print("Make sure you're in the correct directory and dependencies are installed.")
        return
    
    print("=== Testing Local Agent ===\n")
    
    test_queries = [
        "I need to add john.new@company.com to the finance_team group",
        "Please add sarah.dev@company.com to engineering_team",
        "Can you help me get access to hr_team for mike.hr@company.com?",
        "Add test.user@company.com to finance_team please"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"Test Query {i}: {query}")
        print("-" * 50)
        
        try:
            # Use unique user IDs to avoid session conflicts
            user_id = f"test_user_{i}_{hash(query) % 1000}"
            response = process_request(query, user_id)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Test deployed agent with provided reasoning engine ID
        reasoning_engine_id = sys.argv[1]
        print(f"Testing deployed agent with ID: {reasoning_engine_id}")
        test_deployed_agent(reasoning_engine_id)
    else:
        # Test local agent
        print("Testing local agent...")
        test_local_agent()
        
        print("\nTo test a deployed agent, run:")
        print("python test.py <YOUR_DEPLOYED_ENGINE_ID>")
