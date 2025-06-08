# Eva Onboarding Concierge - Optimized Deployment Guide

This guide provides optimized deployment instructions following the travel-concierge reference patterns for best practices.

## 🚀 Quick Start

### Prerequisites

1. **Google Cloud Project** with the following APIs enabled:
   - Vertex AI API
   - Agent Engine API
   - Cloud Storage API

2. **Authentication**:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Environment Variables**:
   ```bash
   export GOOGLE_CLOUD_PROJECT=your-project-id
   export GOOGLE_CLOUD_LOCATION=us-central1
   export GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket-name
   ```

### 🎯 Optimized Deployment

#### Option 1: Command Line Deployment (Recommended)

```bash
# Navigate to the project directory
cd eva_onboarding_concierge

# Create new deployment
python deployment/deploy_optimized.py --create

# Test the deployment
python deployment/deploy_optimized.py --quicktest --resource_id=YOUR_RESOURCE_ID

# Delete deployment when done
python deployment/deploy_optimized.py --delete --resource_id=YOUR_RESOURCE_ID
```

#### Option 2: Environment Variable Deployment

```bash
# Set environment variables
export GOOGLE_CLOUD_PROJECT=vital-octagon-19612
export GOOGLE_CLOUD_LOCATION=us-central1
export GOOGLE_CLOUD_STORAGE_BUCKET=2025-cathay-agentspace

# Deploy
python deployment/deploy_optimized.py --create
```

## 📋 Deployment Features

### ✅ Optimizations Applied

1. **Travel-Concierge Pattern**: Following proven deployment architecture
2. **Command Line Interface**: Using `absl` flags for flexible deployment
3. **Environment Management**: Proper environment variable handling
4. **Package Structure**: Optimized package imports and exports
5. **Dependency Management**: Minimal, focused dependencies
6. **Testing Integration**: Built-in quicktest functionality

### 🔧 Key Improvements

#### **1. Streamlined Dependencies**
```python
requirements=[
    "google-adk>=1.0.0",
    "google-cloud-aiplatform[agent_engines]>=1.93.1", 
    "google-genai>=1.16.1",
    "pydantic>=2.10.6,<3.0.0",
    "python-dotenv>=1.0.1",
    "PyPDF2>=3.0.0",
    "pdfplumber>=0.7.0",
]
```

#### **2. Proper Package Structure**
```
eva_onboarding_concierge/
├── agent.py                    # Main entry point
├── __init__.py                 # Package exports
├── deployment/
│   ├── deploy_optimized.py     # Optimized deployment script
│   └── test_deployment.py      # Testing utilities
└── [sub_agents]/               # Specialist agents
```

#### **3. Command Line Interface**
```bash
# Flexible deployment options
python deployment/deploy_optimized.py --create
python deployment/deploy_optimized.py --quicktest --resource_id=ID
python deployment/deploy_optimized.py --delete --resource_id=ID
```

## 🧪 Testing

### Quick Test
```bash
python deployment/deploy_optimized.py --quicktest --resource_id=YOUR_RESOURCE_ID
```

### Custom Test Message
```python
from google.adk.sessions import VertexAiSessionService
from vertexai import agent_engines

# Get deployed agent
remote_agent = agent_engines.get("YOUR_RESOURCE_ID")

# Create session
session_service = VertexAiSessionService(PROJECT_ID, LOCATION)
session = session_service.create_session(
    app_name="YOUR_RESOURCE_ID",
    user_id="test_user"
)

# Send message
for event in remote_agent.stream_query(
    user_id="test_user",
    session_id=session.id,
    message="Hi Eva! I need to onboard a new employee named Sarah Chen."
):
    print(event)
```

## 📊 Deployment Comparison

### Before Optimization
- ❌ Complex deployment script
- ❌ Many unnecessary dependencies
- ❌ Manual configuration required
- ❌ No built-in testing
- ❌ Inconsistent package structure

### After Optimization
- ✅ Simple command-line deployment
- ✅ Minimal, focused dependencies
- ✅ Environment variable automation
- ✅ Built-in quicktest functionality
- ✅ Travel-concierge proven patterns

## 🎯 Usage Examples

### 1. Development Deployment
```bash
# Quick development deployment
python deployment/deploy_optimized.py --create

# Test with sample onboarding request
python deployment/deploy_optimized.py --quicktest --resource_id=YOUR_ID
```

### 2. Production Deployment
```bash
# Set production environment
export GOOGLE_CLOUD_PROJECT=prod-project-id
export GOOGLE_CLOUD_LOCATION=us-central1
export GOOGLE_CLOUD_STORAGE_BUCKET=prod-bucket

# Deploy to production
python deployment/deploy_optimized.py --create
```

### 3. Cleanup
```bash
# Remove deployment
python deployment/deploy_optimized.py --delete --resource_id=YOUR_ID
```

## 🔍 Troubleshooting

### Common Issues

1. **Authentication Error**:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

2. **Missing APIs**:
   ```bash
   gcloud services enable aiplatform.googleapis.com
   gcloud services enable storage.googleapis.com
   ```

3. **Bucket Permissions**:
   ```bash
   gsutil mb gs://your-bucket-name
   gsutil iam ch user:your-email@domain.com:objectAdmin gs://your-bucket-name
   ```

## 🌟 Benefits of Optimization

### **⚡ Faster Deployment**
- Reduced dependencies (15 → 7)
- Streamlined package structure
- Automated environment setup

### **🔧 Better Maintainability**
- Clear separation of concerns
- Consistent with ADK best practices
- Easy testing and debugging

### **📦 Cleaner Architecture**
- Following travel-concierge patterns
- Proper package exports
- Minimal surface area

### **🚀 Production Ready**
- Environment variable management
- Proper error handling
- Built-in testing capabilities

## 📚 Next Steps

1. **Deploy Eva**: Use the optimized deployment script
2. **Test Functionality**: Run quicktest to verify deployment
3. **Customize**: Modify agents for your specific use case
4. **Scale**: Deploy to multiple environments as needed

**Eva Onboarding Concierge is now optimized for fast, reliable, and maintainable deployment! 🎉**
