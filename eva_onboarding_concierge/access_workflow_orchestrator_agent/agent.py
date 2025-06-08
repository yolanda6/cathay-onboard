"""
Access Workflow Orchestrator Agent - Enhanced Version
A powerful sub-orchestrator that manages the secure, multi-step process for granting access to sensitive AD groups.
Coordinates between ServiceNow and Active Directory agents with enhanced capabilities.
"""

import os
import vertexai
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from google.adk.tools.function_tool import FunctionTool
from typing import Dict, Any, List, Optional
import uuid
import json
from datetime import datetime, timedelta
import logging

# Configuration
#PROJECT_ID = "aimc-410006"
PROJECT_ID = "vital-octagon-19612"
LOCATION = "us-central1"
STAGING_BUCKET = "gs://2025-cathay-agentspace"

os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"

# Model configuration
GEMINI_2_FLASH = "gemini-2.0-flash-exp"

# Simplified mock databases
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
    },
    "marketing_team": {
        "owner": "marketing.lead@company.com",
        "members": ["marketer1@company.com", "marketer2@company.com"],
        "description": "Marketing team access group"
    },
    "admin_group": {
        "owner": "admin@company.com",
        "members": ["admin1@company.com"],
        "description": "Administrative access group"
    }
}

mock_service_requests = {}
mock_work_orders = {}
mock_access_reviews = {}

# Enhanced ServiceNow Agent Tools
def create_service_request(group_name: str, new_user_email: str, requester_email: str) -> Dict[str, Any]:
    """
    Creates a simple service request for AD group access approval.
    
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
            "message": f"AD group '{group_name}' not found",
            "available_groups": list(mock_ad_groups.keys())
        }
    
    group_info = mock_ad_groups[group_name]
    request_id = f"SR-{uuid.uuid4().hex[:8].upper()}"
    group_owner = group_info["owner"]
    
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
    
    service_request = mock_service_requests[request_id]
    
    # Mock approval process - automatically approve for demo
    if service_request["status"] == "pending_approval":
        service_request["status"] = "approved"
        service_request["approved_at"] = datetime.now().isoformat()
        service_request["approved_by"] = service_request["group_owner"]
        
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
        "approved_by": service_request.get("approved_by"),
        "message": f"Request {request_id} has been {service_request['status']}"
    }

def close_work_order(work_order_id: str, completion_status: str, notes: str = "") -> Dict[str, Any]:
    """
    Closes a work order after AD operations are complete with enhanced tracking.
    
    Args:
        work_order_id: The work order ID
        completion_status: Status of the completion (success/failed)
        notes: Additional notes about the completion
    
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
    work_order["completion_notes"] = notes
    work_order["completed_at"] = datetime.now().isoformat()
    
    # Update related service request
    request_id = work_order["request_id"]
    if request_id in mock_service_requests:
        mock_service_requests[request_id]["status"] = "completed"
        mock_service_requests[request_id]["completed_at"] = datetime.now().isoformat()
        
        # Schedule access review if successful
        if completion_status == "success":
            review_id = f"AR-{uuid.uuid4().hex[:8].upper()}"
            review_date = datetime.now() + timedelta(days=30)  # Review in 30 days
            mock_access_reviews[review_id] = {
                "review_id": review_id,
                "request_id": request_id,
                "work_order_id": work_order_id,
                "user_email": work_order["new_user_email"],
                "group_name": work_order["group_name"],
                "review_date": review_date.isoformat(),
                "status": "scheduled"
            }
    
    return {
        "status": "success",
        "message": f"Work order {work_order_id} closed successfully with status: {completion_status}",
        "work_order_id": work_order_id,
        "completion_notes": notes
    }

def list_pending_requests(requester_email: Optional[str] = None) -> Dict[str, Any]:
    """
    Lists pending service requests, optionally filtered by requester.
    
    Args:
        requester_email: Optional filter by requester email
    
    Returns:
        List of pending requests
    """
    pending_requests = []
    for request_id, request in mock_service_requests.items():
        if request["status"] in ["pending_approval", "approved", "in_progress"]:
            if requester_email is None or request["requester_email"] == requester_email:
                pending_requests.append({
                    "request_id": request_id,
                    "group_name": request["group_name"],
                    "new_user_email": request["new_user_email"],
                    "status": request["status"],
                    "created_at": request["created_at"]
                })
    
    return {
        "status": "success",
        "pending_requests": pending_requests,
        "count": len(pending_requests)
    }

