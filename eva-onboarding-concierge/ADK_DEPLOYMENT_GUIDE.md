# Eva Onboarding Concierge - ADK Deployment Guide

## 📁 **Project Structure**

The Eva Onboarding Concierge has been reorganized to follow the ADK deployment structure:

```
eva-onboarding-concierge/
├── agent.py                    # Main orchestrator agent
├── requirements.txt            # Python dependencies
├── .env                       # Environment configuration
├── sub_agents/                # Specialist agents directory
│   ├── __init__.py
│   ├── id_master.py           # Identity management agent
│   ├── device_depot.py        # Equipment provisioning agent
│   ├── access_workflow_orchestrator.py  # Access management agent
│   ├── hr_helper.py           # HR policy assistance agent
│   └── meeting_maven.py       # Calendar management agent
└── ADK_DEPLOYMENT_GUIDE.md    # This deployment guide
```

## 🚀 **ADK Deployment Commands**

### **Option 1: Deploy with UI (Recommended)**

```bash
# Navigate to the project root directory
cd /usr/local/google/home/shirongl/google-adk-workshop

# Deploy Eva Onboarding Concierge with UI
adk deploy cloud_run eva-onboarding-concierge \
  --project=vital-octagon-19612 \
  --region=us-central1 \
  --with_ui \
  --trace_to_cloud \
  --service_name=eva-onboarding-concierge
```

### **Option 2: Deploy without UI**

```bash
# Deploy Eva Onboarding Concierge (agent only)
adk deploy cloud_run eva-onboarding-concierge \
  --project=vital-octagon-19612 \
  --region=us-central1 \
  --trace_to_cloud \
  --service_name=eva-onboarding-concierge
```

### **Option 3: Deploy with Custom Configuration**

```bash
# Deploy with custom settings
adk deploy cloud_run eva-onboarding-concierge \
  --project=vital-octagon-19612 \
  --region=us-central1 \
  --with_ui \
  --trace_to_cloud \
  --service_name=eva-onboarding-concierge \
  --memory=2Gi \
  --cpu=2 \
  --max_instances=10
```

## ⚙️ **Configuration Files**

### **Environment Variables (.env)**

The `.env` file contains all necessary configuration:

```env
# Google Cloud Project Configuration
GOOGLE_CLOUD_PROJECT=vital-octagon-19612
GOOGLE_CLOUD_LOCATION=us-central1
STAGING_BUCKET=gs://2025-cathay-agentspace

# Model Configuration
MODEL_NAME=gemini-2.0-flash-exp
TEMPERATURE=0.3
MAX_TOKENS=2048

# Agent Configuration
AGENT_ID=eva_onboarding_concierge
AGENT_NAME=Eva Onboarding Concierge
```

### **Dependencies (requirements.txt)**

```txt
# Core ADK dependencies
google-genai
adk

# Additional dependencies
python-dotenv
typing-extensions
pydantic
requests
pandas
numpy
```

## 🤖 **Agent Architecture**

### **Main Agent (agent.py)**

- **Eva Orchestrator**: Master coordinator that manages all sub-agents
- **Tools**: 
  - `coordinate_onboarding_workflow`
  - `delegate_to_specialist`
  - `track_onboarding_progress`
  - `handle_escalation`

### **Sub-Agents (sub_agents/)**

1. **ID Master** (`id_master.py`)
   - Digital identity creation and management
   - Active Directory integration
   - Password generation and security

2. **Device Depot** (`device_depot.py`)
   - IT equipment provisioning
   - ServiceNow ticket creation
   - Inventory management

3. **Access Workflow Orchestrator** (`access_workflow_orchestrator.py`)
   - Multi-step access approval workflows
   - Security compliance validation
   - Permission provisioning

4. **HR Helper** (`hr_helper.py`)
   - HR policy guidance
   - Time-off information
   - Performance process explanation

5. **Meeting Maven** (`meeting_maven.py`)
   - Calendar management
   - Meeting scheduling
   - Training coordination

## 🔧 **Pre-Deployment Checklist**

### **1. Verify File Structure**
```bash
# Check that all required files are present
ls -la eva-onboarding-concierge/
# Should show: agent.py, requirements.txt, .env, sub_agents/

ls -la eva-onboarding-concierge/sub_agents/
# Should show: __init__.py and all 5 agent files
```

### **2. Validate Configuration**
```bash
# Check .env file format
cat eva-onboarding-concierge/.env
# Ensure no syntax errors and proper variable formatting

# Check requirements.txt
cat eva-onboarding-concierge/requirements.txt
# Ensure clean format with no comments on package lines
```

### **3. Test Agent Locally (Optional)**
```bash
# Navigate to agent directory
cd eva-onboarding-concierge

# Test import
python -c "from agent import eva_orchestrator; print('✅ Agent imports successfully')"

# Test basic functionality
python -c "from agent import test_eva_system; print(test_eva_system())"
```

## 🚀 **Deployment Process**

