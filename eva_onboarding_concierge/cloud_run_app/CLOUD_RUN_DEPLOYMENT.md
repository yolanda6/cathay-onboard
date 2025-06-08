# Eva Onboarding Concierge - Cloud Run Deployment Guide

This guide provides step-by-step instructions for deploying Eva Onboarding Concierge to Google Cloud Run with a Streamlit frontend.

## 🏗️ **Architecture Overview**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Browser  │───▶│  Cloud Run App   │───▶│  Eva Agents     │
│   (Streamlit)   │    │  (Streamlit UI)  │    │  (ADK Backend)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Google Cloud    │
                       │  Services        │
                       │  (Vertex AI)     │
                       └──────────────────┘
```

## 📋 **Prerequisites**

### **1. Required Tools**
- **Google Cloud CLI** (gcloud)
- **Docker** 
- **Python 3.11+**
- **Git**

### **2. Google Cloud Setup**
- Google Cloud Project with billing enabled
- Required APIs enabled:
  - Cloud Run API
  - Cloud Build API
  - Container Registry API
  - Vertex AI API

### **3. Authentication**
```bash
# Authenticate with Google Cloud
gcloud auth login
gcloud auth application-default login

# Set your project
gcloud config set project YOUR_PROJECT_ID
```

## 🚀 **Quick Deployment**

### **Option 1: Automated Deployment (Recommended)**

```bash
# Navigate to the cloud run app directory
cd eva_onboarding_concierge/cloud_run_app

# Set environment variables
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_LOCATION=us-central1

# Run the automated deployment script
python deploy_cloud_run.py
```

### **Option 2: Manual Deployment**

#### **Step 1: Build Docker Image**
```bash
cd eva_onboarding_concierge/cloud_run_app

# Build the Docker image
docker build -t gcr.io/YOUR_PROJECT_ID/eva-onboarding-concierge .
```

#### **Step 2: Push to Container Registry**
```bash
# Configure Docker authentication
gcloud auth configure-docker

# Push the image
docker push gcr.io/YOUR_PROJECT_ID/eva-onboarding-concierge
```

#### **Step 3: Deploy to Cloud Run**
```bash
gcloud run deploy eva-onboarding-concierge \
    --image gcr.io/YOUR_PROJECT_ID/eva-onboarding-concierge \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8080 \
    --memory 2Gi \
    --cpu 2 \
    --timeout 3600 \
    --concurrency 80 \
    --max-instances 10 \
    --set-env-vars GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID \
    --set-env-vars GOOGLE_CLOUD_LOCATION=us-central1 \
    --set-env-vars GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

## 🎯 **Application Features**

### **💬 Chat Interface**
- **Real-time chat** with Eva Orchestrator
- **Agent selection** (Eva, Device Depot, HR Helper, etc.)
- **Chat history** with export functionality
- **Multi-turn conversations** with context

### **📋 Dashboard**
- **Onboarding metrics** and KPIs
- **Active sessions** tracking
- **Progress visualization** with charts
- **Recent activity** monitoring

### **📊 Analytics**
- **Completion trends** over time
- **Department breakdowns** 
- **Equipment request analytics**
- **Performance metrics**

### **⚙️ Admin Panel**
- **System health** monitoring
- **Agent status** tracking
- **Configuration management**
- **Data export** capabilities

## 🔧 **Configuration**

### **Environment Variables**
```bash
# Required
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=TRUE

# Optional
GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket-name
```

### **Resource Configuration**
```yaml
# Cloud Run Service Configuration
Memory: 2Gi
CPU: 2 cores
Timeout: 3600 seconds
Concurrency: 80 requests
Max Instances: 10
Port: 8080
```

## 📱 **Using the Application**

### **1. Access the Application**
After deployment, you'll receive a URL like:
```
https://eva-onboarding-concierge-xxxxx-uc.a.run.app
```

### **2. Chat with Eva**
```
User: "Hi Eva! I need to onboard a new employee named Alex Johnson"
Eva: "Hello! I'd be happy to help you onboard Alex Johnson. Let me start by gathering some information..."
```

### **3. Equipment Requests**
```
User: "Alex needs a MacBook Pro and monitor"
Device Depot: "I'll create an equipment request for Alex. Let me check our inventory..."
```

