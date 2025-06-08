# Eva - Your AI Onboarding Concierge 🤖

**A comprehensive multi-agent system built with Google's Agent Development Kit (ADK) that provides a seamless, "white-glove" onboarding experience for new employees.**

## 🌟 Overview

Eva is a sophisticated orchestration agent that acts as the "General Manager" for employee onboarding, coordinating a team of specialized sub-agents to handle everything from identity creation and IT provisioning to secure access requests and HR questions. This demonstrates a massive leap in efficiency and employee satisfaction through AI-powered automation.

## 🏗️ Architecture

Eva follows a modular, multi-agent architecture where each specialist agent handles specific domains:

```
Eva Orchestrator (General Manager)
├── ID Master Agent (Identity Management)
├── Device Depot Agent (IT Equipment)
├── Access Workflow Orchestrator (Security & Access)
├── HR Helper Agent (HR Policies & Questions)
└── Meeting Maven Agent (Calendar & Scheduling)
```

## 🤖 Agent Descriptions

### Eva Orchestrator Agent
- **Role**: Primary conversational AI and coordination hub
- **Responsibilities**: Manages end-to-end onboarding experience, delegates tasks to specialists
- **Key Features**: Progress tracking, comprehensive workflow orchestration, status reporting

### ID Master Agent
- **Role**: Digital identity creation and management
- **Responsibilities**: Active Directory accounts, email setup, access credentials
- **Simulates**: Microsoft Active Directory integration
- **Key Features**: Username generation, security group assignment, credential management

### Device Depot Agent
- **Role**: IT equipment provisioning and deployment
- **Responsibilities**: Equipment requests, approval workflows, delivery scheduling
- **Simulates**: ServiceNow ticket creation and management
- **Key Features**: Inventory management, cost approval, deployment tracking

### Access Workflow Orchestrator Agent
- **Role**: Secure access management (Enhanced from internal-chatbot-agent)
- **Responsibilities**: AD group access, multi-step approval workflows, compliance tracking
- **Simulates**: ServiceNow and Active Directory integration
- **Key Features**: Multi-level security validation, auto-approval workflows, audit trails

### HR Helper Agent
- **Role**: HR policy assistance and information
- **Responsibilities**: Policy questions, document search, orientation guidance
- **Data Sources**: Time Off Policy PDF, Performance Policy PDF
- **Key Features**: PDF content extraction, policy search, specialist routing

### Meeting Maven Agent
- **Role**: Meeting coordination and calendar management
- **Responsibilities**: Availability checking, meeting scheduling, calendar coordination
- **Simulates**: Google Calendar integration
- **Key Features**: Multi-attendee scheduling, conflict resolution, automated invitations

## 🚀 Key Features

### Comprehensive Onboarding Workflow
- **Identity Setup**: Automated account creation, email configuration, credential generation
- **Equipment Provisioning**: Smart equipment requests based on role, automated approvals
- **Access Management**: Secure group access with multi-level approvals and compliance
- **HR Coordination**: Policy guidance, orientation scheduling, benefits enrollment
- **Meeting Scheduling**: Welcome meetings, team introductions, buddy system setup

### Advanced Capabilities
- **Multi-level Security**: Different approval workflows based on sensitivity levels
- **Auto-approval**: Smart automation for standard, low-risk requests
- **Progress Tracking**: Real-time status updates and completion monitoring
- **Audit Trails**: Comprehensive logging for compliance and security
- **PDF Integration**: Direct policy document search and retrieval

### Enhanced Access Management
The Access Workflow Orchestrator includes advanced features:
- **Sensitivity Levels**: Critical, High, Medium, Low classification
- **Business Justification**: Required for high-sensitivity access
- **Access Duration**: Automatic expiration based on group sensitivity
- **Review Scheduling**: Ongoing compliance monitoring

## 📋 Onboarding Checklist

Eva manages a comprehensive 5-category checklist:

1. **Identity Management**
   - Create Active Directory account
   - Set up email account
   - Generate access credentials
   - Assign security groups

2. **Equipment Provisioning**
   - Request laptop and accessories
   - Schedule equipment delivery
   - Configure software and security

3. **Access Management**
   - Request department group access
   - Set up VPN and building access
   - Configure application permissions

4. **HR Orientation**
   - Complete HR paperwork
   - Review company policies
   - Set up benefits enrollment
   - Schedule orientation meetings

5. **Meeting Coordination**
   - Schedule welcome meeting with manager
   - Arrange team introduction sessions
   - Set up buddy system meetings
   - Plan first week schedule

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Google Cloud Project with ADK enabled
- Google ADK CLI installed (`pip install google-adk`)
- Required dependencies (see requirements.txt)

### Installation
```bash
# Clone or copy the eva_onboarding_concierge directory
cd eva_onboarding_concierge

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
export GOOGLE_GENAI_USE_VERTEXAI="TRUE"
```

### Configuration
Update the PROJECT_ID in each agent file:
```python
PROJECT_ID = "your-project-id"
LOCATION = "us-central1"
STAGING_BUCKET = "gs://your-staging-bucket"
```

## 🚀 Running Eva with ADK CLI

### Interactive Console Mode
```bash
# Run Eva in interactive console mode
adk run

# Or specify the directory explicitly
adk run eva_onboarding_concierge
```

### Web Interface Mode
```bash
# Launch Eva with web interface
adk web

# Or specify the directory explicitly
adk web eva_onboarding_concierge

# Access Eva at http://localhost:8080
```

