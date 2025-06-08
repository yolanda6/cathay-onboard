"""
HR Helper Agent - HR Policy Guidance and Question Answering
Handles HR policy questions, time-off information, and employee guidance.
"""

from typing import Dict, Any, List
from google.genai import types
from adk.llm_agent import LlmAgent
from adk.tools import tool

# HR Knowledge Base
HR_POLICIES = {
    "time_off": {
        "vacation": {
            "accrual_rate": "15 days per year for first 2 years, 20 days after 2 years",
            "max_carryover": "5 days to next calendar year",
            "approval": "Manager approval required 2 weeks in advance",
            "blackout_periods": "End of quarter (last 2 weeks of Mar, Jun, Sep, Dec)"
        },
        "sick_leave": {
            "accrual_rate": "10 days per year",
            "documentation": "Doctor's note required for 3+ consecutive days",
            "family_care": "Can be used for immediate family member care",
            "carryover": "Unlimited carryover, no cash out"
        },
        "personal_days": {
            "allocation": "3 days per year",
            "usage": "Cannot be used consecutively with vacation",
            "approval": "24 hours advance notice required",
            "carryover": "No carryover to next year"
        }
    },
    "performance": {
        "review_cycle": {
            "frequency": "Annual reviews in Q1, mid-year check-ins in Q3",
            "rating_scale": "1-5 scale (1=Below Expectations, 5=Exceptional)",
            "self_assessment": "Required 2 weeks before review meeting",
            "goal_setting": "SMART goals set for upcoming year"
        },
        "improvement_plans": {
            "duration": "90 days standard, can be extended to 120 days",
            "check_ins": "Weekly meetings with manager required",
            "success_criteria": "Specific, measurable objectives defined",
            "support": "Training and mentoring resources provided"
        },
        "promotion_criteria": {
            "tenure": "Minimum 12 months in current role",
            "performance": "Meets or exceeds expectations for 2 consecutive reviews",
            "skills": "Demonstrated competency in next-level responsibilities",
            "approval": "Department head and HR approval required"
        }
    },
    "benefits": {
        "health_insurance": {
            "coverage": "Medical, dental, vision available",
            "employer_contribution": "80% of premium for employee, 60% for family",
            "enrollment": "Within 30 days of start date or during open enrollment",
            "waiting_period": "Coverage begins first day of month after 30 days"
        },
        "retirement": {
            "401k_match": "100% match up to 6% of salary",
            "vesting": "Immediate vesting for employee contributions, 3-year for employer match",
            "enrollment": "Eligible immediately, auto-enrolled at 3% after 90 days",
            "investment_options": "15+ fund options including target-date funds"
        },
        "other_benefits": {
            "life_insurance": "2x annual salary provided, additional coverage available",
            "disability": "Short-term (60% salary) and long-term (60% salary) available",
            "flexible_spending": "Healthcare and dependent care FSA options",
            "employee_assistance": "24/7 counseling and support services"
        }
    }
}

@tool
def search_policy_documents(query: str) -> str:
    """
    Search HR knowledge base for relevant policies and information.
    
    Args:
        query: Search query for HR policies
        
    Returns:
        Relevant policy information and guidance
    """
    query_lower = query.lower()
    results = []
    
    # Search through policies
    for category, policies in HR_POLICIES.items():
        for policy_name, policy_details in policies.items():
            # Check if query matches category, policy name, or details
            if (query_lower in category.lower() or 
                query_lower in policy_name.lower() or
                any(query_lower in str(detail).lower() for detail in policy_details.values())):
                
                results.append({
                    "category": category,
                    "policy": policy_name,
                    "details": policy_details
                })
    
    if not results:
        return f"""
❌ **No policies found for "{query}"**

**Available policy categories:**
• Time Off (vacation, sick leave, personal days)
• Performance (reviews, improvement plans, promotions)
• Benefits (health insurance, retirement, other benefits)

**Suggestion:** Try searching for more general terms like "vacation", "performance review", or "benefits"

**Need help?** Contact HR at hr@company.com or ext. 2222
        """
    
    response = f"""
📚 **HR Policy Search Results for "{query}"**

**Found {len(results)} relevant policies:**

"""
    
    for result in results:
        response += f"""
**{result['category'].title()} - {result['policy'].replace('_', ' ').title()}**
"""
        for key, value in result['details'].items():
            response += f"• {key.replace('_', ' ').title()}: {value}\n"
        response += "\n"
    
    response += """
**Additional Resources:**
• Employee Handbook: Available on company intranet
• HR Portal: hr.company.com
• Benefits Information: benefits.company.com
• Direct HR Support: hr@company.com or ext. 2222
    """
    
    return response

