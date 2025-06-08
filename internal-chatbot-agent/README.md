# Internal Chatbot Multi-Agent System

This project implements a multi-agent system using Google ADK (Agent Development Kit) for handling internal IT requests, specifically for adding users to Active Directory groups through a ServiceNow workflow.

## Architecture

The system consists of three main agents:

### 1. Root Orchestrator Agent
- **Role**: Coordinates the entire workflow between ServiceNow and Active Directory agents
- **Responsibilities**: 
  - Receives user requests for AD group access
  - Routes requests to appropriate sub-agents
  - Manages the complete workflow from start to finish
  - Provides status updates to users

### 2. ServiceNow Agent
- **Role**: Manages service requests and work orders
- **Responsibilities**:
  - Creates service requests for AD group owner approval
  - Monitors approval status and creates work orders
  - Closes work orders after AD operations complete
- **Tools**:
  - `create_service_request()`: Creates approval requests
  - `get_approval_status()`: Checks approval and creates work orders
  - `close_work_order()`: Closes completed work orders

### 3. Active Directory Agent
- **Role**: Manages AD group memberships
- **Responsibilities**:
  - Adds users to AD groups based on approved work orders
  - Verifies group memberships
  - Ensures proper access control
- **Tools**:
  - `add_user_to_ad_group()`: Adds users to groups
  - `verify_ad_group_membership()`: Verifies memberships

## Workflow Process

```
User Request → Root Agent → ServiceNow Agent → AD Agent → ServiceNow Agent → User Response
```

1. **User Request**: User requests access to an AD group
2. **Service Request Creation**: ServiceNow agent creates approval request
3. **Approval Process**: Mock approval from group owner (auto-approved for demo)
4. **Work Order Creation**: ServiceNow agent creates work order upon approval
5. **AD Operation**: AD agent adds user to the specified group
6. **Work Order Closure**: ServiceNow agent closes the work order
7. **Final Response**: Root agent provides completion status to user

## Mock Data

The system uses mock databases for demonstration:

### AD Groups
- `finance_team` (Owner: john.doe@company.com)
- `hr_team` (Owner: jane.smith@company.com)
- `engineering_team` (Owner: tech.lead@company.com)

### Service Requests & Work Orders
- Stored in-memory dictionaries
- Include status tracking and timestamps
- Support the complete approval workflow

## Installation

1. **Navigate to the project directory**:
   ```bash
   cd internal-chatbot-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   export GOOGLE_CLOUD_PROJECT="your-project-id"
   export GOOGLE_CLOUD_LOCATION="us-central1"
   export GOOGLE_GENAI_USE_VERTEXAI="TRUE"
   ```

## Usage

### Local Testing

1. **Run the agent locally**:
   ```bash
   python agent.py
   ```

2. **Test with predefined scenarios**:
   ```bash
   python test.py
   ```

3. **Interactive mode**:
   The agent script includes an interactive mode where you can enter requests manually.

### Example Requests

- "I need to add john.new@company.com to the finance_team group"
- "Please add sarah.dev@company.com to engineering_team"
- "Can you help me get access to hr_team for mike.hr@company.com?"

### Using ADK Commands

1. **Run the agent with ADK**:
   ```bash
   adk run .
   ```

2. **Run with web UI**:
   ```bash
   adk web
   ```

## Deployment

### Deploy to Agent Engine

1. **Uncomment the deployment section** in `agent.py`:
   ```python
   # Uncomment these lines for deployment
   from vertexai import agent_engines
   
   app = reasoning_engines.AdkApp(
       agent=root_agent,
       enable_tracing=True,
   )
   
   # ... rest of deployment code
   ```

2. **Run the deployment**:
   ```bash
   python agent.py
   ```

3. **Test the deployed agent**:
   ```bash
   python test.py <YOUR_DEPLOYED_ENGINE_ID>
   ```

### Deployment Configuration

Update the following variables in `agent.py` before deployment:
- `PROJECT_ID`: Your Google Cloud Project ID
- `LOCATION`: Your preferred location (e.g., "us-central1")
- `STAGING_BUCKET`: Your Cloud Storage bucket for staging

## API Response Format

The agents return structured responses with the following format:

```json
{
  "status": "success|error|info",
  "message": "Human-readable message",
  "request_id": "SR-XXXXXXXX",
  "work_order_id": "WO-XXXXXXXX",
  "group_name": "target_group",
  "new_user_email": "user@company.com"
}
```

## Features

### Multi-Agent Coordination
- Seamless handoffs between specialized agents
- State management across agent interactions
- Error handling and recovery

### Mock Approval Process
- Simulates real-world approval workflows
- Automatic approval for demonstration purposes
- Tracks approval timestamps and status

### Comprehensive Logging
- Detailed operation tracking
- Status updates at each workflow step
- Error reporting and debugging information

### Extensible Design
- Easy to add new AD groups
- Configurable approval processes
- Modular agent architecture

## Customization

### Adding New AD Groups
Update the `mock_ad_groups` dictionary in `agent.py`:

```python
mock_ad_groups["new_group"] = {
    "owner": "owner@company.com",
    "members": ["existing@company.com"],
    "description": "New group description"
}
```

### Modifying Approval Logic
Update the `get_approval_status()` function to implement custom approval logic:

```python
def get_approval_status(request_id: str) -> Dict[str, Any]:
    # Custom approval logic here
    pass
```

### Adding Real Database Integration
Replace the mock dictionaries with actual database connections:

```python
# Example with BigQuery
from google.cloud import bigquery

def create_service_request(group_name: str, new_user_email: str, requester_email: str):
    client = bigquery.Client()
    # Insert into BigQuery table
    pass
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Ensure you're authenticated with Google Cloud: `gcloud auth application-default login`
   - Verify your project ID and location settings

2. **Import Errors**:
   - Install all required dependencies: `pip install -r requirements.txt`
   - Ensure you're using the correct Python environment

3. **Agent Transfer Issues**:
   - Check agent instructions and transfer rules
   - Verify sub-agent configurations

### Debug Mode

Enable debug logging by adding:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the ADK documentation
3. Create an issue in the repository
