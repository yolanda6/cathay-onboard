
# Eva Onboarding Concierge: Building Enterprise AI Agents with Google ADK
## Technical Speaking Draft & Talk Track

---

## 🎯 **Presentation Overview**
**Duration**: 30-45 minutes  
**Audience**: Technical teams, architects, developers, enterprise IT leaders  
**Focus**: ADK implementation, multi-agent architecture, enterprise integration patterns  

---

## 📋 **Talk Track Structure**

### **Opening Hook (2 minutes)**
*[SLIDE: Title + Demo GIF]*

**Speaker Notes:**
> "Imagine a new employee's first day. Instead of spending hours filling out forms, waiting for IT tickets, and hunting down HR policies, they simply chat with Eva - an AI concierge that orchestrates their entire onboarding experience. Today, I'll show you how we built this sophisticated multi-agent system using Google's Agent Development Kit, and more importantly, how you can adapt this architecture for your own enterprise use cases."

**Key Points to Emphasize:**
- Real-world problem solving
- Enterprise-grade architecture
- Practical implementation with ADK

---

### **Section 1: The Challenge & Vision (5 minutes)**
*[SLIDE: Current vs. Future State]*

**Talk Track:**
> "Let's start with the problem. Traditional employee onboarding is a nightmare of disconnected systems, manual processes, and frustrated new hires. We envisioned Eva as a single conversational interface that could orchestrate complex enterprise workflows."

**Demo Setup:**
```
"Hi Eva, I need to onboard Alex Johnson as a Software Developer 
starting Monday in the Engineering department."
```

**Speaker Notes:**
- Show the complexity behind this simple request
- Highlight the 6 different systems Eva coordinates
- Emphasize the "white-glove" experience concept

**Technical Transition:**
> "But here's the interesting part - this isn't just a chatbot. It's a sophisticated multi-agent orchestration system built with Google's ADK. Let me show you the architecture."

---

### **Section 2: Architecture Deep Dive (10 minutes)**
*[SLIDE: Mermaid Architecture Diagram]*

**Talk Track:**
> "Eva is built as a hierarchical multi-agent system with three distinct layers. At the top, we have Eva herself - the orchestrator. Below her are five specialist agents, and some of those have their own sub-agents. This creates a natural delegation pattern that mirrors how human organizations work."

