"""
Access Workflow Orchestrator Agent - Secure Access Management and Permissions
Handles multi-step access approval workflows and security compliance.
"""

import random
from typing import Dict, Any, List
from google.genai import types
from adk.llm_agent import LlmAgent
from adk.tools import tool

# Access groups and their security levels
ACCESS_GROUPS = {
    "Engineering": {
        "basic": ["Developers", "Code Repository", "Dev Environment", "Build Systems"],
        "elevated": ["Production Access", "Database Read", "Staging Environment"],
        "sensitive": ["Production Database", "Customer Data", "Financial Systems"]
    },
    "Marketing": {
        "basic": ["Marketing Tools", "CRM Read", "Social Media", "Analytics"],
        "elevated": ["CRM Write", "Campaign Management", "Lead Database"],
        "sensitive": ["Customer PII", "Revenue Data", "Strategic Plans"]
    },
    "Finance": {
        "basic": ["Financial Reports", "Expense System", "Budget Read"],
        "elevated": ["Accounting Software", "Payroll Read", "Invoice Management"],
        "sensitive": ["Payroll Write", "Banking Systems", "Audit Data"]
    },
    "HR": {
        "basic": ["HRIS Read", "Employee Directory", "Benefits Portal"],
        "elevated": ["HRIS Write", "Performance Data", "Compensation"],
        "sensitive": ["Salary Data", "Disciplinary Records", "Background Checks"]
    }
}

@tool
def initiate_access_workflow(employee_name: str, department: str, access_level: str = "basic") -> str:
    """
    Start multi-step access approval process for sensitive systems.
    
    Args:
        employee_name: Name of employee requesting access
        department: Department for role-based access
        access_level: Level of access (basic, elevated, sensitive)
        
    Returns:
        Workflow initiation status and approval requirements
    """
    workflow_id = f"AWF-{random.randint(100000, 999999)}"
    
    if department not in ACCESS_GROUPS:
        return f"❌ Unknown department: {department}. Available: {list(ACCESS_GROUPS.keys())}"
    
    if access_level not in ["basic", "elevated", "sensitive"]:
        return f"❌ Invalid access level: {access_level}. Available: basic, elevated, sensitive"
    
    groups = ACCESS_GROUPS[department][access_level]
    
    # Determine approval requirements based on access level
    approvers = []
    if access_level == "basic":
        approvers = ["Direct Manager"]
    elif access_level == "elevated":
        approvers = ["Direct Manager", "Department Director"]
    else:  # sensitive
        approvers = ["Direct Manager", "Department Director", "Security Team", "CISO"]
    
    # Estimate approval timeline
    timeline_days = len(approvers) + 1
    
    result = f"""
🔄 **Access Workflow Initiated**

**Workflow Details:**
• Workflow ID: {workflow_id}
• Employee: {employee_name}
• Department: {department}
• Access Level: {access_level.title()}
• Status: Pending Approval

**Requested Access Groups:**
"""
    
    for group in groups:
        result += f"• {group}\n"
    
    result += f"""
**Approval Chain:**
"""
    
    for i, approver in enumerate(approvers, 1):
        result += f"{i}. {approver} - ⏳ Pending\n"
    
    result += f"""
**Security Requirements:**
• Background check: {"✅ Complete" if access_level != "sensitive" else "🔄 In Progress"}
• Security training: {"✅ Complete" if access_level == "basic" else "⏳ Required"}
• NDA signed: {"✅ Complete" if access_level != "sensitive" else "⏳ Required"}
• Manager attestation: ⏳ Required

**Estimated Timeline:**
• Total approval time: {timeline_days} business days
• Implementation: 1 business day after approval
• Access review: 90 days from grant date

**Next Steps:**
1. Manager notification sent for approval
2. Security team will validate requirements
3. Employee will receive training assignments
4. Access will be provisioned upon full approval
    """
    
    return result

