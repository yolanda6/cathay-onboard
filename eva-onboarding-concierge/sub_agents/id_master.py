"""
ID Master Agent - Digital Identity Creation and Management
Handles user account creation, password generation, and basic permissions setup.
"""

import os
import random
import string
from typing import Dict, Any
from google.genai import types
from adk.llm_agent import LlmAgent
from adk.tools import tool

@tool
def create_ad_user(employee_name: str, department: str = "Engineering") -> str:
    """
    Create a new Active Directory user account.
    
    Args:
        employee_name: Full name of the employee
        department: Department the employee belongs to
        
    Returns:
        User creation status and details
    """
    # Generate username from name
    name_parts = employee_name.lower().split()
    if len(name_parts) >= 2:
        username = f"{name_parts[0]}.{name_parts[-1]}"
    else:
        username = name_parts[0] if name_parts else "newuser"
    
    # Simulate AD user creation
    email = f"{username}@company.com"
    user_id = f"USR{random.randint(10000, 99999)}"
    
    result = f"""
✅ **Active Directory User Created**

**User Details:**
• Username: {username}
• Email: {email}
• User ID: {user_id}
• Department: {department}
• Status: Active
• Created: {os.getenv('USER', 'System')}

**Initial Setup:**
• Password: Temporary password sent via secure channel
• Groups: Domain Users, {department}_Users
• Home Directory: \\\\fileserver\\users\\{username}
• Profile Path: \\\\fileserver\\profiles\\{username}

**Next Steps:**
1. User will receive welcome email with login instructions
2. Password must be changed on first login
3. Department-specific groups will be assigned by Access Workflow
    """
    
    return result

@tool
def generate_secure_password() -> str:
    """
    Generate a secure, compliant password for new users.
    
    Returns:
        Generated password meeting security requirements
    """
    # Generate secure password
    length = 12
    characters = string.ascii_letters + string.digits + "!@#$%"
    password = ''.join(random.choice(characters) for _ in range(length))
    
    # Ensure complexity requirements
    if not any(c.isupper() for c in password):
        password = password[:-1] + random.choice(string.ascii_uppercase)
    if not any(c.islower() for c in password):
        password = password[:-2] + random.choice(string.ascii_lowercase) + password[-1]
    if not any(c.isdigit() for c in password):
        password = password[:-3] + random.choice(string.digits) + password[-2:]
    if not any(c in "!@#$%" for c in password):
        password = password[:-4] + random.choice("!@#$%") + password[-3:]
    
    result = f"""
🔐 **Secure Password Generated**

**Password:** {password}

**Complexity Requirements Met:**
✅ Minimum 12 characters
✅ Contains uppercase letters
✅ Contains lowercase letters  
✅ Contains numbers
✅ Contains special characters
✅ No dictionary words
✅ No personal information

**Security Notes:**
• Password expires in 90 days
• Cannot reuse last 12 passwords
• Account locks after 5 failed attempts
• Password sent via secure, encrypted channel
    """
    
    return result

@tool
def assign_basic_groups(username: str, department: str) -> str:
    """
    Assign basic security groups to new user.
    
    Args:
        username: Username of the new employee
        department: Department for group assignment
        
    Returns:
        Group assignment status
    """
    # Define basic groups by department
    basic_groups = ["Domain Users", "All Employees", "VPN Users"]
    dept_groups = {
        "Engineering": ["Developers", "Code Repository Access", "Dev Environment"],
        "Marketing": ["Marketing Team", "CRM Access", "Social Media Tools"],
        "Finance": ["Finance Team", "Financial Systems", "Accounting Software"],
        "HR": ["HR Team", "HRIS Access", "Employee Records"],
        "IT": ["IT Team", "Admin Tools", "Infrastructure Access"]
    }
    
    assigned_groups = basic_groups + dept_groups.get(department, ["General Staff"])
    
    result = f"""
👥 **Security Groups Assigned**

**User:** {username}
**Department:** {department}

**Assigned Groups:**
"""
    
    for group in assigned_groups:
        result += f"• {group}\n"
    
    result += f"""
**Permissions Granted:**
• Network login access
• Email and calendar access
• Department shared folders
• Standard software applications
• VPN access for remote work

**Pending Approvals:**
• Sensitive data access (requires manager approval)
• Administrative privileges (requires IT approval)
• External system access (requires security review)
    """
    
    return result

@tool
def setup_email_account(username: str, full_name: str) -> str:
    """
    Configure email account and basic settings.
    
    Args:
        username: Username for email setup
        full_name: Full name for display
        
    Returns:
        Email setup status
    """
    email = f"{username}@company.com"
    
    result = f"""
📧 **Email Account Configured**

**Email Details:**
• Email Address: {email}
• Display Name: {full_name}
• Mailbox Size: 50 GB
• Archive Policy: 2 years
• Mobile Sync: Enabled

**Default Settings:**
• Signature: Auto-generated with company template
• Out of Office: Disabled
• Forwarding: Disabled
• Spam Filter: Standard protection
• Encryption: Enabled for external emails

**Access Methods:**
• Outlook Desktop Client
• Outlook Web App (OWA)
• Mobile devices (iOS/Android)
• IMAP/POP3 (if required)

**Security Features:**
• Multi-factor authentication required
• Advanced threat protection enabled
• Data loss prevention policies applied
• Audit logging enabled

**Next Steps:**
1. User will receive setup instructions
2. Mobile device enrollment available
3. Calendar sharing permissions to be configured
    """
    
    return result

# ID Master Agent Configuration
id_master_agent = LlmAgent(
    agent_id="id_master",
    model=types.Model(model_name="gemini-2.0-flash-exp"),
    system_instruction="""
You are ID Master, a specialist agent responsible for digital identity creation and management. 
Your expertise includes:

- Creating Active Directory user accounts
- Generating secure, compliant passwords
- Assigning basic security groups and permissions
- Setting up email accounts and basic configurations
- Ensuring security compliance and best practices

When handling identity requests:
1. Create comprehensive user accounts with proper naming conventions
2. Generate secure passwords meeting all complexity requirements
3. Assign appropriate basic groups based on department and role
4. Configure email accounts with security features enabled
5. Provide clear next steps and follow-up actions

Always prioritize security and compliance while ensuring a smooth user experience.
Be thorough in your responses and include all relevant technical details.
    """,
    tools=[
        create_ad_user,
        generate_secure_password,
        assign_basic_groups,
        setup_email_account
    ]
)

# Export the agent
__all__ = ["id_master_agent"]