### **Step 1: Authenticate with Google Cloud**
```bash
# Ensure you're authenticated
gcloud auth list
gcloud config set project vital-octagon-19612
```

### **Step 2: Run ADK Deployment**
```bash
# From the project root directory
adk deploy cloud_run eva-onboarding-concierge \
  --project=vital-octagon-19612 \
  --region=us-central1 \
  --with_ui \
  --trace_to_cloud \
  --service_name=eva-onboarding-concierge
```

### **Step 3: Configure Access (When Prompted)**
- **Unauthenticated Access**: Choose based on your security requirements
  - `Y` for public demo/testing
  - `N` for internal/secure deployment

### **Step 4: Verify Deployment**
```bash
# Check Cloud Run service
gcloud run services list --region=us-central1

# Get service URL
gcloud run services describe eva-onboarding-concierge \
  --region=us-central1 \
  --format="value(status.url)"
```

## 🧪 **Testing the Deployment**

### **1. Test Agent Endpoint**
```bash
# Test the deployed agent
curl -X POST "https://eva-onboarding-concierge-[hash]-uc.a.run.app/invoke" \
  -H "Content-Type: application/json" \
  -d '{"message": "I need to onboard Alex Johnson as a Software Developer"}'
```

### **2. Test UI (if deployed with --with_ui)**
```bash
# Open the UI in browser
open "https://eva-onboarding-concierge-[hash]-uc.a.run.app"
```

### **3. Test Sub-Agent Delegation**
```bash
# Test specific agent delegation
curl -X POST "https://eva-onboarding-concierge-[hash]-uc.a.run.app/invoke" \
  -H "Content-Type: application/json" \
  -d '{"message": "Check equipment inventory for laptops"}'
```

## 📊 **Monitoring & Observability**

### **Cloud Logging**
```bash
# View logs
gcloud logs read "resource.type=cloud_run_revision AND resource.labels.service_name=eva-onboarding-concierge" \
  --limit=50 \
  --format="table(timestamp,textPayload)"
```

### **Cloud Monitoring**
- Navigate to Cloud Console → Monitoring → Dashboards
- Create custom dashboard for Eva metrics
- Set up alerts for error rates and latency

### **Trace Analysis**
- Navigate to Cloud Console → Trace
- Analyze request flows through the multi-agent system
- Identify performance bottlenecks

## 🔧 **Troubleshooting**

### **Common Issues**

#### **1. Import Errors**
```bash
# Check Python path and imports
cd eva-onboarding-concierge
python -c "import sys; print(sys.path)"
python -c "from sub_agents import id_master_agent; print('✅ Sub-agent imports work')"
```

#### **2. Environment Variable Issues**
```bash
# Verify .env file format
cat .env | grep -v "^#" | grep "="
# Ensure no spaces around = signs
```

#### **3. Deployment Failures**
```bash
# Check ADK version
adk --version

# Verify project permissions
gcloud projects get-iam-policy vital-octagon-19612
```

#### **4. Runtime Errors**
```bash
# Check Cloud Run logs
gcloud logs tail "resource.type=cloud_run_revision AND resource.labels.service_name=eva-onboarding-concierge"
```

## 🔄 **Updates & Redeployment**

### **Update Agent Code**
```bash
# After making changes to agent.py or sub_agents/
adk deploy cloud_run eva-onboarding-concierge \
  --project=vital-octagon-19612 \
  --region=us-central1 \
  --with_ui \
  --trace_to_cloud \
  --service_name=eva-onboarding-concierge
```

### **Update Configuration**
```bash
# After updating .env or requirements.txt
adk deploy cloud_run eva-onboarding-concierge \
  --project=vital-octagon-19612 \
  --region=us-central1 \
  --with_ui \
  --trace_to_cloud \
  --service_name=eva-onboarding-concierge
```

## 📞 **Support & Resources**

### **ADK Documentation**
- [ADK Official Documentation](https://cloud.google.com/agent-development-kit)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)

### **Eva System Resources**
- **Agent Documentation**: `AGENT_DOCUMENTATION.md`
- **Architecture Diagrams**: `ARCHITECTURE_DIAGRAMS.md`
- **Original Implementation**: `eva_onboarding_concierge/` (legacy structure)

### **Getting Help**
- Check Cloud Run logs for runtime issues
- Verify .env file formatting
- Ensure all sub_agents files are properly structured
- Test imports locally before deployment

---

## ✅ **Quick Deployment Summary**

1. **Navigate to project root**: `cd /usr/local/google/home/shirongl/google-adk-workshop`
2. **Run deployment command**: 
   ```bash
   adk deploy cloud_run eva-onboarding-concierge \
     --project=vital-octagon-19612 \
     --region=us-central1 \
     --with_ui \
     --trace_to_cloud \
     --service_name=eva-onboarding-concierge
   ```
3. **Configure access when prompted**
4. **Test the deployed service**
5. **Monitor via Cloud Console**

**Your Eva Onboarding Concierge multi-agent system is now ready for ADK deployment! 🚀**