# Enhanced Active Directory Agent Tools
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
        Membership verification result with group details
    """
    if group_name not in mock_ad_groups:
        return {
            "status": "error",
            "message": f"AD group '{group_name}' not found",
            "available_groups": list(mock_ad_groups.keys())
        }
    
    group_info = mock_ad_groups[group_name]
    is_member = user_email in group_info["members"]
    
    return {
        "status": "success",
        "is_member": is_member,
        "group_name": group_name,
        "user_email": user_email,
        "group_description": group_info["description"],
        "total_members": len(group_info["members"]),
        "message": f"User {user_email} {'is' if is_member else 'is not'} a member of {group_name}"
    }

def remove_user_from_ad_group(group_name: str, user_email: str, reason: str = "") -> Dict[str, Any]:
    """
    Removes a user from an AD group with audit trail.
    
    Args:
        group_name: The AD group name
        user_email: The user's email address
        reason: Reason for removal
    
    Returns:
        Removal operation result
    """
    if group_name not in mock_ad_groups:
        return {
            "status": "error",
            "message": f"AD group '{group_name}' not found"
        }
    
    if user_email in mock_ad_groups[group_name]["members"]:
        mock_ad_groups[group_name]["members"].remove(user_email)
        
        return {
            "status": "success",
            "message": f"Successfully removed {user_email} from {group_name} AD group",
            "group_name": group_name,
            "user_email": user_email,
            "reason": reason,
            "removed_at": datetime.now().isoformat()
        }
    else:
        return {
            "status": "info",
            "message": f"User {user_email} is not a member of {group_name}",
            "group_name": group_name,
            "user_email": user_email
        }

def list_ad_groups() -> Dict[str, Any]:
    """
    Lists all available AD groups with their details.
    
    Returns:
        List of AD groups with metadata
    """
    groups = []
    for group_name, group_info in mock_ad_groups.items():
        groups.append({
            "group_name": group_name,
            "description": group_info["description"],
            "owner": group_info["owner"],
            "member_count": len(group_info["members"])
        })
    
    return {
        "status": "success",
        "groups": groups,
        "total_groups": len(groups)
    }

# Create Simple ServiceNow Agent
servicenow_agent = LlmAgent(
    model=GEMINI_2_FLASH,
    name="servicenow_agent",
    instruction="""You are a ServiceNow Agent responsible for managing service requests and work orders for AD group access.

Your responsibilities:
1. Create service requests for AD group owner approval
2. Check approval status and create work orders when approved
3. Close work orders after AD operations are completed
4. List and manage pending requests

When creating service requests:
- Always validate that the AD group exists and show available groups if not found
- Send approval requests to the appropriate group owner
- Provide clear feedback on the request status

When checking approval status:
- Monitor for approvals and automatically create work orders
- Track approval details including who approved and when
- Return status information

When closing work orders:
- Mark work orders as completed with status
- Update related service requests to completed status
- Maintain audit trail

Always provide clear status updates and next steps.""",
    description="Enhanced ServiceNow Agent for managing service requests and work orders with advanced security and tracking",
    tools=[
        FunctionTool(func=create_service_request),
        FunctionTool(func=get_approval_status),
        FunctionTool(func=close_work_order),
        FunctionTool(func=list_pending_requests)
    ],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)

# Create Enhanced Active Directory Agent
ad_agent = LlmAgent(
    model=GEMINI_2_FLASH,
    name="ad_agent", 
    instruction="""You are an Enhanced Active Directory Agent responsible for managing user access to AD groups with advanced security features.

Your responsibilities:
1. Add users to AD groups based on approved work orders with expiration validation
2. Verify group memberships with detailed group information
3. Remove users from groups with audit trail
4. List available AD groups with comprehensive metadata
5. Ensure proper access control and security compliance

Enhanced Features:
- Access expiration validation before granting access
- Comprehensive group metadata including sensitivity levels
- User removal capabilities with reason tracking
- Detailed membership verification with group context
- Security-conscious operation validation

When adding users to groups:
- Only process approved work orders that haven't expired
- Validate that both the user and group exist
- Check access expiration before granting access
- Add the user to the specified group with timestamp tracking
- Report detailed success/failure status back to the orchestrator

When verifying memberships:
- Check if users are already members of groups
- Provide detailed group information including sensitivity level
- Return comprehensive membership status with context

