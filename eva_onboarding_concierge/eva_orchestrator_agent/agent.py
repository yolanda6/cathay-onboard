"""
Eva Orchestrator Agent - Enhanced Version
The primary conversational AI that manages the end-to-end user experience.
Acts as the "General Manager" coordinating all specialist sub-agents.
"""

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

# Import centralized configuration with fallback
try:
    from eva_onboarding_concierge.shared_libraries.config import GEMINI_MODEL, PROJECT_ID, LOCATION
    from eva_onboarding_concierge.shared_libraries.constants import (
        AgentNames, OnboardingStatus, DEFAULT_ONBOARDING_DURATION_DAYS,
        SYSTEM_MESSAGES, RESPONSE_TEMPLATES
    )
    from eva_onboarding_concierge.eva_orchestrator_agent.prompt import EVA_ORCHESTRATOR_INSTRUCTION
except ImportError:
    # Fallback to relative imports when running as individual agent
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        from ..shared_libraries.config import GEMINI_MODEL, PROJECT_ID, LOCATION
        from ..shared_libraries.constants import (
            AgentNames, OnboardingStatus, DEFAULT_ONBOARDING_DURATION_DAYS,
            SYSTEM_MESSAGES, RESPONSE_TEMPLATES
        )
        from .prompt import EVA_ORCHESTRATOR_INSTRUCTION
    except ImportError:
        # Final fallback to hardcoded values
        import os
        GEMINI_MODEL = "gemini-2.0-flash-exp"
        PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "vital-octagon-19612")
        LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        
        class AgentNames:
            EVA_ORCHESTRATOR = "eva_onboarding_concierge"
            ID_MASTER = "id_master"
            DEVICE_DEPOT = "device_depot"
            ACCESS_WORKFLOW_ORCHESTRATOR = "access_workflow_orchestrator"
            HR_HELPER = "hr_helper"
            MEETING_MAVEN = "meeting_maven"
        
        class OnboardingStatus:
            PENDING = "pending"
            IN_PROGRESS = "in_progress"
            COMPLETED = "completed"
            BLOCKED = "blocked"
            CANCELLED = "cancelled"
        
        DEFAULT_ONBOARDING_DURATION_DAYS = 3
        SYSTEM_MESSAGES = {}
        RESPONSE_TEMPLATES = {}
        
        EVA_ORCHESTRATOR_INSTRUCTION = """You are Eva, the AI Onboarding Concierge - a sophisticated orchestration agent that provides a seamless, "white-glove" onboarding experience for new employees. You act as the "General Manager," understanding employee needs and delegating tasks to the appropriate specialist agents.

IDENTITY CONFIRMATION:
I am Eva, your dedicated AI Onboarding Concierge. When users ask "Who are you?" or "What can you do?", I should clearly identify myself as Eva and explain my role in orchestrating the complete employee onboarding experience.

Your primary role is to coordinate a team of specialist sub-agents to handle everything from identity creation and IT provisioning to secure access requests and HR questions, demonstrating a massive leap in efficiency and employee satisfaction.

SPECIALIST AGENTS UNDER YOUR COORDINATION:
1. ID Master Agent - Creates and manages digital identities and Active Directory accounts
2. Device Depot Agent - Handles IT equipment requests and deployments
3. Access Workflow Orchestrator Agent - Manages secure access to AD groups and systems
4. HR Helper Agent - Answers HR questions using company policy documents
5. Meeting Maven Agent - Schedules meetings and manages calendar coordination

ONBOARDING WORKFLOW ORCHESTRATION:
When a new employee onboarding request comes in:

1. INITIAL SETUP (Identity & Access):
   - Transfer to ID Master to create user accounts, email, and basic credentials
   - Transfer to Access Workflow Orchestrator for department-specific group access
   - Ensure all identity management is complete before proceeding

2. EQUIPMENT PROVISIONING:
   - Transfer to Device Depot to request and schedule equipment delivery
   - Coordinate delivery timing with employee start date
   - Ensure equipment is ready for day one

3. HR COORDINATION:
   - Transfer to HR Helper for policy information and orientation scheduling
   - Provide answers to common HR questions
   - Coordinate benefits enrollment and paperwork

4. MEETING COORDINATION:
   - Transfer to Meeting Maven to schedule welcome meetings
   - Arrange manager meetings, team introductions, and buddy sessions
   - Coordinate first week schedule

5. PROGRESS TRACKING:
   - Monitor completion of all onboarding tasks
   - Update checklist items as they're completed
   - Provide status updates and progress reports

INTRODUCTION PROTOCOL:
When users first interact with me or ask about my capabilities, I should introduce myself as:
"Hi! I'm Eva, your AI Onboarding Concierge. I'm here to make employee onboarding seamless and delightful. I coordinate with a team of specialist agents to handle everything from identity management and IT equipment to access permissions and HR questions. How can I help you today?"

ROUTING RULES:
- For identity/account creation: transfer to id_master
- For equipment requests: transfer to device_depot  
- For access permissions: transfer to access_workflow_orchestrator
- For HR questions/policies: transfer to hr_helper
- For meeting scheduling: transfer to meeting_maven

COMMUNICATION STYLE:
- Be warm, professional, and welcoming
- Provide clear explanations of what's happening
- Give realistic timelines and expectations
- Proactively communicate progress and next steps
- Address concerns with empathy and solutions

ONBOARDING BEST PRACTICES:
- Start with identity management as the foundation
- Coordinate equipment delivery for day one readiness
- Schedule key meetings within the first week
- Ensure all access is properly configured and tested
- Provide comprehensive status updates to managers
- Follow up to ensure smooth transition

Always maintain a comprehensive view of the entire onboarding process and ensure nothing falls through the cracks. You are the single point of contact that makes onboarding effortless and delightful."""

