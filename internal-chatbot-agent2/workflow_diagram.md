# Internal Chatbot Multi-Agent Workflow

## System Architecture Diagram

```mermaid
graph TD
    A[User Request] --> B[Root Orchestrator Agent]
    B --> C{Request Type}
    C -->|AD Group Access| D[ServiceNow Agent]
    
    D --> E[Create Service Request]
    E --> F[Mock AD Group Owner Approval]
    F --> G[Create Work Order]
    G --> H[Return Work Order ID]
    
    H --> B
    B --> I[Active Directory Agent]
    I --> J[Add User to AD Group]
    J --> K[Verify Operation Success]
    K --> L[Return Operation Result]
    
    L --> B
    B --> M[ServiceNow Agent]
    M --> N[Close Work Order]
    N --> O[Update Service Request Status]
    O --> P[Return Completion Status]
    
    P --> B
    B --> Q[Final Response to User]
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style D fill:#e8f5e8
    style I fill:#fff3e0
    style Q fill:#e1f5fe
```

## Detailed Workflow Steps

### 1. Initial Request Processing
```mermaid
sequenceDiagram
    participant User
    participant Root as Root Agent
    participant SN as ServiceNow Agent
    
    User->>Root: "Add user@company.com to finance_team"
    Root->>Root: Parse request and identify workflow
    Root->>SN: Transfer to ServiceNow Agent
    SN->>SN: Extract user, group, and requester info
```

### 2. Service Request and Approval
```mermaid
sequenceDiagram
    participant SN as ServiceNow Agent
    participant DB as Mock Database
    participant Owner as Group Owner
    
    SN->>DB: Create service request
    DB-->>SN: Return request ID (SR-XXXXXXXX)
    SN->>Owner: Send approval request (mocked)
    Owner-->>SN: Auto-approve (for demo)
    SN->>DB: Create work order
    DB-->>SN: Return work order ID (WO-XXXXXXXX)
```

### 3. Active Directory Operations
```mermaid
sequenceDiagram
    participant Root as Root Agent
    participant AD as AD Agent
    participant ADDB as AD Database
    
    Root->>AD: Transfer with work order ID
    AD->>ADDB: Retrieve work order details
    AD->>ADDB: Add user to specified group
    ADDB-->>AD: Confirm user addition
    AD->>AD: Update work order status
    AD-->>Root: Return operation result
```

### 4. Work Order Closure
```mermaid
sequenceDiagram
    participant Root as Root Agent
    participant SN as ServiceNow Agent
    participant DB as Mock Database
    participant User
    
    Root->>SN: Transfer for work order closure
    SN->>DB: Close work order with success status
    SN->>DB: Update service request to completed
    DB-->>SN: Confirm closure
    SN-->>Root: Return closure confirmation
    Root-->>User: Provide final status update
```

## Agent Responsibilities Matrix

| Agent | Primary Role | Key Functions | Tools Used |
|-------|-------------|---------------|------------|
| **Root Orchestrator** | Workflow coordination | - Route requests<br>- Manage agent transfers<br>- Provide status updates | None (coordination only) |
| **ServiceNow Agent** | Request management | - Create service requests<br>- Monitor approvals<br>- Manage work orders | - `create_service_request()`<br>- `get_approval_status()`<br>- `close_work_order()` |
| **Active Directory Agent** | Access management | - Add users to groups<br>- Verify memberships<br>- Ensure security | - `add_user_to_ad_group()`<br>- `verify_ad_group_membership()` |

## Data Flow

### Mock Databases

#### AD Groups Structure
```json
{
  "group_name": {
    "owner": "owner@company.com",
    "members": ["user1@company.com", "user2@company.com"],
    "description": "Group description"
  }
}
```

#### Service Requests Structure
```json
{
  "request_id": {
    "request_id": "SR-XXXXXXXX",
    "group_name": "target_group",
    "new_user_email": "user@company.com",
    "requester_email": "requester@company.com",
    "group_owner": "owner@company.com",
    "status": "pending_approval|approved|completed",
    "created_at": "2024-01-01T00:00:00",
    "work_order_id": "WO-XXXXXXXX"
  }
}
```

#### Work Orders Structure
```json
{
  "work_order_id": {
    "work_order_id": "WO-XXXXXXXX",
    "request_id": "SR-XXXXXXXX",
    "group_name": "target_group",
    "new_user_email": "user@company.com",
    "status": "ready_for_execution|ad_operation_completed|completed",
    "created_at": "2024-01-01T00:00:00",
    "completion_status": "success|failed"
  }
}
```

## Error Handling

### Common Error Scenarios

1. **Invalid AD Group**
   - Detection: Group not found in mock database
   - Response: Error message with available groups
   - Recovery: User can retry with correct group name

2. **User Already in Group**
   - Detection: User email already in group members list
   - Response: Info message about existing membership
   - Recovery: No action needed, operation considered successful

3. **Work Order Not Found**
   - Detection: Work order ID not in database
   - Response: Error message with troubleshooting steps
   - Recovery: ServiceNow agent can recreate work order

4. **Agent Transfer Failures**
   - Detection: Sub-agent cannot be reached or returns error
   - Response: Root agent provides fallback response
   - Recovery: Retry mechanism or manual intervention

## Security Considerations

### Access Control
- Group owners must approve all access requests
- Users can only be added to existing, valid groups
- All operations are logged with timestamps

### Audit Trail
- Service requests track requester and approval chain
- Work orders link to original service requests
- AD operations record success/failure status

### Data Protection
- Email addresses are validated format
- Group membership changes are atomic operations
- Mock data simulates real-world security patterns

## Scalability Features

### Extensibility Points
1. **New Agent Types**: Easy to add specialized agents for other IT operations
2. **Database Integration**: Mock databases can be replaced with real systems
3. **Approval Workflows**: Configurable approval processes
4. **Notification Systems**: Integration points for email/Slack notifications

### Performance Considerations
- Asynchronous agent operations
- Stateless agent design for horizontal scaling
- Efficient session management
- Minimal memory footprint for mock data
