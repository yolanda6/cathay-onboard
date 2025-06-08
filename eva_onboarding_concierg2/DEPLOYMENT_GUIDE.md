# Eva Onboarding Concierge - GCP Agent Engine Deployment Guide

This guide will help you deploy the Eva Onboarding Concierge system to Google Cloud Platform's Agent Engine.

## 🚀 Quick Start

### Prerequisites

Before deploying, ensure you have:

1. **Google Cloud CLI** installed and configured
2. **Google ADK (Agent Development Kit)** installed
3. **Python 3.8+** installed
4. **Active GCP Project** with billing enabled
5. **Appropriate IAM permissions** for Agent Engine

### Installation Commands

```bash
# Install Google Cloud CLI (if not already installed)
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Install Google ADK
pip install google-adk

# Authenticate with Google Cloud
gcloud auth login
gcloud auth application-default login
```

## 📋 Step-by-Step Deployment

### Step 1: Navigate to Project Directory

```bash
cd eva_onboarding_concierge
```

### Step 2: Run the Deployment Script

```bash
# Make the script executable (if not already)
chmod +x deploy.py

# Run the deployment
python deploy.py
```

### Step 3: Follow the Interactive Process

The deployment script will:

1. ✅ **Check Prerequisites** - Verify all tools are installed
2. 🔧 **Enable APIs** - Enable required Google Cloud APIs
3. 📦 **Setup Staging** - Create staging bucket for deployment
4. 📋 **Prepare Package** - Validate all agent files
5. 🚀 **Deploy Agent** - Deploy to GCP Agent Engine
6. 📊 **Check Status** - Verify deployment success
7. 📄 **Create Info** - Generate deployment information

## 🔧 Manual Deployment (Alternative)

If you prefer manual deployment:

```bash
# Set environment variables
export PROJECT_ID="vital-octagon-19612"
export LOCATION="us-central1"
export STAGING_BUCKET="gs://2025-cathay-agentspace"

# Deploy using ADK directly
adk deploy \
    --project-id $PROJECT_ID \
    --location $LOCATION \
    --staging-bucket $STAGING_BUCKET \
    --agent-name eva-onboarding-concierge \
    --display-name "Eva - AI Onboarding Concierge" \
    --description "Comprehensive AI-powered employee onboarding orchestrator" \
    .
```

## 🎯 Configuration Details

### Project Configuration
- **Project ID**: `vital-octagon-19612`
- **Location**: `us-central1`
- **Staging Bucket**: `gs://2025-cathay-agentspace`
- **Agent Name**: `eva-onboarding-concierge`

### Required APIs
The deployment script automatically enables:
- AI Platform API (`aiplatform.googleapis.com`)
- Cloud Storage API (`storage.googleapis.com`)
- Cloud Build API (`cloudbuild.googleapis.com`)
- Cloud Run API (`run.googleapis.com`)

### Agent Architecture
The deployed system includes:

1. **Eva Orchestrator** (Root Agent)
   - Main conversation interface
   - Routes requests to specialist agents
   - Coordinates multi-agent workflows

2. **ID Master Agent**
   - Creates user accounts
   - Manages digital identities
   - Handles Active Directory operations

3. **Device Depot Agent**
   - Manages equipment requests
   - Handles ServiceNow integration
   - Tracks deployment status

4. **HR Helper Agent**
   - Answers policy questions
   - Searches PDF documents
   - Provides HR assistance

5. **Access Workflow Orchestrator Agent**
   - Manages access requests
   - Handles security approvals
   - Coordinates with ServiceNow/AD

6. **Meeting Maven Agent**
   - Schedules meetings
   - Checks calendar availability
   - Manages Google Calendar integration

## 🔍 Verification

### Check Deployment Status

```bash
# List deployed agents
gcloud ai agents list --location=us-central1

# Get specific agent details
gcloud ai agents describe AGENT_ID --location=us-central1
```

### Test the Agent

1. **Via Google Cloud Console**:
   - Navigate to AI Platform > Agent Engine
   - Find "Eva - AI Onboarding Concierge"
   - Use the built-in chat interface

2. **Via API**:
   ```bash
   # Test API endpoint (replace AGENT_ID)
   curl -X POST \
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello Eva, help me onboard a new employee"}' \
     "https://us-central1-aiplatform.googleapis.com/v1/projects/vital-octagon-19612/locations/us-central1/agents/AGENT_ID:chat"
   ```

## 🌟 Features Available After Deployment

### Core Capabilities
- **Natural Language Processing**: Understands complex onboarding requests
- **Multi-Agent Coordination**: Seamlessly delegates to specialist agents
- **Document Integration**: Searches HR policies and procedures
- **Workflow Orchestration**: Manages end-to-end onboarding processes

### Example Interactions
```
User: "I need to onboard Alex Johnson as a Software Engineer"
Eva: "I'll help you onboard Alex Johnson. Let me coordinate with my specialist agents to:
      1. Create his digital identity and accounts
      2. Request his equipment (laptop, monitor, etc.)
      3. Set up his access permissions
      4. Schedule his orientation meetings
      5. Provide him with HR policy information"
```

### Supported Requests
- Employee account creation
- Equipment provisioning
- Access management
- Meeting scheduling
- HR policy questions
- Status tracking
- Multi-step workflows

## 🛠️ Troubleshooting

### Common Issues

1. **Authentication Errors**
   ```bash
   # Re-authenticate
   gcloud auth login
   gcloud auth application-default login
   ```

2. **Permission Errors**
   - Ensure you have Agent Engine Admin role
   - Check project billing is enabled
   - Verify APIs are enabled

3. **Deployment Failures**
   ```bash
   # Check logs
   gcloud logging read "resource.type=cloud_function" --limit=50
   
   # Verify staging bucket
   gsutil ls gs://2025-cathay-agentspace
   ```

4. **Agent Not Responding**
   - Check agent status in console
   - Verify all sub-agents are properly configured
   - Review deployment logs

### Getting Help

1. **Check deployment_info.json** for configuration details
2. **Review Google Cloud Console** for error messages
3. **Check ADK documentation** for latest updates
4. **Contact support** if issues persist

## 📊 Monitoring and Maintenance

### Performance Monitoring
- Monitor agent usage in Google Cloud Console
- Track response times and success rates
- Review conversation logs for improvements

### Updates and Maintenance
```bash
# Update the agent
python deploy.py  # Re-run deployment script

# Or use ADK directly
adk deploy --update .
```

### Scaling Considerations
- Monitor concurrent user limits
- Consider regional deployments for global usage
- Plan for peak onboarding periods

## 🎉 Success!

Once deployed, your Eva Onboarding Concierge will be available at:
- **Console URL**: https://console.cloud.google.com/ai/agents?project=vital-octagon-19612
- **Agent Interface**: Available through Google Cloud Console
- **API Endpoint**: Programmatically accessible via REST API

The system is now ready to handle comprehensive employee onboarding workflows with enterprise-grade security and scalability!
