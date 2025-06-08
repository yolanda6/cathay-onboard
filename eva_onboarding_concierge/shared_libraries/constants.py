"""
Shared Constants for Eva Onboarding Concierge
Common constants and enums used across all agents.
"""

from enum import Enum
from typing import Dict, List

class AgentNames:
    """Standard agent names used throughout the system."""
    EVA_ORCHESTRATOR = "eva_onboarding_concierge"
    ID_MASTER = "id_master"
    DEVICE_DEPOT = "device_depot"
    ACCESS_WORKFLOW_ORCHESTRATOR = "access_workflow_orchestrator"
    HR_HELPER = "hr_helper"
    MEETING_MAVEN = "meeting_maven"

class OnboardingStatus:
    """Standard onboarding status values."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

class RequestStatus:
    """Standard request status values."""
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class EquipmentTypes:
    """Standard equipment types."""
    LAPTOP = "laptop"
    MONITOR = "monitor"
    KEYBOARD = "keyboard"
    MOUSE = "mouse"
    HEADSET = "headset"
    WEBCAM = "webcam"
    DOCKING_STATION = "docking_station"
    MOBILE_PHONE = "mobile_phone"

class Departments:
    """Standard department names."""
    ENGINEERING = "engineering"
    FINANCE = "finance"
    HR = "hr"
    MARKETING = "marketing"
    SALES = "sales"
    OPERATIONS = "operations"
    LEGAL = "legal"
    ADMIN = "admin"

class ADGroups:
    """Standard Active Directory group names."""
    ENGINEERING_TEAM = "engineering_team"
    FINANCE_TEAM = "finance_team"
    HR_TEAM = "hr_team"
    MARKETING_TEAM = "marketing_team"
    ADMIN_GROUP = "admin_group"

class MeetingTypes:
    """Standard meeting types."""
    WELCOME = "welcome"
    ORIENTATION = "orientation"
    TEAM_INTRODUCTION = "team_introduction"
    ONE_ON_ONE = "one_on_one"
    TRAINING = "training"
    BUDDY_MEETING = "buddy_meeting"

# Default configurations
DEFAULT_ONBOARDING_DURATION_DAYS = 3
DEFAULT_EQUIPMENT_DELIVERY_DAYS = 2
DEFAULT_ACCESS_REVIEW_DAYS = 30

# System messages
SYSTEM_MESSAGES = {
    "welcome": "Welcome to Eva Onboarding Concierge! I'm here to make your employee onboarding seamless and delightful.",
    "error": "I encountered an issue while processing your request. Please try again or contact support.",
    "success": "Your request has been processed successfully!",
    "in_progress": "Your request is being processed. I'll keep you updated on the progress.",
}

# Agent descriptions for better coordination
AGENT_DESCRIPTIONS = {
    AgentNames.EVA_ORCHESTRATOR: "Main orchestration agent that coordinates all onboarding activities",
    AgentNames.ID_MASTER: "Creates and manages digital identities and Active Directory accounts",
    AgentNames.DEVICE_DEPOT: "Handles IT equipment requests and deployments",
    AgentNames.ACCESS_WORKFLOW_ORCHESTRATOR: "Manages secure access to AD groups and systems",
    AgentNames.HR_HELPER: "Answers HR questions using company policy documents",
    AgentNames.MEETING_MAVEN: "Schedules meetings and manages calendar coordination"
}

# Standard response templates
RESPONSE_TEMPLATES = {
    "onboarding_started": "🎉 Onboarding session started for {employee_name}! Session ID: {session_id}",
    "equipment_requested": "📦 Equipment request submitted for {employee_name}: {equipment_list}",
    "access_granted": "🔐 Access granted to {group_name} for {employee_name}",
    "meeting_scheduled": "📅 Meeting scheduled: {meeting_type} on {date} at {time}",
    "hr_question_answered": "📋 HR Question answered regarding {topic}",
}

__all__ = [
    'AgentNames',
    'OnboardingStatus', 
    'RequestStatus',
    'EquipmentTypes',
    'Departments',
    'ADGroups',
    'MeetingTypes',
    'DEFAULT_ONBOARDING_DURATION_DAYS',
    'DEFAULT_EQUIPMENT_DELIVERY_DAYS', 
    'DEFAULT_ACCESS_REVIEW_DAYS',
    'SYSTEM_MESSAGES',
    'AGENT_DESCRIPTIONS',
    'RESPONSE_TEMPLATES'
]
