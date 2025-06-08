import os
import vertexai
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from google.adk.tools.function_tool import FunctionTool
from typing import Dict, Any
import uuid
import json
from datetime import datetime

# Configuration
#PROJECT_ID = "hello-world-418507"
PROJECT_ID ="aimc-410006"

LOCATION = "us-central1"
STAGING_BUCKET = "gs://2025-wy-agentspace"

os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"

# Model configuration
GEMINI_2_FLASH = "gemini-2.0-flash-exp"

# Mock databases
mock_ad_groups = {
    "finance_team": {
        "owner": "john.doe@company.com",
        "members": ["alice@company.com", "bob@company.com"],
        "description": "Finance team access group"
    },
    "hr_team": {
        "owner": "jane.smith@company.com", 
        "members": ["carol@company.com", "dave@company.com"],
        "description": "HR team access group"
    },
    "engineering_team": {
        "owner": "tech.lead@company.com",
        "members": ["dev1@company.com", "dev2@company.com"],
        "description": "Engineering team access group"
    }
}

mock_service_requests = {}
mock_work_orders = {}

# ServiceNow Agent Tools
def create_service_request(group_name: str, new_user_email: str, requester_email: str) -> Dict[str, Any]:
    """
    Creates a service request for AD group access approval.
    
    Args:
        group_name: The AD group name to request access to
        new_user_email: Email of the user requesting access
        requester_email: Email of the person making the request
    
    Returns:
        Service request details with request ID
    """
    if group_name not in mock_ad_groups:
        return {
            "status": "error",
            "message": f"AD group '{group_name}' not found"
        }
    
    request_id = f"SR-{uuid.uuid4().hex[:8].upper()}"
    group_owner = mock_ad_groups[group_name]["owner"]
    
    service_request = {
        "request_id": request_id,
        "group_name": group_name,
        "new_user_email": new_user_email,
        "requester_email": requester_email,
        "group_owner": group_owner,
        "status": "pending_approval",
        "created_at": datetime.now().isoformat(),
        "description": f"Request to add {new_user_email} to {group_name} AD group"
    }
    
    mock_service_requests[request_id] = service_request
    
    return {
        "status": "success",
        "request_id": request_id,
        "message": f"Service request {request_id} created. Approval request sent to {group_owner}",
        "group_owner": group_owner
    }

def get_approval_status(request_id: str) -> Dict[str, Any]:
    """
    Checks the approval status of a service request.
    
    Args:
        request_id: The service request ID
    
    Returns:
        Current approval status
    """
    if request_id not in mock_service_requests:
        return {
            "status": "error",
            "message": f"Service request {request_id} not found"
        }
    
    # Mock approval process - automatically approve for demo
    service_request = mock_service_requests[request_id]
    if service_request["status"] == "pending_approval":
        service_request["status"] = "approved"
        service_request["approved_at"] = datetime.now().isoformat()
        
        # Create work order
        work_order_id = f"WO-{uuid.uuid4().hex[:8].upper()}"
        work_order = {
            "work_order_id": work_order_id,
            "request_id": request_id,
            "group_name": service_request["group_name"],
            "new_user_email": service_request["new_user_email"],
            "status": "ready_for_execution",
            "created_at": datetime.now().isoformat()
        }
        mock_work_orders[work_order_id] = work_order
        service_request["work_order_id"] = work_order_id
    
    return {
        "status": "success",
        "request_status": service_request["status"],
        "work_order_id": service_request.get("work_order_id"),
        "message": f"Request {request_id} has been {service_request['status']}"
    }

def close_work_order(work_order_id: str, completion_status: str) -> Dict[str, Any]:
    """
    Closes a work order after AD operations are complete.
    
    Args:
        work_order_id: The work order ID
        completion_status: Status of the completion (success/failed)
    
    Returns:
        Work order closure confirmation
    """
    if work_order_id not in mock_work_orders:
        return {
            "status": "error",
            "message": f"Work order {work_order_id} not found"
        }
    
    work_order = mock_work_orders[work_order_id]
    work_order["status"] = "completed"
    work_order["completion_status"] = completion_status
    work_order["completed_at"] = datetime.now().isoformat()
    
    # Update related service request
    request_id = work_order["request_id"]
    if request_id in mock_service_requests:
        mock_service_requests[request_id]["status"] = "completed"
        mock_service_requests[request_id]["completed_at"] = datetime.now().isoformat()
    
    return {
        "status": "success",
        "message": f"Work order {work_order_id} closed successfully with status: {completion_status}",
        "work_order_id": work_order_id
    }

