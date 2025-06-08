# Eva Onboarding Concierge - Agent Engine Deployment

This directory contains the official ADK-style deployment scripts for deploying Eva Onboarding Concierge to Google Cloud Agent Engine.

## 🚀 Quick Start

### Prerequisites

1. **Google Cloud CLI** installed and authenticated
2. **Python 3.8+** with pip
3. **Google Cloud Project** with billing enabled
4. **Required APIs** enabled (see below)

### Setup Environment

1. **Copy environment configuration:**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env file with your values:**
   ```bash
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket-name
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Deploy to Agent Engine

1. **Run the deployment script:**
   ```bash
   python deployment/deploy.py
   ```

2. **Set the agent ID (from deployment output):**
   ```bash
   export AGENT_ENGINE_ID=projects/PROJECT_ID/locations/LOCATION/agents/AGENT_ID
   ```

3. **Test the deployment:**
   ```bash
   python deployment/test_deployment.py
   ```

## 📋 Detailed Setup

### Required Google Cloud APIs

Enable these APIs in your project:
```bash
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
```

### Authentication

Ensure you're authenticated with Google Cloud:
```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

### Staging Bucket

Create a staging bucket if it doesn't exist:
```bash
gsutil mb gs://your-bucket-name
```

## 🔧 Deployment Scripts

### `deploy.py`

The main deployment script that:
- Validates environment configuration
- Initializes Vertex AI
- Creates an ADK App with Eva root agent
- Deploys to Agent Engine with proper dependencies
- Provides deployment status and next steps

**Usage:**
```bash
python deployment/deploy.py
```

### `test_deployment.py`

Interactive testing script that:
- Connects to the deployed agent
- Creates a test session
- Provides an interactive chat interface
- Tests all Eva capabilities
- Cleans up resources

**Usage:**
```bash
export AGENT_ENGINE_ID=your-agent-id
python deployment/test_deployment.py
```

## 🌟 Eva Capabilities

The deployed system includes:

### **Eva Orchestrator (Root Agent)**
- Main conversation interface
- Routes requests to specialist agents
- Coordinates multi-agent workflows
- Manages onboarding sessions

### **Specialist Agents:**
1. **ID Master Agent** - Identity management and Active Directory
2. **Device Depot Agent** - IT equipment provisioning
3. **Access Workflow Orchestrator** - Security and access control
4. **HR Helper Agent** - Policy assistance with PDF search
5. **Meeting Maven Agent** - Calendar and meeting coordination

## 🧪 Testing Examples

Try these commands with the deployed agent:

```
"I need to onboard Alex Johnson as a Software Engineer"
"What's the vacation policy?"
"Request a MacBook Pro for the new hire"
"Schedule a welcome meeting with the manager"
"What access does Alex need for the Engineering team?"
"Check the status of Alex's onboarding"
```

## 🔍 Troubleshooting

### Common Issues

1. **Authentication Errors**
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

2. **Missing APIs**
   ```bash
   gcloud services enable aiplatform.googleapis.com
   ```

3. **Bucket Access Issues**
   ```bash
   gsutil ls gs://your-bucket-name
   ```

4. **Import Errors**
   - Ensure you're running from the eva_onboarding_concierge directory
   - Check that all dependencies are installed

### Deployment Logs

Check deployment logs in Google Cloud Console:
- Navigate to AI Platform > Agent Engine
- Find your deployed agent
- Check logs and monitoring

## 📊 Monitoring

After deployment, monitor your agent:
- **Google Cloud Console**: AI Platform > Agent Engine
- **Usage metrics**: Track conversations and performance
- **Error logs**: Monitor for issues and failures
- **Cost tracking**: Monitor usage and billing

## 🔄 Updates

To update the deployed agent:
1. Make changes to your agent code
2. Run `python deployment/deploy.py` again
3. Test with `python deployment/test_deployment.py`

## 🎯 Production Considerations

For production deployment:
- Use a dedicated GCP project
- Set up proper IAM roles and permissions
- Configure monitoring and alerting
- Implement backup and disaster recovery
- Set up CI/CD pipelines for automated deployment

## 📞 Support

For issues with deployment:
1. Check the troubleshooting section above
2. Review Google Cloud Console logs
3. Verify all prerequisites are met
4. Check ADK documentation for updates

## 🎉 Success!

Once deployed, Eva Onboarding Concierge will be available through:
- **Agent Engine API**: Programmatic access
- **Google Cloud Console**: Web interface
- **Custom integrations**: Via the Agent Engine SDK

Ready to transform employee onboarding with AI! 🚀