### **4. View Dashboard**
- Navigate to the **Dashboard** tab
- View active onboarding sessions
- Monitor completion metrics
- Track equipment requests

### **5. Analytics**
- Check the **Analytics** tab
- View completion trends
- Analyze department breakdowns
- Export reports

## 🔍 **Monitoring & Troubleshooting**

### **View Logs**
```bash
# View Cloud Run logs
gcloud logs read --service eva-onboarding-concierge --region us-central1

# Follow logs in real-time
gcloud logs tail --service eva-onboarding-concierge --region us-central1
```

### **Health Checks**
The application includes built-in health checks:
- **Endpoint**: `/_stcore/health`
- **Interval**: 30 seconds
- **Timeout**: 30 seconds

### **Common Issues**

#### **1. Import Errors**
```
Error: Failed to import Eva system
```
**Solution**: Ensure all dependencies are in requirements.txt

#### **2. Memory Issues**
```
Error: Container exceeded memory limit
```
**Solution**: Increase memory allocation in deployment

#### **3. Timeout Issues**
```
Error: Request timeout
```
**Solution**: Increase timeout or optimize agent response time

## 🔄 **Updates & Maintenance**

### **Update Deployment**
```bash
# Make code changes
# Then redeploy
python deploy_cloud_run.py
```

### **Scale Resources**
```bash
# Update memory and CPU
gcloud run services update eva-onboarding-concierge \
    --region us-central1 \
    --memory 4Gi \
    --cpu 4
```

### **Environment Variables**
```bash
# Update environment variables
gcloud run services update eva-onboarding-concierge \
    --region us-central1 \
    --set-env-vars NEW_VAR=value
```

## 💰 **Cost Optimization**

### **Resource Recommendations**
- **Development**: 1Gi memory, 1 CPU
- **Production**: 2Gi memory, 2 CPU
- **High Load**: 4Gi memory, 4 CPU

### **Auto-scaling**
```bash
# Set minimum instances to 0 for cost savings
gcloud run services update eva-onboarding-concierge \
    --region us-central1 \
    --min-instances 0 \
    --max-instances 10
```

## 🔒 **Security**

### **Authentication (Optional)**
```bash
# Require authentication
gcloud run services update eva-onboarding-concierge \
    --region us-central1 \
    --no-allow-unauthenticated
```

### **IAM Permissions**
```bash
# Grant access to specific users
gcloud run services add-iam-policy-binding eva-onboarding-concierge \
    --region us-central1 \
    --member user:user@example.com \
    --role roles/run.invoker
```

## 📊 **Performance Metrics**

### **Expected Performance**
- **Cold Start**: ~10-15 seconds
- **Warm Response**: ~1-3 seconds
- **Concurrent Users**: 80 per instance
- **Memory Usage**: ~1.5Gi under load

### **Monitoring**
```bash
# View metrics
gcloud monitoring metrics list --filter="resource.type=cloud_run_revision"
```

## 🎉 **Success Indicators**

After successful deployment, you should see:

✅ **Application accessible** at the provided URL
✅ **Chat interface** responding to messages
✅ **Dashboard** showing sample data
✅ **Analytics** displaying charts
✅ **Admin panel** showing system status
✅ **No errors** in Cloud Run logs

## 🆘 **Support**

### **Debugging Steps**
1. Check Cloud Run logs
2. Verify environment variables
3. Test locally with Docker
4. Check API quotas and limits
5. Verify IAM permissions

### **Common Commands**
```bash
# Check service status
gcloud run services describe eva-onboarding-concierge --region us-central1

# View recent deployments
gcloud run revisions list --service eva-onboarding-concierge --region us-central1

# Delete service
gcloud run services delete eva-onboarding-concierge --region us-central1
```

## 🎊 **Congratulations!**

You now have Eva Onboarding Concierge running on Google Cloud Run with:

- 🤖 **Full Eva multi-agent system**
- 💬 **Interactive Streamlit interface**
- 📊 **Real-time dashboard and analytics**
- ⚙️ **Admin panel for management**
- 🔄 **Auto-scaling and high availability**
- 🌐 **Global accessibility via HTTPS**

**Your AI-powered employee onboarding system is now live and ready to transform the onboarding experience! 🚀**
