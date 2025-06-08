"""
ID Master Agent - Enhanced Version
Creates and manages the new employee's core digital identity.
Simulates interaction with Microsoft Active Directory.
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
import re
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

# Mock Active Directory database
mock_ad_users = {}
mock_ad_groups = {
    "all_employees": {"members": [], "description": "All company employees"},
    "new_hires": {"members": [], "description": "New employees in first 90 days"},
    "finance_team": {"members": [], "description": "Finance department"},
    "hr_team": {"members": [], "description": "Human Resources department"},
    "engineering_team": {"members": [], "description": "Engineering department"},
    "marketing_team": {"members": [], "description": "Marketing department"}
}

mock_email_accounts = {}
mock_security_groups = {}

# ID Master Tools
def create_user_account(first_name: str, last_name: str, department: str, 
                       job_title: str, manager_email: Optional[str] = None, 
                       employee_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Creates a new user account in Active Directory.
    
    Args:
        first_name: Employee's first name
        last_name: Employee's last name
        department: Employee's department
        job_title: Employee's job title
        manager_email: Manager's email address
        employee_id: Employee ID (auto-generated if not provided)
    
    Returns:
        User account creation details
    """
    try:
        # Generate employee ID if not provided
        if not employee_id:
            employee_id = f"EMP{uuid.uuid4().hex[:6].upper()}"
        
        # Generate username (first initial + last name)
        username = f"{first_name[0].lower()}{last_name.lower()}".replace(" ", "")
        
        # Check if username already exists and modify if needed
        original_username = username
        counter = 1
        while username in mock_ad_users:
            username = f"{original_username}{counter}"
            counter += 1
        
        # Generate email address
        email = f"{username}@company.com"
        
        # Generate temporary password
        temp_password = f"TempPass{uuid.uuid4().hex[:8]}"
        
        # Create user account
        user_account = {
            "employee_id": employee_id,
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "full_name": f"{first_name} {last_name}",
            "department": department,
            "job_title": job_title,
            "manager_email": manager_email,
            "temp_password": temp_password,
            "account_status": "active",
            "created_date": datetime.now().isoformat(),
            "password_must_change": True,
            "groups": ["all_employees", "new_hires"]
        }
        
        # Store in mock AD
        mock_ad_users[username] = user_account
        mock_email_accounts[email] = user_account
        
        # Add to default groups
        mock_ad_groups["all_employees"]["members"].append(username)
        mock_ad_groups["new_hires"]["members"].append(username)
        
        # Add to department group if it exists
        dept_group = f"{department.lower()}_team"
        if dept_group in mock_ad_groups:
            mock_ad_groups[dept_group]["members"].append(username)
            user_account["groups"].append(dept_group)
        
        return {
            "status": "success",
            "message": f"User account created successfully for {first_name} {last_name}",
            "employee_id": employee_id,
            "username": username,
            "email": email,
            "temp_password": temp_password,
            "groups_assigned": user_account["groups"],
            "next_steps": [
                "User must change password on first login",
                "Account will be reviewed after 90 days",
                "Manager should be notified of account creation"
            ]
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to create user account: {e}",
            "employee_details": {
                "first_name": first_name,
                "last_name": last_name,
                "department": department
            }
        }

def assign_security_groups(username: str, security_groups: List[str]) -> Dict[str, Any]:
    """
    Assigns security groups to a user account.
    
    Args:
        username: The username to assign groups to
        security_groups: List of security group names
    
    Returns:
        Security group assignment results
    """
    if username not in mock_ad_users:
        return {
            "status": "error",
            "message": f"User '{username}' not found in Active Directory"
        }
    
    user = mock_ad_users[username]
    assigned_groups = []
    failed_groups = []
    
    for group in security_groups:
        if group in mock_ad_groups:
            if username not in mock_ad_groups[group]["members"]:
                mock_ad_groups[group]["members"].append(username)
                user["groups"].append(group)
                assigned_groups.append(group)
            else:
                assigned_groups.append(f"{group} (already member)")
        else:
            failed_groups.append(group)
    
    return {
        "status": "success" if not failed_groups else "partial_success",
        "username": username,
        "assigned_groups": assigned_groups,
        "failed_groups": failed_groups,
        "total_groups": user["groups"],
        "message": f"Security group assignment completed for {username}"
    }

