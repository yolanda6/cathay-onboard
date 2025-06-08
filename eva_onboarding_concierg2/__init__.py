"""
Eva Onboarding Concierge - AI-Powered Employee Onboarding System
A comprehensive multi-agent system built with Google's Agent Development Kit (ADK).
"""

from .eva_orchestrator_agent.agent import eva_orchestrator, process_onboarding_request
from .access_workflow_orchestrator_agent.agent import access_workflow_orchestrator, process_access_request
from .id_master_agent.agent import id_master, process_identity_request
from .device_depot_agent.agent import device_depot, process_equipment_request
from .hr_helper_agent.agent import hr_helper, process_hr_question
from .meeting_maven_agent.agent import meeting_maven, process_meeting_request

# Export main agent for ADK CLI compatibility
agent = eva_orchestrator
root_agent = eva_orchestrator

__version__ = "1.0.0"
__author__ = "Google ADK Team"
__description__ = "Eva - Your AI Onboarding Concierge"

# Main agents
__all__ = [
    # ADK CLI compatibility
    'agent',
    'root_agent',
    
    # Main orchestrator
    'eva_orchestrator',
    'process_onboarding_request',
    
    # Specialist agents
    'access_workflow_orchestrator',
    'process_access_request',
    'id_master', 
    'process_identity_request',
    'device_depot',
    'process_equipment_request',
    'hr_helper',
    'process_hr_question',
    'meeting_maven',
    'process_meeting_request'
]

# System information
SYSTEM_INFO = {
    "name": "Eva Onboarding Concierge",
    "version": __version__,
    "description": __description__,
    "agents": {
        "eva_orchestrator": "Main orchestration agent that coordinates all onboarding activities",
        "access_workflow_orchestrator": "Manages secure access to AD groups and systems",
        "id_master": "Creates and manages digital identities and Active Directory accounts",
        "device_depot": "Handles IT equipment requests and deployments",
        "hr_helper": "Answers HR questions using company policy documents",
        "meeting_maven": "Schedules meetings and manages calendar coordination"
    },
    "capabilities": [
        "Complete employee onboarding orchestration",
        "Identity and access management",
        "IT equipment provisioning",
        "HR policy assistance",
        "Meeting scheduling and coordination",
        "Progress tracking and reporting"
    ]
}

def get_system_info():
    """Returns system information and capabilities."""
    return SYSTEM_INFO

def start_eva_demo():
    """Starts an interactive demo of the Eva system."""
    print("=" * 60)
    print("🤖 Welcome to Eva - Your AI Onboarding Concierge!")
    print("=" * 60)
    print(f"Version: {__version__}")
    print(f"Description: {__description__}")
    print()
    print("Available Agents:")
    for agent_name, description in SYSTEM_INFO["agents"].items():
        print(f"  • {agent_name}: {description}")
    print()
    print("System Capabilities:")
    for capability in SYSTEM_INFO["capabilities"]:
        print(f"  ✓ {capability}")
    print()
    print("To start using Eva, try:")
    print("  from eva_onboarding_concierge import process_onboarding_request")
    print("  response = process_onboarding_request('Hi Eva, I need to onboard a new employee')")
    print()
