"""
HR Helper Agent - Enhanced Version
Answers common HR questions by tapping into the company's knowledge base.
Specialized agents for Time Off and Performance policies using PDF datasets.
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
import pdfplumber
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

# PDF file paths
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
TIMEOFF_POLICY_PATH = os.path.join(current_dir, "data", "timeoff-policy.pdf")
PERFORMANCE_POLICY_PATH = os.path.join(current_dir, "data", "performance-policy.pdf")

# Cache for PDF content
pdf_content_cache = {}

def extract_pdf_content(pdf_path: str) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
    
    Returns:
        Extracted text content
    """
    if pdf_path in pdf_content_cache:
        return pdf_content_cache[pdf_path]
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        pdf_content_cache[pdf_path] = text
        return text
    except Exception as e:
        logging.error(f"Error extracting PDF content from {pdf_path}: {e}")
        return f"Error reading PDF file: {e}"

# Mock HR database for additional information
mock_hr_data = {
    "employee_handbook": {
        "dress_code": "Business casual is the standard dress code. Remote workers should maintain professional appearance during video calls.",
        "work_hours": "Standard work hours are 9 AM to 5 PM, Monday through Friday. Flexible hours available with manager approval.",
        "remote_work": "Hybrid work model allows up to 3 days remote per week. Full remote work requires special approval.",
        "benefits_enrollment": "Benefits enrollment period is during the first 30 days of employment and annually in November.",
        "parking": "Free parking is available in the company garage. Parking passes can be obtained from the front desk."
    },
    "contact_info": {
        "hr_department": "hr@company.com",
        "it_support": "it-help@company.com",
        "facilities": "facilities@company.com",
        "payroll": "payroll@company.com",
        "benefits": "benefits@company.com"
    },
    "common_forms": {
        "time_off_request": "Available in the employee portal under 'Time Off' section",
        "expense_report": "Submit through the expense management system",
        "performance_review": "Completed quarterly through the performance management portal",
        "equipment_request": "Submit IT tickets through the service desk portal"
    }
}

# HR Helper Tools
def search_timeoff_policy(query: str) -> Dict[str, Any]:
    """
    Search the time off policy document for relevant information.
    
    Args:
        query: The search query related to time off policies
    
    Returns:
        Relevant information from the time off policy
    """
    try:
        content = extract_pdf_content(TIMEOFF_POLICY_PATH)
        
        if "Error reading PDF" in content:
            return {
                "status": "error",
                "message": "Unable to access time off policy document",
                "content": content
            }
        
        # Simple keyword matching for demo purposes
        # In a real implementation, you'd use more sophisticated search/RAG
        query_lower = query.lower()
        lines = content.split('\n')
        relevant_lines = []
        
        keywords = query_lower.split()
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in keywords):
                relevant_lines.append(line.strip())
        
        if relevant_lines:
            relevant_content = '\n'.join(relevant_lines[:10])  # Limit to first 10 matches
        else:
            relevant_content = content[:1000] + "..." if len(content) > 1000 else content
        
        return {
            "status": "success",
            "query": query,
            "relevant_content": relevant_content,
            "source": "Time Off Policy Document",
            "message": f"Found information related to: {query}"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error searching time off policy: {e}",
            "query": query
        }

def search_performance_policy(query: str) -> Dict[str, Any]:
    """
    Search the performance policy document for relevant information.
    
    Args:
        query: The search query related to performance policies
    
    Returns:
        Relevant information from the performance policy
    """
    try:
        content = extract_pdf_content(PERFORMANCE_POLICY_PATH)
        
        if "Error reading PDF" in content:
            return {
                "status": "error",
                "message": "Unable to access performance policy document",
                "content": content
            }
        
        # Simple keyword matching for demo purposes
        query_lower = query.lower()
        lines = content.split('\n')
        relevant_lines = []
        
        keywords = query_lower.split()
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in keywords):
                relevant_lines.append(line.strip())
        
        if relevant_lines:
            relevant_content = '\n'.join(relevant_lines[:10])  # Limit to first 10 matches
        else:
            relevant_content = content[:1000] + "..." if len(content) > 1000 else content
        
        return {
            "status": "success",
            "query": query,
            "relevant_content": relevant_content,
            "source": "Performance Policy Document",
            "message": f"Found information related to: {query}"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error searching performance policy: {e}",
            "query": query
        }