# Active Directory Agent Tools
def add_user_to_ad_group(work_order_id: str) -> Dict[str, Any]:
    """
    Adds a user to an Active Directory group based on work order.
    
    Args:
        work_order_id: The work order ID containing user and group details
    
    Returns:
        Result of the AD operation
    """
    if work_order_id not in mock_work_orders:
        return {
            "status": "error",
            "message": f"Work order {work_order_id} not found"
        }
    
    work_order = mock_work_orders[work_order_id]
    group_name = work_order["group_name"]
    new_user_email = work_order["new_user_email"]
    
    if group_name not in mock_ad_groups:
        return {
            "status": "error",
            "message": f"AD group '{group_name}' not found"
        }
    
    # Add user to group
    if new_user_email not in mock_ad_groups[group_name]["members"]:
        mock_ad_groups[group_name]["members"].append(new_user_email)
        
        # Update work order status
        work_order["status"] = "ad_operation_completed"
        work_order["ad_operation_result"] = "success"
        work_order["ad_operation_completed_at"] = datetime.now().isoformat()
        
        return {
            "status": "success",
            "message": f"Successfully added {new_user_email} to {group_name} AD group",
            "group_name": group_name,
            "new_user_email": new_user_email,
            "work_order_id": work_order_id
        }
    else:
        return {
            "status": "info",
            "message": f"User {new_user_email} is already a member of {group_name}",
            "group_name": group_name,
            "new_user_email": new_user_email
        }

def verify_ad_group_membership(group_name: str, user_email: str) -> Dict[str, Any]:
    """
    Verifies if a user is a member of an AD group.
    
    Args:
        group_name: The AD group name
        user_email: The user's email address
    
    Returns:
        Membership verification result
    """
    if group_name not in mock_ad_groups:
        return {
            "status": "error",
            "message": f"AD group '{group_name}' not found"
        }
    
    is_member = user_email in mock_ad_groups[group_name]["members"]
    
    return {
        "status": "success",
        "is_member": is_member,
        "group_name": group_name,
        "user_email": user_email,
        "message": f"User {user_email} {'is' if is_member else 'is not'} a member of {group_name}"
    }

# Create ServiceNow Agent
servicenow_agent = LlmAgent(
    model=GEMINI_2_FLASH,
    name="servicenow_agent",
    instruction="""You are a ServiceNow Agent responsible for managing service requests and work orders for AD group access.

Your responsibilities:
1. Create service requests for AD group owner approval when users need to be added to groups
2. Check approval status and create work orders when approved
3. Close work orders after AD operations are completed

When creating service requests:
- Always validate that the AD group exists
- Capture the requester, new user, and target group information
- Send approval requests to the appropriate group owner

When checking approval status:
- Monitor for approvals and automatically create work orders
- Return work order IDs to the root agent for AD operations

When closing work orders:
- Mark work orders as completed based on AD operation results
- Update related service requests to completed status

Always provide clear status updates and next steps.""",
    description="Manages ServiceNow service requests and work orders for AD group access",
    tools=[
        FunctionTool(func=create_service_request),
        FunctionTool(func=get_approval_status),
        FunctionTool(func=close_work_order)
    ],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)

# Create Active Directory Agent
ad_agent = LlmAgent(
    model=GEMINI_2_FLASH,
    name="ad_agent", 
    instruction="""You are an Active Directory Agent responsible for managing user access to AD groups.

Your responsibilities:
1. Add users to AD groups based on approved work orders
2. Verify group memberships
3. Ensure proper access control and security

When adding users to groups:
- Only process approved work orders
- Validate that both the user and group exist
- Add the user to the specified group
- Report success/failure status back to the root agent

When verifying memberships:
- Check if users are already members of groups
- Provide accurate membership status

Always follow security best practices and provide detailed operation results.""",
    description="Manages Active Directory group memberships and user access",
    tools=[
        FunctionTool(func=add_user_to_ad_group),
        FunctionTool(func=verify_ad_group_membership)
    ],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)