def setup_email_account(username: str, mailbox_size_mb: int = 5000) -> Dict[str, Any]:
    """
    Sets up email account and mailbox for the user.
    
    Args:
        username: The username to setup email for
        mailbox_size_mb: Mailbox size in MB
    
    Returns:
        Email setup results
    """
    if username not in mock_ad_users:
        return {
            "status": "error",
            "message": f"User '{username}' not found in Active Directory"
        }
    
    user = mock_ad_users[username]
    email = user["email"]
    
    # Setup email account
    email_config = {
        "email_address": email,
        "mailbox_size_mb": mailbox_size_mb,
        "exchange_server": "mail.company.com",
        "smtp_server": "smtp.company.com",
        "imap_server": "imap.company.com",
        "mobile_sync_enabled": True,
        "archive_policy": "7_years",
        "spam_filter_enabled": True,
        "setup_date": datetime.now().isoformat(),
        "status": "active"
    }
    
    # Update user record
    user["email_config"] = email_config
    
    return {
        "status": "success",
        "message": f"Email account setup completed for {email}",
        "email_address": email,
        "mailbox_size_mb": mailbox_size_mb,
        "servers": {
            "exchange": email_config["exchange_server"],
            "smtp": email_config["smtp_server"],
            "imap": email_config["imap_server"]
        },
        "features": [
            "Mobile synchronization enabled",
            "Spam filtering enabled",
            "7-year archive policy applied"
        ]
    }