# Import sub-agents
try:
    from eva_onboarding_concierge.access_workflow_orchestrator_agent.agent import access_workflow_orchestrator
    from eva_onboarding_concierge.id_master_agent.agent import id_master
    from eva_onboarding_concierge.device_depot_agent.agent import device_depot
    from eva_onboarding_concierge.hr_helper_agent.agent import hr_helper
    from eva_onboarding_concierge.meeting_maven_agent.agent import meeting_maven
except ImportError:
    # Fallback to relative imports when running as individual agent
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from access_workflow_orchestrator_agent.agent import access_workflow_orchestrator
    from id_master_agent.agent import id_master
    from device_depot_agent.agent import device_depot
    from hr_helper_agent.agent import hr_helper
    from meeting_maven_agent.agent import meeting_maven

# Mock onboarding database
mock_onboarding_sessions = {}
mock_employee_profiles = {}

# Eva Orchestrator Tools
def start_onboarding_session(employee_name: str, employee_email: str, department: str,
                           job_title: str, start_date: str, manager_email: Optional[str] = None,
                           buddy_email: Optional[str] = None) -> Dict[str, Any]:
    """
    Starts a comprehensive onboarding session for a new employee.
    
    Args:
        employee_name: Full name of the new employee
        employee_email: Email address of the new employee
        department: Employee's department
        job_title: Employee's job title
        start_date: Employee's start date (YYYY-MM-DD)
        manager_email: Manager's email address
        buddy_email: Buddy's email address for mentoring
    
    Returns:
        Onboarding session details and checklist
    """
    try:
        session_id = f"ONBOARD-{uuid.uuid4().hex[:8].upper()}"
        
        # Create comprehensive onboarding checklist
        onboarding_checklist = {
            "identity_management": {
                "status": "pending",
                "tasks": [
                    "Create Active Directory account",
                    "Set up email account",
                    "Generate access credentials",
                    "Assign security groups"
                ]
            },
            "equipment_provisioning": {
                "status": "pending", 
                "tasks": [
                    "Request laptop and accessories",
                    "Schedule equipment delivery",
                    "Configure software and security"
                ]
            },
            "access_management": {
                "status": "pending",
                "tasks": [
                    "Request department group access",
                    "Set up VPN and building access",
                    "Configure application permissions"
                ]
            },
            "hr_orientation": {
                "status": "pending",
                "tasks": [
                    "Complete HR paperwork",
                    "Review company policies",
                    "Set up benefits enrollment",
                    "Schedule orientation meetings"
                ]
            },
            "meeting_coordination": {
                "status": "pending",
                "tasks": [
                    "Schedule welcome meeting with manager",
                    "Arrange team introduction sessions",
                    "Set up buddy system meetings",
                    "Plan first week schedule"
                ]
            }
        }
        
        # Create employee profile
        employee_profile = {
            "employee_name": employee_name,
            "employee_email": employee_email,
            "department": department,
            "job_title": job_title,
            "start_date": start_date,
            "manager_email": manager_email,
            "buddy_email": buddy_email,
            "onboarding_status": "in_progress",
            "created_date": datetime.now().isoformat()
        }
        
        # Create onboarding session
        onboarding_session = {
            "session_id": session_id,
            "employee_profile": employee_profile,
            "checklist": onboarding_checklist,
            "status": "active",
            "created_date": datetime.now().isoformat(),
            "estimated_completion": (datetime.now() + timedelta(days=3)).isoformat(),
            "progress_percentage": 0
        }
        
        mock_onboarding_sessions[session_id] = onboarding_session
        mock_employee_profiles[employee_email] = employee_profile
        
        return {
            "status": "success",
            "session_id": session_id,
            "message": f"Onboarding session started for {employee_name}",
            "employee_profile": employee_profile,
            "checklist_summary": {
                "total_categories": len(onboarding_checklist),
                "total_tasks": sum(len(cat["tasks"]) for cat in onboarding_checklist.values()),
                "estimated_completion": onboarding_session["estimated_completion"]
            },
            "next_steps": [
                "Eva will coordinate with specialist agents",
                "Identity and access management will be set up first",
                "Equipment provisioning will be initiated",
                "Meetings will be scheduled with key stakeholders"
            ]
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to start onboarding session: {e}",
            "employee_details": {
                "name": employee_name,
                "email": employee_email,
                "department": department
            }
        }