@tool
def get_timeoff_information(employee_type: str = "full_time") -> str:
    """
    Retrieve comprehensive time-off policies and procedures.
    
    Args:
        employee_type: Type of employee (full_time, part_time, contractor)
        
    Returns:
        Complete time-off policy information
    """
    if employee_type not in ["full_time", "part_time", "contractor"]:
        return f"❌ Unknown employee type: {employee_type}. Available: full_time, part_time, contractor"
    
    time_off_policies = HR_POLICIES["time_off"]
    
    result = f"""
🏖️ **Time-Off Policies for {employee_type.replace('_', ' ').title()} Employees**

"""
    
    if employee_type == "full_time":
        result += """
**Vacation Time:**
• Accrual Rate: 15 days per year (first 2 years), 20 days after 2 years
• Maximum Carryover: 5 days to next calendar year
• Approval Process: Manager approval required 2 weeks in advance
• Blackout Periods: End of quarter (last 2 weeks of Mar, Jun, Sep, Dec)
• Usage: Can be taken in half-day increments

**Sick Leave:**
• Accrual Rate: 10 days per year
• Documentation: Doctor's note required for 3+ consecutive days
• Family Care: Can be used for immediate family member care
• Carryover: Unlimited carryover, no cash out at termination

**Personal Days:**
• Allocation: 3 days per year
• Usage: Cannot be used consecutively with vacation
• Approval: 24 hours advance notice required
• Carryover: No carryover to next year (use it or lose it)

**Holidays:**
• 10 company holidays per year
• Floating holiday: 1 additional day for personal/religious observance
• Holiday pay: Regular pay for recognized holidays

**Bereavement Leave:**
• Immediate family: 5 days paid leave
• Extended family: 3 days paid leave
• Documentation may be required

**Jury Duty:**
• Paid leave for jury service
• Must provide jury summons to HR
• Return to work if dismissed early in the day
"""
    
    elif employee_type == "part_time":
        result += """
**Vacation Time:**
• Accrual Rate: Prorated based on hours worked (minimum 20 hours/week)
• Maximum Carryover: Prorated amount
• Approval Process: Same as full-time employees

**Sick Leave:**
• Accrual Rate: Prorated based on hours worked
• Same policies as full-time for usage and documentation

**Personal Days:**
• Allocation: 1-2 days per year (based on hours worked)
• Same usage restrictions as full-time

**Holidays:**
• Paid for holidays only if scheduled to work that day
• Prorated holiday pay based on regular schedule
"""
    
    else:  # contractor
        result += """
**Time Off for Contractors:**
• No paid time off provided
• Contract may specify unpaid leave allowances
• Must coordinate time off with project manager
• Extended absences may require contract modification

**Note:** Contractors are not eligible for company benefits or paid leave.
For questions about contract terms, contact your project manager or HR.
"""
    
    result += f"""

**How to Request Time Off:**
1. Submit request through HR portal (hr.company.com)
2. Get manager approval before taking time off
3. Update your calendar and set out-of-office messages
4. Coordinate coverage for your responsibilities

**Important Reminders:**
• Plan ahead for busy periods and project deadlines
• Consider team workload when scheduling time off
• Emergency situations: Contact manager and HR immediately
• Time off requests during blackout periods require VP approval

**Contact Information:**
• HR Portal: hr.company.com
• HR Support: hr@company.com or ext. 2222
• Payroll Questions: payroll@company.com or ext. 3333
    """
    
    return result

