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
import sys

def main(argv: list[str]) -> None:
    """
    Test the deployed Eva Onboarding Concierge Agent Engine.
    
    This script provides an interactive interface to test the deployed
    Eva multi-agent system through Agent Engine.
    """
    
    load_dotenv()

    PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "vital-octagon-19612")
    LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    STAGING_BUCKET = os.environ.get("GOOGLE_CLOUD_STORAGE_BUCKET", "2025-cathay-agentspace")
    AGENT_ENGINE_ID = os.environ.get("AGENT_ENGINE_ID")

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
    elif not AGENT_ENGINE_ID:
        print("❌ Missing required environment variable: AGENT_ENGINE_ID")
        print("   This should be set after running deployment/deploy.py")
        print("   Set it with: export AGENT_ENGINE_ID=your-agent-engine-id")
        return

    print("🧪 Eva Onboarding Concierge - Agent Engine Testing")
    print("=" * 60)
    print(f"📋 PROJECT: {PROJECT}")
    print(f"📍 LOCATION: {LOCATION}")
    print(f"📦 STAGING_BUCKET: gs://{STAGING_BUCKET}")
    print(f"🤖 AGENT_ENGINE_ID: {AGENT_ENGINE_ID}")
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

        # Get the deployed agent
        print("🔍 Connecting to deployed agent...")
        agent = agent_engines.get(AGENT_ENGINE_ID)
        print("✅ Connected to Eva Onboarding Concierge")

        # Create a session
        user_id = "test_user"
        print(f"📱 Creating session for user: {user_id}")
        session = agent.create_session(user_id=user_id)
        print(f"✅ Session created: {session['id']}")
        print()

        # Interactive testing
        print("🎯 Eva Onboarding Concierge - Interactive Testing")
        print("=" * 50)
        print("Hi! I'm Eva, your AI Onboarding Concierge. I can help you with:")
        print("• Employee onboarding and identity management")
        print("• IT equipment requests and provisioning")
        print("• Access control and security permissions")
        print("• HR policy questions and guidance")
        print("• Meeting scheduling and coordination")
        print("• Complete onboarding workflow orchestration")
        print()
        print("💡 Try these example requests:")
        print("   'I need to onboard Alex Johnson as a Software Engineer'")
        print("   'What's the vacation policy?'")
        print("   'Request a MacBook Pro for the new hire'")
        print("   'Schedule a welcome meeting with the manager'")
        print("   'What access does Alex need for the Engineering team?'")
        print()
        print("Type 'quit' to exit.")
        print("-" * 50)

        while True:
            user_input = input("\n🗣️  You: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if not user_input:
                continue

            print("🤖 Eva: ", end="", flush=True)
            
            try:
                response_parts = []
                for event in agent.stream_query(
                    user_id=user_id, 
                    session_id=session["id"], 
                    message=user_input
                ):
                    if "content" in event:
                        if "parts" in event["content"]:
                            parts = event["content"]["parts"]
                            for part in parts:
                                if "text" in part:
                                    text_part = part["text"]
                                    response_parts.append(text_part)
                                    print(text_part, end="", flush=True)
                
                if not response_parts:
                    print("(No response received)")
                else:
                    print()  # New line after response
                    
            except Exception as e:
                print(f"❌ Error during query: {e}")

        # Clean up
        print("\n🧹 Cleaning up session...")
        agent.delete_session(user_id=user_id, session_id=session["id"])
        print("✅ Session deleted successfully")
        print()
        print("🎉 Testing completed! Eva Onboarding Concierge is working perfectly.")
        print("🚀 Ready to transform employee onboarding with AI!")

    except Exception as e:
        print(f"❌ Testing failed: {e}")
        print()
        print("🔧 Troubleshooting:")
        print("1. Ensure the agent was deployed successfully")
        print("2. Check that AGENT_ENGINE_ID is correct")
        print("3. Verify you have access to the agent resource")
        print("4. Try running deployment/deploy.py again if needed")
        return

if __name__ == "__main__":
    app.run(main)