When removing users:
- Remove users from specified groups with reason tracking
- Maintain audit trail of removal operations
- Validate group and user existence before removal

When listing groups:
- Provide comprehensive group metadata
- Include sensitivity levels, approval requirements, and member counts
- Support filtering and search capabilities

Always follow security best practices, validate all operations, and provide detailed operation results with security context.""",
    description="Enhanced Active Directory Agent for managing group memberships with advanced security and audit capabilities",
    tools=[
        FunctionTool(func=add_user_to_ad_group),
        FunctionTool(func=verify_ad_group_membership),
        FunctionTool(func=remove_user_from_ad_group),
        FunctionTool(func=list_ad_groups)
    ],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)

# Create Simple Access Workflow Orchestrator Agent
access_workflow_orchestrator = LlmAgent(
    model=GEMINI_2_FLASH,
    name="access_workflow_orchestrator",
    instruction="""You are the Access Workflow Orchestrator Agent - a sub-orchestrator that manages the process for granting access to AD groups. You coordinate between ServiceNow and Active Directory agents.

SIMPLE WORKFLOW PROCESS:
1. When a user requests to be added to an AD group:
   - Transfer to ServiceNow agent to create a service request
   - Monitor approval process and provide status updates
   
2. Once work order is created:
   - Transfer to AD agent to add user to the group
   - Wait for AD operation completion
   
3. After AD operation:
   - Transfer back to ServiceNow agent to close the work order
   - Provide final status to the user

TRANSFER RULES:
- For service request creation and work order management: transfer to servicenow_agent
- For AD group operations and membership verification: transfer to ad_agent
- Always coordinate the complete workflow from start to finish
- Provide clear status updates throughout the process

Handle requests like:
- "Add [user] to [group]"
- "I need access to [group]"
- "Please add [email] to [group]"
- "Check my pending access requests"
- "List available groups I can request access to"

Always ensure the complete workflow is executed and provide clear status updates.""",
    description="Enhanced Access Workflow Orchestrator that manages secure, multi-step processes for AD group access with advanced security and compliance features",
    sub_agents=[servicenow_agent, ad_agent]
)

# Session and Runner setup
session_service = InMemorySessionService()
runner = Runner(
    agent=access_workflow_orchestrator,
    app_name="access_workflow_orchestrator_app",
    session_service=session_service
)

# Export for ADK CLI compatibility
agent = access_workflow_orchestrator

def process_access_request(user_input: str, user_id: str = "default_user") -> str:
    """
    Process an access request through the enhanced multi-agent system.
    
    Args:
        user_input: The user's access request
        user_id: Unique identifier for the user
    
    Returns:
        Final response from the agent system
    """
    # Create or get session
    session_id = f"access_session_{user_id}"
    
    # Check if session exists, if not create it
    session = None
    try:
        session = session_service.get_session(
            app_name="access_workflow_orchestrator_app",
            user_id=user_id,
            session_id=session_id
        )
    except:
        # Session doesn't exist, create a new one
        pass
    
    if session is None:
        session = session_service.create_session(
            app_name="access_workflow_orchestrator_app",
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

# Test function for the enhanced system
def test_enhanced_workflow():
    """Test the enhanced workflow with various security scenarios."""
    print("=== Testing Enhanced Access Workflow Orchestrator ===\n")
    
    test_cases = [
        "I need to add john.new@company.com to the finance_team group for quarterly reporting",
        "Please add sarah.dev@company.com to engineering_team for the new project",
        "Can you help me get access to admin_group for system maintenance?",
        "Add mike.marketing@company.com to marketing_team",
        "List all available groups I can request access to",
        "Check the status of my pending access requests"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test Case {i}: {test_case}")
        print("-" * 60)
        
        response = process_access_request(test_case, f"test_user_{i}")
        print(f"Response: {response}")
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    # Run enhanced tests
    test_enhanced_workflow()
    
    # Interactive mode
    print("Enhanced Interactive Mode - Enter your access requests (type 'quit' to exit):")
    print("Available commands:")
    print("- Request access: 'Add [user] to [group] for [reason]'")
    print("- List groups: 'List available groups'")
    print("- Check status: 'Check my pending requests'")
    print("- Verify membership: 'Check if [user] is in [group]'")
    print()
    
    while True:
        user_input = input("\nUser: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        if user_input:
            response = process_access_request(user_input, "interactive_user")
            print(f"Access Orchestrator: {response}")