def get_general_hr_info(topic: str) -> Dict[str, Any]:
    """
    Get general HR information from the employee handbook.
    
    Args:
        topic: The HR topic to get information about
    
    Returns:
        General HR information
    """
    topic_lower = topic.lower()
    
    # Search in employee handbook
    for key, value in mock_hr_data["employee_handbook"].items():
        if topic_lower in key or any(word in key for word in topic_lower.split()):
            return {
                "status": "success",
                "topic": topic,
                "information": value,
                "source": "Employee Handbook",
                "category": key
            }
    
    # Search in contact info
    for key, value in mock_hr_data["contact_info"].items():
        if topic_lower in key or any(word in key for word in topic_lower.split()):
            return {
                "status": "success",
                "topic": topic,
                "information": f"Contact: {value}",
                "source": "HR Contact Directory",
                "category": key
            }
    
    # Search in common forms
    for key, value in mock_hr_data["common_forms"].items():
        if topic_lower in key or any(word in key for word in topic_lower.split()):
            return {
                "status": "success",
                "topic": topic,
                "information": value,
                "source": "Forms and Procedures",
                "category": key
            }
    
    return {
        "status": "not_found",
        "topic": topic,
        "message": "Information not found in general HR resources. Try searching specific policy documents.",
        "suggestions": [
            "Time off policies - use time off search",
            "Performance policies - use performance search",
            "Contact HR directly at hr@company.com"
        ]
    }

def list_hr_resources() -> Dict[str, Any]:
    """
    List available HR resources and topics.
    
    Returns:
        List of available HR resources
    """
    return {
        "status": "success",
        "resources": {
            "policy_documents": [
                "Time Off Policy (vacation, sick leave, personal days)",
                "Performance Policy (reviews, goals, development)"
            ],
            "employee_handbook_topics": list(mock_hr_data["employee_handbook"].keys()),
            "contact_information": list(mock_hr_data["contact_info"].keys()),
            "common_forms": list(mock_hr_data["common_forms"].keys())
        },
        "search_capabilities": [
            "Search time off policies",
            "Search performance policies", 
            "Get general HR information",
            "Find contact information"
        ]
    }

def get_hr_contacts(department: Optional[str] = None) -> Dict[str, Any]:
    """
    Get HR contact information.
    
    Args:
        department: Specific department to get contact for
    
    Returns:
        HR contact information
    """
    if department:
        department_lower = department.lower()
        for key, value in mock_hr_data["contact_info"].items():
            if department_lower in key:
                return {
                    "status": "success",
                    "department": department,
                    "contact": value,
                    "category": key
                }
        
        return {
            "status": "not_found",
            "department": department,
            "message": f"Contact information for '{department}' not found",
            "available_contacts": list(mock_hr_data["contact_info"].keys())
        }
    else:
        return {
            "status": "success",
            "all_contacts": mock_hr_data["contact_info"],
            "message": "All HR contact information"
        }

# Create Time Off Policy Agent
timeoff_agent = LlmAgent(
    model=GEMINI_2_FLASH,
    name="timeoff_policy_agent",
    instruction="""You are a Time Off Policy Specialist Agent that helps employees understand company time off policies.

Your responsibilities:
1. Answer questions about vacation time, sick leave, personal days, and other time off policies
2. Search the time off policy document for specific information
3. Provide clear explanations of time off procedures and requirements
4. Help employees understand their time off benefits and entitlements

When answering questions:
- Search the time off policy document for relevant information
- Provide specific policy details and procedures
- Explain any requirements or restrictions clearly
- Reference the official policy document as your source
- If information isn't found, suggest contacting HR directly

Topics you can help with:
- Vacation time accrual and usage
- Sick leave policies and procedures
- Personal days and floating holidays
- Time off request procedures
- Holiday schedules
- Leave of absence policies
- Time off approval processes

Always provide accurate information based on the official policy documents and be helpful in guiding employees through time off procedures.""",
    description="Specialist agent for time off and vacation policy questions",
    tools=[
        FunctionTool(func=search_timeoff_policy)
    ],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)