def get_onboarding_status(session_id: Optional[str] = None, employee_email: Optional[str] = None, employee_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Gets the current status of an onboarding session.
    
    Args:
        session_id: The onboarding session ID
        employee_email: Alternative lookup by employee email
        employee_name: Alternative lookup by employee name
    
    Returns:
        Current onboarding status and progress
    """
    # Find session by ID, email, or name
    target_session = None
    if session_id and session_id in mock_onboarding_sessions:
        target_session = mock_onboarding_sessions[session_id]
    elif employee_email:
        for sid, session in mock_onboarding_sessions.items():
            if session["employee_profile"]["employee_email"] == employee_email:
                target_session = session
                session_id = sid
                break
    elif employee_name:
        for sid, session in mock_onboarding_sessions.items():
            if session["employee_profile"]["employee_name"].lower() == employee_name.lower():
                target_session = session
                session_id = sid
                break
    
    if not target_session:
        return {
            "status": "error",
            "message": f"Onboarding session not found",
            "search_criteria": {
                "session_id": session_id,
                "employee_email": employee_email
            }
        }
    
    # Calculate progress
    checklist = target_session["checklist"]
    completed_categories = sum(1 for cat in checklist.values() if cat["status"] == "completed")
    total_categories = len(checklist)
    progress_percentage = (completed_categories / total_categories) * 100
    
    # Update progress in session
    target_session["progress_percentage"] = progress_percentage
    
    return {
        "status": "success",
        "session_id": session_id,
        "employee_profile": target_session["employee_profile"],
        "progress": {
            "percentage": progress_percentage,
            "completed_categories": completed_categories,
            "total_categories": total_categories,
            "estimated_completion": target_session["estimated_completion"]
        },
        "checklist_status": checklist,
        "overall_status": target_session["status"]
    }

def update_checklist_item(session_id: str, category: str, status: str, 
                         notes: str = "") -> Dict[str, Any]:
    """
    Updates the status of a checklist category.
    
    Args:
        session_id: The onboarding session ID
        category: The checklist category to update
        status: New status (pending, in_progress, completed, blocked)
        notes: Additional notes about the update
    
    Returns:
        Update confirmation and new status
    """
    if session_id not in mock_onboarding_sessions:
        return {
            "status": "error",
            "message": f"Onboarding session {session_id} not found"
        }
    
    session = mock_onboarding_sessions[session_id]
    checklist = session["checklist"]
    
    if category not in checklist:
        return {
            "status": "error",
            "message": f"Checklist category '{category}' not found",
            "available_categories": list(checklist.keys())
        }
    
    # Update category status
    old_status = checklist[category]["status"]
    checklist[category]["status"] = status
    checklist[category]["updated_date"] = datetime.now().isoformat()
    if notes:
        checklist[category]["notes"] = notes
    
    # Recalculate overall progress
    completed_categories = sum(1 for cat in checklist.values() if cat["status"] == "completed")
    total_categories = len(checklist)
    progress_percentage = (completed_categories / total_categories) * 100
    session["progress_percentage"] = progress_percentage
    
    # Check if onboarding is complete
    if progress_percentage == 100:
        session["status"] = "completed"
        session["completed_date"] = datetime.now().isoformat()
    
    return {
        "status": "success",
        "session_id": session_id,
        "category": category,
        "status_change": f"{old_status} → {status}",
        "notes": notes,
        "progress_percentage": progress_percentage,
        "onboarding_complete": session["status"] == "completed"
    }

def generate_onboarding_summary(session_id: str) -> Dict[str, Any]:
    """
    Generates a comprehensive onboarding summary report.
    
    Args:
        session_id: The onboarding session ID
    
    Returns:
        Detailed onboarding summary and recommendations
    """
    if session_id not in mock_onboarding_sessions:
        return {
            "status": "error",
            "message": f"Onboarding session {session_id} not found"
        }
    
    session = mock_onboarding_sessions[session_id]
    employee = session["employee_profile"]
    checklist = session["checklist"]
    
    # Analyze completion status
    completed_items = []
    pending_items = []
    blocked_items = []
    
    for category, details in checklist.items():
        if details["status"] == "completed":
            completed_items.append(category)
        elif details["status"] == "blocked":
            blocked_items.append(category)
        else:
            pending_items.append(category)
    
    # Calculate timeline
    created_date = datetime.fromisoformat(session["created_date"])
    current_date = datetime.now()
    days_elapsed = (current_date - created_date).days
    
    return {
        "status": "success",
        "session_id": session_id,
        "employee_summary": {
            "name": employee["employee_name"],
            "email": employee["employee_email"],
            "department": employee["department"],
            "job_title": employee["job_title"],
            "start_date": employee["start_date"]
        },
        "progress_summary": {
            "overall_progress": session["progress_percentage"],
            "days_elapsed": days_elapsed,
            "status": session["status"],
            "completed_categories": len(completed_items),
            "pending_categories": len(pending_items),
            "blocked_categories": len(blocked_items)
        },
        "detailed_status": {
            "completed": completed_items,
            "pending": pending_items,
            "blocked": blocked_items
        },
        "recommendations": [
            "Focus on completing pending items" if pending_items else "All items completed!",
            "Address blocked items immediately" if blocked_items else "No blocked items",
            "Schedule follow-up meetings with manager and buddy",
            "Ensure all access credentials are working properly"
        ]
    }

def list_active_onboarding_sessions(department: Optional[str] = None) -> Dict[str, Any]:
    """
    Lists all active onboarding sessions, optionally filtered by department.
    
    Args:
        department: Optional department filter
    
    Returns:
        List of active onboarding sessions
    """
    active_sessions = []
    
    for session_id, session in mock_onboarding_sessions.items():
        if session["status"] == "active":
            employee = session["employee_profile"]
            
            # Apply department filter if specified
            if department and employee["department"].lower() != department.lower():
                continue
            
            active_sessions.append({
                "session_id": session_id,
                "employee_name": employee["employee_name"],
                "employee_email": employee["employee_email"],
                "department": employee["department"],
                "job_title": employee["job_title"],
                "start_date": employee["start_date"],
                "progress_percentage": session["progress_percentage"],
                "created_date": session["created_date"]
            })
    
    # Sort by creation date (newest first)
    active_sessions.sort(key=lambda x: x["created_date"], reverse=True)
    
    return {
        "status": "success",
        "active_sessions": active_sessions,
        "total_count": len(active_sessions),
        "department_filter": department
    }

# Create Eva Orchestrator Agent
eva_orchestrator = LlmAgent(
    model=GEMINI_MODEL,
    name=AgentNames.EVA_ORCHESTRATOR,
    instruction=EVA_ORCHESTRATOR_INSTRUCTION,
    description="Eva - AI Onboarding Concierge that orchestrates comprehensive employee onboarding through specialist agents",
    tools=[
        FunctionTool(func=start_onboarding_session),
        FunctionTool(func=get_onboarding_status),
        FunctionTool(func=update_checklist_item),
        FunctionTool(func=generate_onboarding_summary),
        FunctionTool(func=list_active_onboarding_sessions)
    ],
    sub_agents=[
        id_master,
        device_depot,
        access_workflow_orchestrator,
        hr_helper,
        meeting_maven
    ]
)

# Session and Runner setup
session_service = InMemorySessionService()
runner = Runner(
    agent=eva_orchestrator,
    app_name="eva_orchestrator_app",
    session_service=session_service
)

# Export for ADK CLI compatibility
agent = eva_orchestrator
root_agent = eva_orchestrator

def process_onboarding_request(user_input: str, user_id: str = "default_user") -> str:
    """
    Process an onboarding request through the Eva system.
    
    Args:
        user_input: The onboarding request or question
        user_id: Unique identifier for the user
    
    Returns:
        Final response from Eva
    """
    # Create or get session
    session_id = f"eva_session_{user_id}"
    
    # Check if session exists, if not create it
    session = None
    try:
        session = session_service.get_session(
            app_name="eva_orchestrator_app",
            user_id=user_id,
            session_id=session_id
        )
    except:
        # Session doesn't exist, create a new one
        pass
    
    if session is None:
        session = session_service.create_session(
            app_name="eva_orchestrator_app",
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
def test_eva_system():
    """Test the complete Eva onboarding system."""
    print("=== Testing Eva Onboarding Concierge System ===\n")
    
    test_cases = [
        "Hi Eva! I need to onboard a new employee named Alex Johnson who is starting as a Software Developer in the Engineering department on Monday. His email will be alex.johnson@company.com and his manager is manager@company.com",
        "What's the status of Alex Johnson's onboarding?",
        "Alex needs a MacBook Pro and monitor for his work setup",
        "Can you schedule a welcome meeting between Alex and his manager for his first day?",
        "Alex has questions about the company's vacation policy",
        "What access does Alex need for the Engineering team?",
        "Generate a summary of Alex's onboarding progress"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test Case {i}: {test_case}")
        print("-" * 60)
        
        response = process_onboarding_request(test_case, f"test_user_{i}")
        print(f"Eva: {response}")
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    # Run tests
    test_eva_system()
    
    # Interactive mode
    print("Eva Onboarding Concierge - Interactive Mode (type 'quit' to exit):")
    print("Hi! I'm Eva, your AI Onboarding Concierge. I can help you with:")
    print("- Starting new employee onboarding")
    print("- Checking onboarding progress")
    print("- Coordinating IT equipment and access")
    print("- Scheduling meetings and orientation")
    print("- Answering HR policy questions")
    print("- Managing the complete onboarding experience")
    print()
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        if user_input:
            response = process_onboarding_request(user_input, "interactive_user")
            print(f"Eva: {response}")
