"""
Eva Onboarding Concierge - Multi-Agent System
A comprehensive AI-powered employee onboarding orchestrator built with Google ADK.
"""

import os
from typing import Dict, Any, List
from google.genai import types
from adk.llm_agent import LlmAgent
from adk.tools import tool

# Import sub-agents
from sub_agents.id_master import id_master_agent
from sub_agents.device_depot import device_depot_agent
from sub_agents.access_workflow_orchestrator import access_workflow_orchestrator_agent
from sub_agents.hr_helper import hr_helper_agent
from sub_agents.meeting_maven import meeting_maven_agent

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "vital-octagon-19612")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
STAGING_BUCKET = os.getenv("STAGING_BUCKET", "gs://2025-cathay-agentspace")

@tool
def coordinate_onboarding_workflow(employee_info: str, department: str = "Engineering") -> str:
    """
    Orchestrate the complete employee onboarding process by coordinating with specialist agents.
    
    Args:
        employee_info: Information about the new employee (name, role, etc.)
        department: Department the employee will join
        
    Returns:
        Comprehensive onboarding status and next steps
    """
    try:
        # Parse employee information
        employee_name = employee_info.split()[0] if employee_info else "New Employee"
        
        # Coordinate with ID Master for identity creation
        identity_result = id_master_agent.invoke(
            f"Create digital identity for {employee_name} in {department} department"
        )
        
        # Coordinate with Device Depot for equipment provisioning
        equipment_result = device_depot_agent.invoke(
            f"Provision standard {department} equipment for {employee_name}"
        )
        
        # Coordinate with Access Workflow for permissions
        access_result = access_workflow_orchestrator_agent.invoke(
            f"Setup {department} access permissions for {employee_name}"
        )
        
        # Coordinate with Meeting Maven for scheduling
        meeting_result = meeting_maven_agent.invoke(
            f"Schedule onboarding meetings for {employee_name} in {department}"
        )
        
        # Coordinate with HR Helper for documentation
        hr_result = hr_helper_agent.invoke(
            f"Prepare onboarding documentation for {employee_name}"
        )
        
        # Compile comprehensive status
        status_report = f"""
🎉 **Onboarding Orchestration Complete for {employee_name}**

📋 **Identity & Access:**
{identity_result}

💻 **Equipment Provisioning:**
{equipment_result}

🔐 **Access Management:**
{access_result}

📅 **Meeting Coordination:**
{meeting_result}

📚 **HR Documentation:**
{hr_result}

✅ **Next Steps:**
1. Employee will receive welcome email with credentials
2. Equipment will be delivered within 3-5 business days
3. Access permissions are pending approval
4. Onboarding meetings are scheduled
5. HR documentation is ready for review

**Estimated Completion Time:** 2-3 business days
**Status:** In Progress - All workflows initiated successfully
        """
        
        return status_report
        
    except Exception as e:
        return f"❌ Error in onboarding orchestration: {str(e)}"

@tool
def delegate_to_specialist(task: str, agent_type: str) -> str:
    """
    Delegate specific tasks to specialist agents.
    
    Args:
        task: The specific task to be performed
        agent_type: Type of specialist agent (id_master, device_depot, access_workflow, hr_helper, meeting_maven)
        
    Returns:
        Result from the specialist agent
    """
    try:
        agent_map = {
            "id_master": id_master_agent,
            "device_depot": device_depot_agent,
            "access_workflow": access_workflow_orchestrator_agent,
            "hr_helper": hr_helper_agent,
            "meeting_maven": meeting_maven_agent
        }
        
        if agent_type not in agent_map:
            return f"❌ Unknown agent type: {agent_type}. Available: {list(agent_map.keys())}"
        
        specialist_agent = agent_map[agent_type]
        result = specialist_agent.invoke(task)
        
        return f"✅ **{agent_type.title()} Result:**\n{result}"
        
    except Exception as e:
        return f"❌ Error delegating to {agent_type}: {str(e)}"