### Custom Configuration
```bash
# Run with custom port
adk web --port 9000

# Run with verbose logging
adk run --verbose

# Run with specific agent module
adk run --agent eva_onboarding_concierge.agent
```

## 🎯 Usage Examples

### Basic Onboarding
```python
from eva_onboarding_concierge import process_onboarding_request

# Start a new employee onboarding
response = process_onboarding_request(
    "Hi Eva! I need to onboard Alex Johnson as a Software Developer in Engineering, starting Monday. His email will be alex.johnson@company.com"
)
print(response)
```

### Check Progress
```python
# Check onboarding status
response = process_onboarding_request(
    "What's the status of Alex Johnson's onboarding?"
)
print(response)
```

### Equipment Request
```python
# Request equipment
response = process_onboarding_request(
    "Alex needs a MacBook Pro and monitor for his work setup"
)
print(response)
```

### Schedule Meetings
```python
# Schedule welcome meeting
response = process_onboarding_request(
    "Can you schedule a welcome meeting between Alex and his manager for his first day?"
)
print(response)
```

### HR Questions
```python
# Ask HR policy questions
response = process_onboarding_request(
    "Alex has questions about the company's vacation policy"
)
print(response)
```

## 🧪 Testing

### Run Individual Agent Tests
```bash
# Test Eva Orchestrator
python eva_orchestrator_agent/agent.py

# Test ID Master
python id_master_agent/agent.py

# Test Device Depot
python device_depot_agent/agent.py

# Test Access Workflow Orchestrator
python access_workflow_orchestrator_agent/agent.py

# Test HR Helper
python hr_helper_agent/agent.py

# Test Meeting Maven
python meeting_maven_agent/agent.py
```

### Run Complete System Test
```python
from eva_onboarding_concierge.eva_orchestrator_agent.agent import test_eva_system
test_eva_system()
```

### Interactive Demo
```python
from eva_onboarding_concierge import start_eva_demo
start_eva_demo()
```

## 📊 System Capabilities

### Automation Level
- **Fully Automated**: Identity creation, email setup, low-cost equipment
- **Semi-Automated**: High-value equipment, sensitive access requests
- **Manual Oversight**: Critical security groups, executive-level access

### Integration Points
- **Active Directory**: User accounts, security groups, authentication
- **ServiceNow**: Ticket management, approval workflows, asset tracking
- **Google Calendar**: Meeting scheduling, availability checking
- **HR Systems**: Policy documents, employee data, benefits

### Security Features
- **Multi-level Approvals**: Based on cost, sensitivity, and risk
- **Audit Trails**: Comprehensive logging of all operations
- **Access Reviews**: Scheduled compliance monitoring
- **Principle of Least Privilege**: Minimal required access grants

## 🔧 Customization

### Adding New Equipment Types
Update the `mock_inventory` in `device_depot_agent/agent.py`:
```python
mock_inventory["new_category"] = {
    "item_key": {
        "model": "Item Name",
        "specs": "Specifications",
        "available": 10,
        "cost": 500,
        "category": "standard"
    }
}
```

### Adding New AD Groups
Update the `mock_ad_groups` in `access_workflow_orchestrator_agent/agent.py`:
```python
mock_ad_groups["new_group"] = {
    "owner": "owner@company.com",
    "members": [],
    "description": "Group description",
    "sensitivity_level": "medium",
    "approval_required": True,
    "auto_expire_days": 180
}
```

### Adding New HR Policies
1. Add PDF files to `hr_helper_agent/data/`
2. Update the PDF paths in `hr_helper_agent/agent.py`
3. Create new search functions for the policy content

## 📈 Metrics & Reporting

Eva provides comprehensive reporting on:
- **Onboarding Progress**: Real-time completion tracking
- **Equipment Costs**: Department-wise spending analysis
- **Access Requests**: Security compliance monitoring
- **Meeting Efficiency**: Scheduling success rates
- **Policy Queries**: Most common HR questions

## 🔮 Future Enhancements

### Planned Features
- **Real Integration**: Connect to actual AD, ServiceNow, Google Calendar
- **Machine Learning**: Predictive equipment needs, optimal scheduling
- **Mobile App**: Native mobile interface for managers and new hires
- **Analytics Dashboard**: Visual progress tracking and insights
- **Workflow Customization**: Department-specific onboarding flows

### Extension Points
- **Custom Agents**: Add domain-specific specialists
- **External APIs**: Integrate with additional enterprise systems
- **Notification Systems**: Email, Slack, Teams integration
- **Approval Workflows**: Custom business logic and routing

## 🤝 Contributing

This system demonstrates the power of Google's ADK for building sophisticated multi-agent systems. Key architectural patterns include:

- **Agent Orchestration**: Central coordination with specialist delegation
- **Tool Integration**: Function tools for external system simulation
- **Session Management**: Stateful conversations across agent interactions
- **Error Handling**: Graceful degradation and user feedback
- **Modular Design**: Easy extension and customization

## 📄 License

This project is part of the Google ADK workshop materials and is intended for educational and demonstration purposes.

## 🆘 Support

For questions about this demo system:
1. Review the agent-specific documentation in each subdirectory
2. Check the test files for usage examples
3. Examine the mock data structures for customization guidance
4. Refer to the Google ADK documentation for framework details

---

**Eva - Making employee onboarding effortless and delightful! 🎉**