def generate_access_credentials(username: str, credential_types: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Generates various access credentials for the user.
    
    Args:
        username: The username to generate credentials for
        credential_types: Types of credentials to generate
    
    Returns:
        Generated credentials
    """
    if username not in mock_ad_users:
        return {
            "status": "error",
            "message": f"User '{username}' not found in Active Directory"
        }
    
    if credential_types is None:
        credential_types = ["vpn", "wifi", "building_access"]
    
    user = mock_ad_users[username]
    credentials = {}
    
    for cred_type in credential_types:
        if cred_type == "vpn":
            credentials["vpn"] = {
                "vpn_username": f"vpn_{username}",
                "vpn_password": f"VPN{uuid.uuid4().hex[:8]}",
                "vpn_server": "vpn.company.com",
                "connection_type": "IKEv2"
            }
        elif cred_type == "wifi":
            credentials["wifi"] = {
                "network_name": "CompanyWiFi",
                "wifi_password": f"WiFi{uuid.uuid4().hex[:8]}",
                "security_type": "WPA2-Enterprise",
                "certificate_required": True
            }
        elif cred_type == "building_access":
            credentials["building_access"] = {
                "badge_id": f"BADGE{uuid.uuid4().hex[:6].upper()}",
                "access_level": "standard_employee",
                "valid_from": datetime.now().isoformat(),
                "valid_until": (datetime.now() + timedelta(days=365)).isoformat(),
                "access_zones": ["lobby", "office_floors", "cafeteria", "parking"]
            }
    
    # Update user record
    user["credentials"] = credentials
    
    return {
        "status": "success",
        "message": f"Access credentials generated for {username}",
        "username": username,
        "credentials": credentials,
        "security_notes": [
            "VPN credentials must be used only for business purposes",
            "WiFi password should not be shared",
            "Building access badge must be worn visibly at all times"
        ]
    }

def verify_user_setup(username: str) -> Dict[str, Any]:
    """
    Verifies that user setup is complete and all systems are configured.
    
    Args:
        username: The username to verify
    
    Returns:
        Verification results
    """
    if username not in mock_ad_users:
        return {
            "status": "error",
            "message": f"User '{username}' not found in Active Directory"
        }
    
    user = mock_ad_users[username]
    verification_results = {
        "ad_account": True,
        "email_account": "email_config" in user,
        "security_groups": len(user.get("groups", [])) > 0,
        "credentials": "credentials" in user,
        "manager_assigned": user.get("manager_email") is not None
    }
    
    all_complete = all(verification_results.values())
    
    missing_items = [key for key, value in verification_results.items() if not value]
    
    return {
        "status": "complete" if all_complete else "incomplete",
        "username": username,
        "verification_results": verification_results,
        "completion_percentage": (sum(verification_results.values()) / len(verification_results)) * 100,
        "missing_items": missing_items,
        "user_details": {
            "full_name": user["full_name"],
            "email": user["email"],
            "department": user["department"],
            "job_title": user["job_title"]
        },
        "next_steps": missing_items if missing_items else ["User setup is complete"]
    }

def list_user_accounts(department: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
    """
    Lists user accounts with optional filtering.
    
    Args:
        department: Filter by department
        status: Filter by account status
    
    Returns:
        List of user accounts
    """
    users = []
    for username, user in mock_ad_users.items():
        if department and user.get("department", "").lower() != department.lower():
            continue
        if status and user.get("account_status", "").lower() != status.lower():
            continue
        
        users.append({
            "username": username,
            "full_name": user["full_name"],
            "email": user["email"],
            "department": user["department"],
            "job_title": user["job_title"],
            "account_status": user["account_status"],
            "created_date": user["created_date"],
            "groups_count": len(user.get("groups", []))
        })
    
    return {
        "status": "success",
        "users": users,
        "total_count": len(users),
        "filters_applied": {
            "department": department,
            "status": status
        }
    }

# Create ID Master Agent
id_master = LlmAgent(
    model=GEMINI_2_FLASH,
    name="id_master",
    instruction="""You are the ID Master Agent responsible for creating and managing new employee digital identities and Active Directory accounts.

Your responsibilities:
1. Create new user accounts in Active Directory with proper naming conventions
2. Set up email accounts and mailbox configurations
3. Assign appropriate security groups based on department and role
4. Generate access credentials (VPN, WiFi, building access)
5. Verify complete user setup and configuration

When creating user accounts:
- Generate unique usernames using first initial + last name format
- Create secure temporary passwords that must be changed on first login
- Assign users to appropriate default groups (all_employees, new_hires)
- Add users to department-specific groups when available
- Set up proper email configuration with standard mailbox size

When setting up access:
- Generate VPN credentials for remote access
- Provide WiFi credentials for office connectivity
- Create building access badges with appropriate security levels
- Ensure all credentials follow company security policies

When verifying setup:
- Check that all required components are configured
- Verify security group assignments are appropriate
- Confirm email and credential setup is complete
- Provide completion status and next steps

Security considerations:
- All temporary passwords must be changed on first login
- Access credentials should follow principle of least privilege
- New hire accounts should be reviewed after 90 days
- Manager approval should be obtained for sensitive group access

Always provide comprehensive setup information and clear next steps for both the new employee and their manager.""",
    description="Creates and manages digital identities and Active Directory accounts for new employees",
    tools=[
        FunctionTool(func=create_user_account),
        FunctionTool(func=assign_security_groups),
        FunctionTool(func=setup_email_account),
        FunctionTool(func=generate_access_credentials),
        FunctionTool(func=verify_user_setup),
        FunctionTool(func=list_user_accounts)
    ]
)

# Session and Runner setup
session_service = InMemorySessionService()
runner = Runner(
    agent=id_master,
    app_name="id_master_app",
    session_service=session_service
)

# Export for ADK CLI compatibility
agent = id_master

def process_identity_request(user_input: str, user_id: str = "default_user") -> str:
    """
    Process an identity management request through the ID Master system.
    
    Args:
        user_input: The identity management request
        user_id: Unique identifier for the user
    
    Returns:
        Final response from the ID Master system
    """
    # Create or get session
    session_id = f"id_session_{user_id}"
    
    # Check if session exists, if not create it
    session = None
    try:
        session = session_service.get_session(
            app_name="id_master_app",
            user_id=user_id,
            session_id=session_id
        )
    except:
        # Session doesn't exist, create a new one
        pass
    
    if session is None:
        session = session_service.create_session(
            app_name="id_master_app",
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
def test_id_master():
    """Test the ID Master system with various scenarios."""
    print("=== Testing ID Master Agent ===\n")
    
    test_cases = [
        "Create a new user account for Alex Johnson in the Engineering department as a Software Developer",
        "Set up email account for the user ajohnson",
        "Generate VPN and WiFi credentials for ajohnson",
        "Verify the complete setup for user ajohnson",
        "List all users in the Engineering department"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test Case {i}: {test_case}")
        print("-" * 50)
        
        response = process_identity_request(test_case, f"test_user_{i}")
        print(f"ID Master: {response}")
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    # Run tests
    test_id_master()
    
    # Interactive mode
    print("ID Master Interactive Mode - Enter identity management requests (type 'quit' to exit):")
    print("Available commands:")
    print("- Create user account: 'Create account for [name] in [department] as [job title]'")
    print("- Setup email: 'Setup email for [username]'")
    print("- Generate credentials: 'Generate credentials for [username]'")
    print("- Verify setup: 'Verify setup for [username]'")
    print("- List users: 'List users in [department]'")
    print()
    
    while True:
        user_input = input("\nAdmin: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        if user_input:
            response = process_identity_request(user_input, "interactive_user")
            print(f"ID Master: {response}")