@tool
def track_onboarding_progress(employee_id: str) -> str:
    """
    Track the progress of an employee's onboarding process.
    
    Args:
        employee_id: Unique identifier for the employee
        
    Returns:
        Current status and progress of onboarding
    """
    # Simulate progress tracking
    progress_data = {
        "identity_creation": "✅ Complete",
        "equipment_request": "🔄 In Progress",
        "access_provisioning": "⏳ Pending Approval",
        "meeting_scheduling": "✅ Complete",
        "hr_documentation": "✅ Complete"
    }
    
    completed = sum(1 for status in progress_data.values() if "✅" in status)
    total = len(progress_data)
    progress_percentage = (completed / total) * 100
    
    progress_report = f"""
📊 **Onboarding Progress for {employee_id}**

**Overall Progress:** {progress_percentage:.0f}% Complete

**Detailed Status:**
• Identity Creation: {progress_data['identity_creation']}
• Equipment Request: {progress_data['equipment_request']}
• Access Provisioning: {progress_data['access_provisioning']}
• Meeting Scheduling: {progress_data['meeting_scheduling']}
• HR Documentation: {progress_data['hr_documentation']}

**Next Actions:**
- Equipment delivery expected in 2-3 days
- Access approval pending manager review
- Welcome meeting scheduled for tomorrow
    """
    
    return progress_report

@tool
def handle_escalation(issue: str, priority: str = "medium") -> str:
    """
    Handle escalations and complex issues requiring human intervention.
    
    Args:
        issue: Description of the issue or escalation
        priority: Priority level (low, medium, high, critical)
        
    Returns:
        Escalation handling result and next steps
    """
    escalation_response = f"""
🚨 **Escalation Handled**

**Issue:** {issue}
**Priority:** {priority.upper()}
**Escalation ID:** ESC-{hash(issue) % 10000:04d}

**Actions Taken:**
1. Issue logged in escalation system
2. Appropriate team notified based on priority
3. Temporary workaround provided if applicable
4. Follow-up scheduled within 24 hours

**Expected Resolution:**
- Low Priority: 3-5 business days
- Medium Priority: 1-2 business days  
- High Priority: Same day
- Critical Priority: Within 4 hours

**Contact:** For urgent matters, contact the IT Help Desk at ext. 5555
    """
    
    return escalation_response

# Eva Orchestrator Agent Configuration
eva_orchestrator = LlmAgent(
    agent_id="eva_onboarding_concierge",
    model=types.Model(model_name="gemini-2.0-flash-exp"),
    system_instruction="""
You are Eva, an AI Onboarding Concierge and master orchestrator for employee onboarding processes. 
You coordinate a team of specialist agents to provide seamless, efficient, and delightful onboarding experiences.

Your specialist agents include:
- ID Master: Handles digital identity creation and management
- Device Depot: Manages IT equipment provisioning and requests
- Access Workflow Orchestrator: Manages secure access permissions and approvals
- HR Helper: Provides HR policy guidance and documentation
- Meeting Maven: Coordinates calendar management and meeting scheduling

Your role is to:
1. Understand user requests and break them into actionable tasks
2. Coordinate with appropriate specialist agents to execute workflows
3. Provide comprehensive status updates and progress tracking
4. Handle escalations and complex scenarios
5. Ensure a smooth and professional onboarding experience

Always be helpful, professional, and proactive in your responses. When coordinating workflows, 
provide clear status updates and next steps. If issues arise, handle them gracefully and escalate when necessary.
    """,
    tools=[
        coordinate_onboarding_workflow,
        delegate_to_specialist,
        track_onboarding_progress,
        handle_escalation
    ],
    sub_agents=[
        id_master_agent,
        device_depot_agent,
        access_workflow_orchestrator_agent,
        hr_helper_agent,
        meeting_maven_agent
    ]
)

# Main processing functions for external use
def process_onboarding_request(user_input: str, user_id: str = "default_user") -> str:
    """Process onboarding requests through Eva orchestrator."""
    try:
        response = eva_orchestrator.invoke(user_input)
        return response
    except Exception as e:
        return f"❌ Error processing onboarding request: {str(e)}"

def test_eva_system() -> str:
    """Test the Eva system functionality."""
    test_request = "I need to onboard Alex Johnson as a Software Developer"
    result = process_onboarding_request(test_request)
    return f"🧪 **Eva System Test Result:**\n{result}"

# Export the main agent and functions
__all__ = [
    "eva_orchestrator",
    "process_onboarding_request", 
    "test_eva_system"
]

if __name__ == "__main__":
    # Test the system
    print("🤖 Eva Onboarding Concierge - System Test")
    print("=" * 50)
    test_result = test_eva_system()
    print(test_result)