#### **2.1 Root Agent - Eva Orchestrator**
*[SLIDE: Eva's Tools and Responsibilities]*

**Code Example to Show:**
```python
# Eva's core orchestration tools
eva_orchestrator = LlmAgent(
    model="gemini-2.0-flash-exp",  # More powerful model for orchestration
    name="Eva",
    tools=[
        FunctionTool(func=start_onboarding_session),
        FunctionTool(func=get_onboarding_status),
        FunctionTool(func=update_checklist_item),
        # ... more tools
    ],
    sub_agents=[
        id_master, device_depot, access_workflow_orchestrator,
        hr_helper, meeting_maven
    ]
)
```

**Speaker Notes:**
- Eva uses the more powerful Gemini 2.0 Flash model
- She maintains session state and overall workflow
- Delegates to specialists but maintains oversight

#### **2.2 Specialist Agents**
*[SLIDE: The Five Specialists]*

**Talk Track:**
> "Each specialist agent is like a domain expert. The ID Master handles identity management, Device Depot manages equipment, and so on. But here's where it gets interesting - some agents are themselves orchestrators."

**Focus on Access Workflow Orchestrator:**
```python
# Sub-orchestrator pattern
access_workflow_orchestrator = LlmAgent(
    model="gemini-2.5-flash-preview-05-20",
    sub_agents=[servicenow_agent, ad_agent]
)
```

**Speaker Notes:**
- Show how the Access Workflow Orchestrator manages its own sub-agents
- Explain the security workflow: ServiceNow → Approval → Active Directory
- Emphasize the audit trail and compliance features

#### **2.3 ADK Implementation Patterns**
*[SLIDE: Code Structure]*

**Key ADK Concepts to Highlight:**

1. **Agent Definition:**
```python
from google.adk.agents import LlmAgent
from google.adk.tools.function_tool import FunctionTool

agent = LlmAgent(
    model="gemini-2.5-flash-preview-05-20",
    name="specialist_agent",
    instruction="Your specialized role...",
    tools=[FunctionTool(func=your_function)],
    sub_agents=[sub_agent1, sub_agent2]
)
```

2. **Session Management:**
```python
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

session_service = InMemorySessionService()
runner = Runner(agent=eva_orchestrator, session_service=session_service)
```

3. **Tool Implementation:**
```python
def start_onboarding_session(employee_name: str, employee_email: str, 
                           department: str) -> Dict[str, Any]:
    """
    ADK tools return structured data that agents can understand
    """
    return {
        "status": "success",
        "session_id": session_id,
        "next_steps": [...]
    }
```

**Speaker Notes:**
- Emphasize how ADK handles the complexity of agent coordination
- Show how tools return structured data for agent reasoning
- Highlight the session management capabilities

---

### **Section 3: Current Implementation - Mock Backend Strategy (8 minutes)**
*[SLIDE: Mock vs. Real Systems]*

**Talk Track:**
> "Now, here's the crucial part for enterprise adoption. Our current implementation uses sophisticated mocks that simulate real enterprise systems. This isn't just placeholder code - it's a deliberate architectural decision that provides immediate value while enabling seamless future integration."

#### **3.1 Mock Implementation Examples**

**ServiceNow Simulation:**
```python
# Mock ServiceNow database
mock_service_requests = {}

def create_service_request(group_name: str, new_user_email: str) -> Dict[str, Any]:
    """
    Simulates ServiceNow ticket creation with realistic workflow
    """
    request_id = f"SR-{uuid.uuid4().hex[:8].upper()}"
    
    # Simulate approval workflow
    service_request = {
        "request_id": request_id,
        "status": "pending_approval",
        "group_owner": mock_ad_groups[group_name]["owner"],
        "created_at": datetime.now().isoformat()
    }
    
    mock_service_requests[request_id] = service_request
    return {"status": "success", "request_id": request_id}
```

**Active Directory Simulation:**
```python
# Mock AD groups with realistic structure
mock_ad_groups = {
    "engineering_team": {
        "owner": "tech.lead@company.com",
        "members": ["dev1@company.com", "dev2@company.com"],
        "description": "Engineering team access group"
    }
}

def add_user_to_ad_group(work_order_id: str) -> Dict[str, Any]:
    """
    Simulates AD group membership changes with audit trail
    """
    # Realistic validation and processing
    work_order = mock_work_orders[work_order_id]
    group_name = work_order["group_name"]
    new_user_email = work_order["new_user_email"]
    
    mock_ad_groups[group_name]["members"].append(new_user_email)
    
    return {
        "status": "success",
        "message": f"Successfully added {new_user_email} to {group_name}",
        "audit_trail": {...}
    }
```

#### **3.2 Benefits of Mock-First Approach**

**Speaker Notes:**
> "This mock-first approach provides several key benefits:"

1. **Immediate Demonstration Value**
   - Complete workflows work end-to-end
   - Stakeholders can see the full vision
   - No dependency on enterprise system availability

2. **Realistic Behavior Modeling**
   - Approval workflows with delays
   - Error conditions and edge cases
   - Audit trails and compliance features

3. **Development Velocity**
   - Teams can develop and test independently
   - No need for complex enterprise system access
   - Rapid iteration and prototyping

4. **Integration Planning**
   - Mock interfaces define real API contracts
   - Clear separation between business logic and system integration
   - Risk reduction for enterprise rollout

---

### **Section 4: Enterprise Integration Roadmap (8 minutes)**
*[SLIDE: Migration Path to Production]*

**Talk Track:**
> "The beauty of this architecture is the migration path to production. Each mock can be replaced with real enterprise integrations without changing the agent logic or user experience."

#### **4.1 Integration Patterns**

**Configuration-Driven Integration:**
```python
# Centralized configuration enables easy switching
class EvaConfig:
    # Development: use mocks
    USE_MOCK_SERVICENOW = os.getenv("USE_MOCK_SERVICENOW", "true") == "true"
    USE_MOCK_ACTIVE_DIRECTORY = os.getenv("USE_MOCK_AD", "true") == "true"
    
    # Production: real endpoints
    SERVICENOW_API_URL = os.getenv("SERVICENOW_API_URL")
    ACTIVE_DIRECTORY_ENDPOINT = os.getenv("AD_ENDPOINT")

def create_service_request(group_name: str, new_user_email: str) -> Dict[str, Any]:
    if EvaConfig.USE_MOCK_SERVICENOW:
        return mock_create_service_request(group_name, new_user_email)
    else:
        return real_servicenow_integration(group_name, new_user_email)
```

**Real ServiceNow Integration Example:**
```python
def real_servicenow_integration(group_name: str, new_user_email: str) -> Dict[str, Any]:
    """
    Production ServiceNow integration
    """
    headers = {
        "Authorization": f"Bearer {get_servicenow_token()}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "short_description": f"AD Group Access Request: {group_name}",
        "description": f"Request to add {new_user_email} to {group_name}",
        "category": "Access Request",
        "urgency": "3"
    }
    
    response = requests.post(
        f"{EvaConfig.SERVICENOW_API_URL}/api/now/table/incident",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 201:
        ticket_data = response.json()
        return {
            "status": "success",
            "request_id": ticket_data["result"]["number"],
            "sys_id": ticket_data["result"]["sys_id"]
        }
    else:
        return {"status": "error", "message": "ServiceNow API error"}
```

#### **4.2 Enterprise System Integration Points**

**Microsoft Active Directory:**
```python
# Using Microsoft Graph API
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient

def real_ad_integration():
    credential = ClientSecretCredential(
        tenant_id=EvaConfig.AZURE_TENANT_ID,
        client_id=EvaConfig.AZURE_CLIENT_ID,
        client_secret=EvaConfig.AZURE_CLIENT_SECRET
    )
    
    graph_client = GraphServiceClient(
        credentials=credential,
        scopes=['https://graph.microsoft.com/.default']
    )
    
    return graph_client
```

**Google Calendar Integration:**
```python
# Using Google Calendar API
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def real_calendar_integration():
    credentials = Credentials.from_service_account_file(
        EvaConfig.GOOGLE_SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/calendar']
    )
    
    service = build('calendar', 'v3', credentials=credentials)
    return service
```

#### **4.3 Migration Strategy**

**Phase 1: Proof of Concept (Current)**
- All mocks, full functionality demonstration
- Stakeholder buy-in and requirement validation
- Agent behavior refinement

**Phase 2: Pilot Integration**
- Replace one system at a time (e.g., start with Google Calendar)
- Maintain mocks for other systems
- Validate integration patterns

**Phase 3: Production Rollout**
- Replace remaining mocks with real integrations
- Implement proper error handling and monitoring
- Add enterprise security and compliance features

**Phase 4: Scale and Extend**
- Add new specialist agents for additional workflows
- Implement advanced features like ML-driven optimization
- Expand to other business processes

---

### **Section 5: Live Demo (8 minutes)**
*[SLIDE: Demo Environment]*

**Demo Script:**

1. **Start Onboarding Session:**
```
"Hi Eva! I need to onboard Sarah Chen as a Data Scientist 
in the Analytics department starting next Monday. 
Her email will be sarah.chen@company.com and her manager is analytics.lead@company.com"
```

2. **Show Equipment Request:**
```
"Sarah will need a MacBook Pro and an external monitor for her data science work"
```

3. **Access Management:**
```
"Please add Sarah to the analytics_team group for data access"
```

4. **HR Questions:**
```
"What's the company policy on vacation time?"
```

5. **Meeting Scheduling:**
```
"Schedule a welcome meeting between Sarah and her manager for her first day"
```

**Demo Talking Points:**
- Show how Eva delegates to different agents
- Highlight the conversational flow
- Demonstrate the comprehensive checklist tracking
- Show the audit trail and status updates

---

### **Section 6: Technical Implementation Details (5 minutes)**
*[SLIDE: Code Architecture]*

#### **6.1 ADK Best Practices**

**Agent Instruction Design:**
```python
EVA_ORCHESTRATOR_INSTRUCTION = """
You are Eva, an AI Onboarding Concierge that orchestrates comprehensive 
employee onboarding through specialist agents.

Your responsibilities:
1. Understand onboarding requests and break them into tasks
2. Delegate to appropriate specialist agents
3. Maintain overall progress tracking
4. Provide status updates and summaries

DELEGATION RULES:
- For identity management: transfer to id_master
- For equipment requests: transfer to device_depot
- For access requests: transfer to access_workflow_orchestrator
- For HR questions: transfer to hr_helper
- For meeting scheduling: transfer to meeting_maven

Always maintain the onboarding session state and provide clear next steps.
"""
```

**Tool Design Patterns:**
```python
def start_onboarding_session(
    employee_name: str, 
    employee_email: str, 
    department: str,
    job_title: str, 
    start_date: str
) -> Dict[str, Any]:
    """
    ADK tools should:
    1. Have clear, descriptive function signatures
    2. Return structured data with status indicators
    3. Include error handling and validation
    4. Provide actionable next steps
    """
    try:
        # Validation
        if not employee_email or "@" not in employee_email:
            return {
                "status": "error",
                "message": "Invalid email address",
                "required_fields": ["employee_name", "employee_email", "department"]
            }
        
        # Business logic
        session_id = f"ONBOARD-{uuid.uuid4().hex[:8].upper()}"
        
        # Return structured response
        return {
            "status": "success",
            "session_id": session_id,
            "employee_profile": {...},
            "checklist_summary": {...},
            "next_steps": [...]
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to start onboarding: {e}",
            "support_contact": "it-support@company.com"
        }
```

#### **6.2 Configuration Management**

**Centralized Configuration:**
```python
class EvaConfig:
    """
    Centralized configuration for all agents and integrations
    """
    # Google Cloud
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project")
    LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    # Agent Models
    ROOT_AGENT_MODEL = os.getenv("ROOT_AGENT_MODEL", "gemini-2.0-flash-exp")
    SUB_AGENT_MODEL = os.getenv("SUB_AGENT_MODEL", "gemini-2.5-flash-preview-05-20")
    
    # Enterprise Systems
    SERVICENOW_API_URL = os.getenv("SERVICENOW_API_URL")
    AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
    
    # Feature Flags
    ENABLE_AUDIT_LOGGING = os.getenv("ENABLE_AUDIT_LOGGING", "true") == "true"
    USE_MOCK_BACKENDS = os.getenv("USE_MOCK_BACKENDS", "true") == "true"
```

---

### **Section 7: Q&A and Next Steps (5 minutes)**

**Common Questions to Prepare For:**

1. **"How does this scale to thousands of employees?"**
   - ADK handles session management and agent coordination
   - Stateless agent design enables horizontal scaling
   - Enterprise systems handle the actual load

2. **"What about security and compliance?"**
   - All enterprise integrations use proper authentication
   - Audit trails built into every operation
   - Role-based access controls in the enterprise systems

3. **"How long does integration take?"**
   - Depends on enterprise system APIs and security requirements
   - Typical timeline: 2-4 weeks per system integration
   - Can be done incrementally without disrupting the demo

4. **"Can this work with our existing systems?"**
   - Yes, the mock interfaces define the integration contracts
   - Any system with REST APIs can be integrated
   - Custom adapters can be built for legacy systems

**Next Steps for Audience:**
1. **Try the Demo**: Provide access to the running system
2. **Review Architecture**: Share the technical documentation
3. **Integration Planning**: Identify their enterprise systems and APIs
4. **Pilot Planning**: Define scope for initial integration

---

## 🎯 **Key Takeaways to Emphasize**

### **For Technical Teams:**
- ADK provides powerful multi-agent orchestration capabilities
- Mock-first development enables rapid prototyping and stakeholder buy-in
- Clear migration path from demo to production
- Modular architecture supports incremental integration

### **For Enterprise Leaders:**
- Immediate demonstration value with full workflow visibility
- Risk mitigation through phased integration approach
- Scalable architecture that grows with business needs
- ROI through improved employee experience and reduced manual processes

### **For Architects:**
- Hierarchical agent design mirrors organizational structures
- Configuration-driven integration enables environment management
- Audit trails and compliance features built-in from the start
- Extensible pattern for other business processes

---

## 📋 **Presentation Materials Checklist**

### **Slides Needed:**
- [ ] Title slide with demo GIF
- [ ] Problem statement and vision
- [ ] Architecture diagram (Mermaid)
- [ ] Agent hierarchy breakdown
- [ ] Code examples for each layer
- [ ] Mock vs. real integration comparison
- [ ] Migration roadmap timeline
- [ ] Live demo environment
- [ ] Technical implementation details
- [ ] Q&A and next steps

### **Demo Environment:**
- [ ] Running Eva system with all agents
- [ ] Sample employee data for realistic demos
- [ ] Pre-configured scenarios for different workflows
- [ ] Backup demo recordings in case of technical issues

### **Handouts:**
- [ ] Architecture documentation
- [ ] Code repository access
- [ ] Integration planning template
- [ ] Contact information for follow-up

---

## 🚀 **Speaker Preparation Notes**

### **Technical Depth Calibration:**
- **Developer Audience**: Focus on code examples and ADK patterns
- **Architect Audience**: Emphasize design decisions and scalability
- **Business Audience**: Highlight ROI and risk mitigation
- **Mixed Audience**: Balance technical details with business value

### **Demo Contingencies:**
- Have backup recordings for each demo section
- Prepare simplified examples if time runs short
- Know the codebase well enough to show specific implementations
- Have troubleshooting steps ready for common issues

### **Engagement Strategies:**
- Ask audience about their current onboarding pain points
- Invite questions throughout, not just at the end
- Use polls or interactive elements if virtual presentation
- Provide clear next steps for interested attendees

This presentation structure provides a comprehensive technical overview while maintaining practical focus on implementation and enterprise adoption. The mock-to-production migration story is particularly compelling for enterprise audiences who need to see both immediate value and a clear path to integration.