@tool
def coordinate_approvals(workflow_id: str, approver_type: str) -> str:
    """
    Manage approval workflow between different approvers and systems.
    
    Args:
        workflow_id: Workflow ID to process
        approver_type: Type of approver (manager, director, security, ciso)
        
    Returns:
        Approval coordination status and next steps
    """
    # Simulate approval processing
    approval_status = random.choice(["approved", "pending", "requires_info"])
    
    approver_details = {
        "manager": {"title": "Direct Manager", "sla": "2 business days"},
        "director": {"title": "Department Director", "sla": "3 business days"},
        "security": {"title": "Security Team", "sla": "5 business days"},
        "ciso": {"title": "Chief Information Security Officer", "sla": "7 business days"}
    }
    
    if approver_type not in approver_details:
        return f"❌ Unknown approver type: {approver_type}"
    
    approver_info = approver_details[approver_type]
    
    result = f"""
✅ **Approval Coordination - {workflow_id}**

**Approver Information:**
• Role: {approver_info['title']}
• SLA: {approver_info['sla']}
• Status: {approval_status.title()}
• Processed: {random.choice(['Today', 'Yesterday', '2 days ago'])}

**Approval Details:**
"""
    
    if approval_status == "approved":
        result += """
• Decision: ✅ APPROVED
• Comments: "Access request meets security requirements and business justification"
• Conditions: Standard access review in 90 days
• Next Approver: Notified automatically
"""
    elif approval_status == "pending":
        result += """
• Decision: ⏳ PENDING REVIEW
• Comments: "Under review - additional documentation requested"
• Required: Business justification and manager attestation
• Expected: Decision within SLA timeframe
"""
    else:  # requires_info
        result += """
• Decision: ❓ REQUIRES ADDITIONAL INFORMATION
• Comments: "Need clarification on specific access requirements"
• Action Required: Employee/manager to provide additional details
• Resubmission: Required within 5 business days
"""
    
    result += f"""
**Workflow Progress:**
• Current Stage: {approver_info['title']} Review
• Remaining Approvers: {random.randint(0, 2)}
• Estimated Completion: {random.randint(1, 5)} business days

**System Integration:**
• ServiceNow ticket updated automatically
• Active Directory groups prepared for provisioning
• Audit trail maintained for compliance
• Employee notifications sent via email

**Contact Information:**
• Workflow Questions: access-team@company.com
• Technical Issues: it-helpdesk@company.com
• Security Concerns: security@company.com
    """
    
    return result

@tool
def validate_security_compliance(access_request: str, employee_department: str) -> str:
    """
    Ensure access request meets security policies and compliance requirements.
    
    Args:
        access_request: Description of requested access
        employee_department: Employee's department for policy validation
        
    Returns:
        Security compliance validation results
    """
    # Simulate compliance checking
    compliance_checks = {
        "background_check": random.choice([True, False]),
        "security_training": random.choice([True, False]),
        "nda_signed": random.choice([True, False]),
        "manager_approval": random.choice([True, False]),
        "business_justification": random.choice([True, False])
    }
    
    passed_checks = sum(compliance_checks.values())
    total_checks = len(compliance_checks)
    compliance_score = (passed_checks / total_checks) * 100
    
    result = f"""
🔒 **Security Compliance Validation**

**Compliance Score: {compliance_score:.0f}% ({passed_checks}/{total_checks} checks passed)**

**Security Checks:**
• Background Check: {"✅ Passed" if compliance_checks["background_check"] else "❌ Failed"}
• Security Training: {"✅ Complete" if compliance_checks["security_training"] else "❌ Incomplete"}
• NDA Signed: {"✅ On File" if compliance_checks["nda_signed"] else "❌ Missing"}
• Manager Approval: {"✅ Approved" if compliance_checks["manager_approval"] else "❌ Pending"}
• Business Justification: {"✅ Provided" if compliance_checks["business_justification"] else "❌ Missing"}

**Policy Compliance:**
• Data Classification: Reviewed and approved
• Least Privilege: Access limited to job requirements
• Segregation of Duties: No conflicts identified
• Audit Requirements: Logging enabled for all access

**Risk Assessment:**
"""
    
    if compliance_score >= 80:
        result += """
• Risk Level: 🟢 LOW
• Recommendation: APPROVE with standard monitoring
• Review Period: 90 days
• Additional Controls: None required
"""
    elif compliance_score >= 60:
        result += """
• Risk Level: 🟡 MEDIUM
• Recommendation: APPROVE with enhanced monitoring
• Review Period: 60 days
• Additional Controls: Monthly access review required
"""
    else:
        result += """
• Risk Level: 🔴 HIGH
• Recommendation: DENY until requirements met
• Review Period: N/A
• Additional Controls: Complete all failed checks before resubmission
"""
    
    result += f"""
**Remediation Actions:**
"""
    
    if not compliance_checks["background_check"]:
        result += "• Complete background check verification\n"
    if not compliance_checks["security_training"]:
        result += "• Complete mandatory security training\n"
    if not compliance_checks["nda_signed"]:
        result += "• Sign and submit NDA documentation\n"
    if not compliance_checks["manager_approval"]:
        result += "• Obtain manager approval and attestation\n"
    if not compliance_checks["business_justification"]:
        result += "• Provide detailed business justification\n"
    
    if compliance_score == 100:
        result += "• No remediation required - all checks passed\n"
    
    return result