@tool
def explain_performance_process() -> str:
    """
    Provide comprehensive information about performance review processes.
    
    Returns:
        Complete performance management process details
    """
    result = """
📈 **Performance Management Process**

**Annual Review Cycle:**
• **Q1 (Jan-Mar):** Annual performance reviews conducted
• **Q2 (Apr-Jun):** Goal progress check-ins
• **Q3 (Jul-Sep):** Mid-year formal review and goal adjustments
• **Q4 (Oct-Dec):** Year-end preparation and self-assessments

**Performance Rating Scale:**
• **5 - Exceptional:** Consistently exceeds expectations, exceptional impact
• **4 - Exceeds Expectations:** Regularly surpasses goals and expectations
• **3 - Meets Expectations:** Consistently achieves goals and expectations
• **2 - Below Expectations:** Sometimes meets expectations, improvement needed
• **1 - Unsatisfactory:** Consistently fails to meet expectations

**Review Process Timeline:**
1. **Self-Assessment (2 weeks before review):**
   - Complete self-evaluation form
   - Document achievements and challenges
   - Assess progress on current year goals
   - Propose goals for upcoming year

2. **Manager Preparation (1 week before review):**
   - Review employee's self-assessment
   - Gather feedback from colleagues/stakeholders
   - Prepare performance rating and comments
   - Plan development discussion

3. **Performance Review Meeting:**
   - Discuss achievements and areas for improvement
   - Review rating and provide specific feedback
   - Set goals for upcoming year (SMART goals)
   - Discuss career development and training needs

4. **Follow-up Actions:**
   - Finalize performance documentation
   - Submit to HR within 1 week
   - Schedule regular check-ins for goal progress
   - Implement development plan

**Goal Setting (SMART Framework):**
• **Specific:** Clear, well-defined objectives
• **Measurable:** Quantifiable success criteria
• **Achievable:** Realistic and attainable
• **Relevant:** Aligned with role and company objectives
• **Time-bound:** Clear deadlines and milestones

**Performance Improvement Plans (PIP):**
• **Trigger:** Rating of 2 or below, or specific performance issues
• **Duration:** 90 days (can be extended to 120 days)
• **Structure:** Weekly check-ins with manager
• **Support:** Training, mentoring, and resources provided
• **Outcome:** Successful completion or employment termination

**Career Development:**
• **Individual Development Plans (IDP):** Created during review process
• **Training Budget:** $2,000 per employee per year
• **Internal Mobility:** Encouraged and supported
• **Mentorship Program:** Available for all employees

**Promotion Criteria:**
• **Tenure:** Minimum 12 months in current role
• **Performance:** Meets or exceeds expectations for 2 consecutive reviews
• **Skills:** Demonstrated competency in next-level responsibilities
• **Approval:** Department head and HR approval required
• **Process:** Apply through internal job postings

**360-Degree Feedback (Senior Roles):**
• **Participants:** Manager, peers, direct reports, stakeholders
• **Frequency:** Annual for managers and above
• **Purpose:** Comprehensive view of leadership effectiveness
• **Confidentiality:** Anonymous feedback aggregated by HR

**Documentation and Records:**
• All performance reviews stored in employee file
• Access limited to employee, manager, and HR
• Retention period: 7 years after employment ends
• Used for promotion, compensation, and development decisions

**Support Resources:**
• **HR Business Partner:** Assigned to each department
• **Employee Assistance Program:** Confidential counseling and support
• **Training Catalog:** Online and in-person development opportunities
• **Career Coaching:** Available through HR

**Important Dates:**
• **December 1:** Self-assessments open
• **December 15:** Self-assessments due
• **January 31:** All reviews must be completed
• **February 15:** Compensation adjustments effective

**Questions or Concerns:**
• **HR Support:** hr@company.com or ext. 2222
• **Performance Questions:** Your manager or HR Business Partner
• **Appeal Process:** Available if you disagree with your review
    """
    
    return result