# Create Root Orchestrator Agent
root_agent = LlmAgent(
    model=GEMINI_2_FLASH,
    name="root_orchestrator_agent",
    instruction="""You are the Root Orchestrator Agent for the internal chatbot system. You coordinate between ServiceNow and Active Directory agents to handle user access requests.

WORKFLOW PROCESS:
1. When a user requests to be added to an AD group:
   - Transfer to ServiceNow agent to create a service request
   - Wait for approval and work order creation
   
2. Once work order is created:
   - Transfer to AD agent to add user to the group
   - Wait for AD operation completion
   
3. After AD operation:
   - Transfer back to ServiceNow agent to close the work order
   - Provide final status to the user

TRANSFER RULES:
- For service request creation and work order management: transfer to servicenow_agent
- For AD group operations: transfer to ad_agent
- Always coordinate the full workflow from start to finish
- Provide clear status updates to users throughout the process

Handle requests like:
- "Add [user] to [group]"
- "I need access to [group]"
- "Please add [email] to [group] for [reason]"

Always ensure the complete workflow is executed and provide comprehensive status updates.""",
    description="Orchestrates the complete workflow for AD group access requests between ServiceNow and AD agents",
    sub_agents=[servicenow_agent, ad_agent]
)

# Session and Runner setup
session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name="internal_chatbot_app",
    session_service=session_service
)

def process_request(user_input: str, user_id: str = "default_user") -> str:
    """
    Process a user request through the multi-agent system.
    
    Args:
        user_input: The user's request
        user_id: Unique identifier for the user
    
    Returns:
        Final response from the agent system
    """
    # Create or get session
    session_id = f"session_{user_id}"
    
    # Check if session exists, if not create it
    session = None
    try:
        session = session_service.get_session(
            app_name="internal_chatbot_app",
            user_id=user_id,
            session_id=session_id
        )
    except:
        # Session doesn't exist, create a new one
        pass
    
    if session is None:
        session = session_service.create_session(
            app_name="internal_chatbot_app",
            user_id=user_id,
            session_id=session_id
        )
    
    # Process the request
    content = types.Content(role="user", parts=[types.Part(text=user_input)])
    events = runner.run(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )
    
    final_response = ""
    for event in events:
        if event.is_final_response() and event.content and event.content.parts:
            final_response = event.content.parts[0].text
            break
    
    return final_response

# Test function
def test_workflow():
    """Test the complete workflow with sample requests."""
    print("=== Testing Internal Chatbot Multi-Agent System ===\n")
    
    test_cases = [
        "I need to add john.new@company.com to the finance_team group",
        "Please add sarah.dev@company.com to engineering_team",
        "Can you help me get access to hr_team for mike.hr@company.com?"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test Case {i}: {test_case}")
        print("-" * 50)
        
        response = process_request(test_case, f"test_user_{i}")
        print(f"Response: {response}")
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    # Run tests
    test_workflow()
    
    # Interactive mode
    print("Interactive mode - Enter your requests (type 'quit' to exit):")
    while True:
        user_input = input("\nUser: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        if user_input:
            response = process_request(user_input, "interactive_user")
            print(f"Assistant: {response}")

# Agent Engine Deployment:
# Create a remote app for our multiagent with agent Engine.
# This may take 1-2 minutes to finish.
# Uncomment the below segment when you're ready to deploy.

# from vertexai import agent_engines

# app = reasoning_engines.AdkApp(
#     agent=root_agent,
#     enable_tracing=True,
# )

# vertexai.init(
#     project=PROJECT_ID,
#     location=LOCATION,
#     staging_bucket=STAGING_BUCKET,
# )

# remote_app = agent_engines.create(
#     app,
#     requirements=[
#         "google-cloud-aiplatform[agent_engines,adk]>=1.88",
#         "google-adk",
#         "pysqlite3-binary",
#         "toolbox-langchain==0.1.0",
#         "pdfplumber",
#         "google-cloud-aiplatform",
#         "cloudpickle==3.1.1",
#         "pydantic==2.10.6",
#         "pytest",
#         "overrides",
#         "scikit-learn",
#         "reportlab",
#         "google-auth",
#         "google-cloud-storage",
#     ],
# )
# Deployment to Agent Engine related code ends