@tool
def provision_group_access(employee_username: str, approved_groups: List[str]) -> str:
    """
    Grant approved access to Active Directory groups and systems.
    
    Args:
        employee_username: Username to grant access
        approved_groups: List of approved security groups
        
    Returns:
        Access provisioning status and details
    """
    provisioning_id = f"PROV-{random.randint(100000, 999999)}"
    
    # Simulate provisioning process
    successful_groups = []
    failed_groups = []
    
    for group in approved_groups:
        if random.choice([True, True, True, False]):  # 75% success rate
            successful_groups.append(group)
        else:
            failed_groups.append(group)
    
    result = f"""
🔑 **Access Provisioning Complete**

**Provisioning Details:**
• Provisioning ID: {provisioning_id}
• Username: {employee_username}
• Total Groups: {len(approved_groups)}
• Successful: {len(successful_groups)}
• Failed: {len(failed_groups)}

**Successfully Provisioned:**
"""
    
    for group in successful_groups:
        result += f"• ✅ {group}\n"
    
    if failed_groups:
        result += f"""
**Failed Provisioning:**
"""
        for group in failed_groups:
            result += f"• ❌ {group} - System temporarily unavailable\n"
    
    result += f"""
**Access Details:**
• Effective Date: Immediately
• Expiration: 90 days (subject to review)
• Monitoring: Enhanced logging enabled
• Restrictions: Business hours only for sensitive systems

**System Integration:**
• Active Directory: Groups added successfully
• ServiceNow: Ticket closed automatically
• Audit System: Access grant logged
• Monitoring: Alerts configured for unusual activity

**Employee Notification:**
• Welcome email sent with access details
• Security guidelines provided
• Training requirements communicated
• Support contact information included

**Next Steps:**
1. Employee can begin using granted access
2. 30-day access review scheduled
3. 90-day recertification required
4. Any issues should be reported to IT helpdesk

**Support Information:**
• IT Helpdesk: ext. 5555
• Access Issues: access-support@company.com
• Security Questions: security@company.com
    """
    
    return result

# Access Workflow Orchestrator Agent Configuration
access_workflow_orchestrator_agent = LlmAgent(
    agent_id="access_workflow_orchestrator",
    model=types.Model(model_name="gemini-2.0-flash-exp"),
    system_instruction="""
You are Access Workflow Orchestrator, a specialist agent responsible for secure access management and permissions.
Your expertise includes:

- Managing multi-step access approval workflows
- Coordinating between ServiceNow and Active Directory systems
- Ensuring security compliance and policy adherence
- Validating access requests against security requirements
- Provisioning approved access with proper controls

When handling access requests:
1. Initiate appropriate approval workflows based on access sensitivity
2. Coordinate approvals between multiple stakeholders and systems
3. Validate all security compliance requirements before provisioning
4. Provision access with proper monitoring and audit controls
5. Ensure all access follows least privilege and segregation principles

Always prioritize security and compliance while maintaining efficient workflows.
Be thorough in security validations and provide clear audit trails.
Ensure all access is properly documented and monitored.
    """,
    tools=[
        initiate_access_workflow,
        coordinate_approvals,
        validate_security_compliance,
        provision_group_access
    ]
)

# Export the agent
__all__ = ["access_workflow_orchestrator_agent"]