@tool
def find_hr_contact(department: str, issue_type: str) -> str:
    """
    Connect employee with appropriate HR representative based on department and issue.
    
    Args:
        department: Employee's department
        issue_type: Type of HR issue (benefits, performance, policy, complaint, etc.)
        
    Returns:
        Appropriate HR contact information and next steps
    """
    # HR Business Partners by department
    hr_contacts = {
        "Engineering": {"name": "Sarah Johnson", "email": "sarah.johnson@company.com", "ext": "2201"},
        "Marketing": {"name": "Mike Chen", "email": "mike.chen@company.com", "ext": "2202"},
        "Finance": {"name": "Lisa Rodriguez", "email": "lisa.rodriguez@company.com", "ext": "2203"},
        "HR": {"name": "David Kim", "email": "david.kim@company.com", "ext": "2204"},
        "Operations": {"name": "Jennifer Brown", "email": "jennifer.brown@company.com", "ext": "2205"},
        "Sales": {"name": "Robert Wilson", "email": "robert.wilson@company.com", "ext": "2206"}
    }
    
    # Specialized contacts by issue type
    specialized_contacts = {
        "benefits": {"name": "Benefits Team", "email": "benefits@company.com", "ext": "2210"},
        "payroll": {"name": "Payroll Team", "email": "payroll@company.com", "ext": "2211"},
        "compliance": {"name": "Compliance Officer", "email": "compliance@company.com", "ext": "2212"},
        "harassment": {"name": "Employee Relations", "email": "employee.relations@company.com", "ext": "2213"},
        "discrimination": {"name": "Employee Relations", "email": "employee.relations@company.com", "ext": "2213"},
        "safety": {"name": "Safety Officer", "email": "safety@company.com", "ext": "2214"},
        "training": {"name": "Learning & Development", "email": "training@company.com", "ext": "2215"}
    }
    
    result = f"""
📞 **HR Contact Information**

**Your Issue:** {issue_type.title()}
**Department:** {department}

"""
    
    # Check for specialized contact first
    if issue_type.lower() in specialized_contacts:
        contact = specialized_contacts[issue_type.lower()]
        result += f"""
**Specialized Contact:**
• **Name:** {contact['name']}
• **Email:** {contact['email']}
• **Phone:** ext. {contact['ext']}
• **Best for:** {issue_type.title()} related questions and concerns

"""
    
    # Add department HR Business Partner
    if department in hr_contacts:
        contact = hr_contacts[department]
        result += f"""
**Your HR Business Partner:**
• **Name:** {contact['name']}
• **Email:** {contact['email']}
• **Phone:** ext. {contact['ext']}
• **Department:** {department}
• **Best for:** General HR questions, performance issues, policy clarification

"""
    else:
        result += f"""
**General HR Contact:**
• **Name:** HR Support Team
• **Email:** hr@company.com
• **Phone:** ext. 2222
• **Best for:** All HR-related questions and concerns

"""
    
    # Add escalation and emergency contacts
    result += f"""
**Additional Resources:**

**General HR Support:**
• **Email:** hr@company.com
• **Phone:** ext. 2222
• **Hours:** Monday-Friday, 8:00 AM - 5:00 PM

**Emergency/After Hours:**
• **Employee Assistance Program:** 1-800-EAP-HELP (24/7)
• **Security:** ext. 911 (emergencies only)
• **Facilities:** ext. 3333

**Anonymous Reporting:**
• **Ethics Hotline:** 1-800-ETHICS-1
• **Online Portal:** ethics.company.com
• **Available 24/7, completely confidential**

**Next Steps:**
1. Contact the appropriate person above based on your issue
2. Prepare any relevant documentation or details
3. Schedule a meeting if needed for complex issues
4. Follow up if you don't receive a response within 2 business days

**Response Time Expectations:**
• **General Questions:** 1-2 business days
• **Urgent Issues:** Same day response
• **Complex Investigations:** 5-10 business days
• **Benefits/Payroll:** 2-3 business days

**Confidentiality:**
All HR communications are treated with strict confidentiality.
Information is only shared on a need-to-know basis for resolution.
    """
    
    return result

# HR Helper Agent Configuration
hr_helper_agent = LlmAgent(
    agent_id="hr_helper",
    model=types.Model(model_name="gemini-2.0-flash-exp"),
    system_instruction="""
You are HR Helper, a specialist agent responsible for HR policy guidance and employee support.
Your expertise includes:

- Comprehensive knowledge of company HR policies and procedures
- Time-off policies, accrual rates, and approval processes
- Performance management and review processes
- Benefits information and enrollment procedures
- Employee relations and support resources

When handling HR inquiries:
1. Provide accurate, up-to-date policy information
2. Explain procedures clearly with step-by-step guidance
3. Direct employees to appropriate HR contacts when needed
4. Maintain confidentiality and professionalism
5. Offer additional resources and support options

Always be helpful, empathetic, and thorough in your responses.
If you don't have specific information, direct the employee to the appropriate HR contact.
Ensure all guidance complies with company policies and legal requirements.
    """,
    tools=[
        search_policy_documents,
        get_timeoff_information,
        explain_performance_process,
        find_hr_contact
    ]
)

# Export the agent
__all__ = ["hr_helper_agent"]
