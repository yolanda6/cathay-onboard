# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from absl import app
import os
from dotenv import load_dotenv
import vertexai
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp
import sys

# Add the parent directory to the path to import the agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from agent import root_agent
except ImportError:
    # Fallback import path
    from eva_onboarding_concierge.agent import root_agent

def main(argv: list[str]) -> None:
    """
    Deploy Eva Onboarding Concierge to Google Cloud Agent Engine.
    
    This script deploys the Eva multi-agent system to GCP using the official
    ADK deployment pattern with Agent Engine.
    """
    
    load_dotenv()

    PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT","aimc-410006")# "vital-octagon-19612")
    PROJECT = "aimc-410006"

    LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    STAGING_BUCKET = os.environ.get("GOOGLE_CLOUD_STORAGE_BUCKET", "aimc-cathay-agentspace")#"2025-cathay-agentspace")

    if not PROJECT:
        print("❌ Missing required environment variable: GOOGLE_CLOUD_PROJECT")
        print("   Set it with: export GOOGLE_CLOUD_PROJECT=your-project-id")
        return
    elif not LOCATION:
        print("❌ Missing required environment variable: GOOGLE_CLOUD_LOCATION")
        print("   Set it with: export GOOGLE_CLOUD_LOCATION=us-central1")
        return
    elif not STAGING_BUCKET:
        print("❌ Missing required environment variable: GOOGLE_CLOUD_STORAGE_BUCKET")
        print("   Set it with: export GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket-name")
        return

    print("🚀 Eva Onboarding Concierge - Agent Engine Deployment")
    print("=" * 60)
    print(f"📋 PROJECT: {PROJECT}")
    print(f"📍 LOCATION: {LOCATION}")
    print(f"📦 STAGING_BUCKET: gs://{STAGING_BUCKET}")
    print()

    try:
        # Initialize Vertex AI
        print("🔧 Initializing Vertex AI...")
        vertexai.init(
            project=PROJECT,
            location=LOCATION,
            staging_bucket=f"gs://{STAGING_BUCKET}",
        )
        print("✅ Vertex AI initialized successfully")

        # Create ADK App
        print("📱 Creating ADK App with Eva root agent...")
        app_instance = AdkApp(agent=root_agent, enable_tracing=False)
        print("✅ ADK App created successfully")

        # Deploy to Agent Engine
        print("🚀 Deploying to Agent Engine...")
        print("   This may take several minutes...")
        
        remote_agent = agent_engines.create(
            app_instance,
            requirements=[
                "google-adk>=0.5.0",
                "google-cloud-aiplatform[adk,agent_engines]>=1.94.0",
                "google-genai>=0.3.0",
                "vertexai>=1.38.0",
                "pydantic>=2.0.0",
                "typing-extensions>=4.0.0",
                "PyPDF2>=3.0.0",
                "pdfplumber>=0.7.0"
            ],
            extra_packages=["../../eva_onboarding_concierge"],
        )

        print("🎉 Deployment completed successfully!")
        print()
        print("📋 Deployment Details:")
        print(f"   Agent Resource Name: {remote_agent.resource_name}")
        print()
        print("🔧 Next Steps:")
        print("1. Set the agent ID for testing:")
        print(f"   export AGENT_ENGINE_ID={remote_agent.resource_name}")
        print()
        print("2. Test the deployment:")
        print("   python deployment/test_deployment.py")
        print()
        print("3. Access via Google Cloud Console:")
        print(f"   https://console.cloud.google.com/ai/agents?project={PROJECT}")
        print()
        print("🌟 Eva Onboarding Concierge Features:")
        print("   • Employee Identity Management (ID Master Agent)")
        print("   • IT Equipment Provisioning (Device Depot Agent)")
        print("   • Access Control & Security (Access Workflow Orchestrator)")
        print("   • HR Policy Assistance (HR Helper Agent)")
        print("   • Meeting Scheduling (Meeting Maven Agent)")
        print("   • Multi-Agent Orchestration (Eva Orchestrator)")
        print()
        print("✅ Ready to transform employee onboarding with AI! 🚀")

    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        print()
        print("🔧 Troubleshooting:")
        print("1. Ensure you're authenticated: gcloud auth login")
        print("2. Check project permissions for Agent Engine")
        print("3. Verify staging bucket exists and is accessible")
        print("4. Ensure all required APIs are enabled")
        return

if __name__ == "__main__":
    app.run(main)