# Create Performance Policy Agent
performance_agent = LlmAgent(
    model=GEMINI_2_FLASH,
    name="performance_policy_agent", 
    instruction="""You are a Performance Policy Specialist Agent that helps employees understand company performance management policies.

Your responsibilities:
1. Answer questions about performance reviews, goal setting, and career development
2. Search the performance policy document for specific information
3. Provide clear explanations of performance management procedures
4. Help employees understand performance expectations and development opportunities

When answering questions:
- Search the performance policy document for relevant information
- Provide specific policy details and procedures
- Explain performance review processes and timelines
- Reference the official policy document as your source
- If information isn't found, suggest contacting HR directly

Topics you can help with:
- Performance review cycles and procedures
- Goal setting and tracking
- Career development opportunities
- Performance improvement plans
- Promotion and advancement criteria
- Training and development programs
- Manager feedback and coaching
- Performance rating systems

Always provide accurate information based on the official policy documents and help employees understand how to succeed in their performance management journey.""",
    description="Specialist agent for performance management and career development questions",
    tools=[
        FunctionTool(func=search_performance_policy)
    ],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)

# Create Main HR Helper Agent
hr_helper = LlmAgent(
    model=GEMINI_2_FLASH,
    name="hr_helper",
    instruction="""You are the HR Helper Agent - your primary role is to assist employees with HR-related questions and direct them to the appropriate specialist agents or resources.

Your responsibilities:
1. Understand employee HR questions and route them to the appropriate specialist
2. Provide general HR information from the employee handbook
3. Help employees find the right contacts and resources
4. Handle general HR inquiries that don't require specialist knowledge

ROUTING RULES:
- For time off, vacation, sick leave questions: transfer to timeoff_policy_agent
- For performance reviews, goals, career development: transfer to performance_policy_agent
- For general HR topics (dress code, work hours, benefits, etc.): use general HR tools
- For contact information: provide HR contact details

When handling requests:
1. First determine if the question is about time off policies or performance policies
2. If it's a specialist topic, transfer to the appropriate agent
3. If it's general HR information, search the employee handbook
4. Always provide helpful guidance and next steps
5. If you can't find information, provide relevant contact details

You can help with:
- Time off and vacation policies (via specialist agent)
- Performance management (via specialist agent)
- General employee handbook topics
- HR contact information
- Common forms and procedures
- Benefits information
- Workplace policies

Always be helpful, professional, and ensure employees get the information they need from the most appropriate source.""",
    description="Main HR Helper agent that routes questions to specialists and provides general HR information",
    tools=[
        FunctionTool(func=get_general_hr_info),
        FunctionTool(func=list_hr_resources),
        FunctionTool(func=get_hr_contacts)
    ],
    sub_agents=[timeoff_agent, performance_agent]
)

# Session and Runner setup
session_service = InMemorySessionService()
runner = Runner(
    agent=hr_helper,
    app_name="hr_helper_app",
    session_service=session_service
)

# Export for ADK CLI compatibility
agent = hr_helper

def process_hr_question(user_input: str, user_id: str = "default_user") -> str:
    """
    Process an HR question through the multi-agent system.
    
    Args:
        user_input: The user's HR question
        user_id: Unique identifier for the user
    
    Returns:
        Final response from the HR system
    """
    # Create or get session
    session_id = f"hr_session_{user_id}"
    
    # Check if session exists, if not create it
    session = None
    try:
        session = session_service.get_session(
            app_name="hr_helper_app",
            user_id=user_id,
            session_id=session_id
        )
    except:
        # Session doesn't exist, create a new one
        pass
    
    if session is None:
        session = session_service.create_session(
            app_name="hr_helper_app",
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
def test_hr_helper():
    """Test the HR Helper system with various questions."""
    print("=== Testing HR Helper Multi-Agent System ===\n")
    
    test_cases = [
        "How many vacation days do I get?",
        "What is the performance review process?",
        "What is the dress code policy?",
        "How do I request time off?",
        "When are performance reviews conducted?",
        "What are the work hours?",
        "Who should I contact for IT support?",
        "What HR resources are available?",
        "How do I submit an expense report?"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test Case {i}: {test_case}")
        print("-" * 50)
        
        response = process_hr_question(test_case, f"test_user_{i}")
        print(f"HR Helper: {response}")
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    # Run tests
    test_hr_helper()
    
    # Interactive mode
    print("HR Helper Interactive Mode - Ask your HR questions (type 'quit' to exit):")
    print("Available topics:")
    print("- Time off and vacation policies")
    print("- Performance reviews and career development")
    print("- General HR policies and procedures")
    print("- Contact information")
    print()
    
    while True:
        user_input = input("\nEmployee: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        if user_input:
            response = process_hr_question(user_input, "interactive_user")
            print(f"HR Helper: {response}")
