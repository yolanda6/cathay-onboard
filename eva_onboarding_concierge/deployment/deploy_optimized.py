"""Deployment script for Eva Onboarding Concierge - Optimized following travel-concierge patterns."""

import asyncio
import os

from absl import app, flags
from dotenv import load_dotenv

from eva_onboarding_concierge.agent import root_agent

from google.adk.sessions import VertexAiSessionService

import vertexai
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp

FLAGS = flags.FLAGS
flags.DEFINE_string("project_id", None, "GCP project ID.")
flags.DEFINE_string("location", None, "GCP location.")
flags.DEFINE_string("bucket", None, "GCP bucket.")

flags.DEFINE_string("resource_id", None, "ReasoningEngine resource ID.")
flags.DEFINE_bool("create", False, "Creates a new deployment.")
flags.DEFINE_bool("quicktest", False, "Try a new deployment with one turn.")
flags.DEFINE_bool("delete", False, "Deletes an existing deployment.")
flags.mark_bool_flags_as_mutual_exclusive(["create", "delete", "quicktest"])


def create(env_vars: dict[str, str]) -> None:
    """Creates a new deployment."""
    print("🚀 Creating Eva Onboarding Concierge deployment...")
    print(f"Environment variables: {env_vars}")
    
    app_instance = AdkApp(
        agent=root_agent,
        enable_tracing=True,
        env_vars=env_vars,
    )

    remote_agent = agent_engines.create(  
        app_instance,
        display_name="Eva-Onboarding-Concierge-ADK",
        description="AI-powered employee onboarding orchestrator with specialist agents",                    
        requirements=[
            "google-adk>=1.0.0",
            "google-cloud-aiplatform[agent_engines]>=1.93.1",
            "google-genai>=1.16.1",
            "pydantic>=2.10.6,<3.0.0",
            "python-dotenv>=1.0.1",
            "PyPDF2>=3.0.0",
            "pdfplumber>=0.7.0",
        ],
        extra_packages=[
            "./eva_onboarding_concierge",  # The main package
        ],
    )
    print(f"✅ Created remote agent: {remote_agent.resource_name}")


def delete(resource_id: str) -> None:
    """Deletes an existing deployment."""
    remote_agent = agent_engines.get(resource_id)
    remote_agent.delete(force=True)
    print(f"🗑️ Deleted remote agent: {resource_id}")


def send_message(session_service: VertexAiSessionService, resource_id: str, message: str) -> None:
    """Send a message to the deployed agent."""

    session = asyncio.run(session_service.create_session(
            app_name=resource_id,
            user_id="eva_test_user"
        )
    )

    remote_agent = agent_engines.get(resource_id)

    print(f"🧪 Testing remote agent: {resource_id}")
    print(f"📝 Message: {message}")
    print("-" * 60)
    
    for event in remote_agent.stream_query(
        user_id="eva_test_user",
        session_id=session.id,
        message=message,
    ):
        print(event)
    print("✅ Test completed.")


def main(argv: list[str]) -> None:

    load_dotenv()
    env_vars = {}

    project_id = (
        FLAGS.project_id if FLAGS.project_id else os.getenv("GOOGLE_CLOUD_PROJECT")
    )
    location = FLAGS.location if FLAGS.location else os.getenv("GOOGLE_CLOUD_LOCATION")
    bucket = FLAGS.bucket if FLAGS.bucket else os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
    
    # Environment variables for Eva Onboarding Concierge
    env_vars["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"

    print("🎯 Eva Onboarding Concierge - Deployment Configuration")
    print("=" * 60)
    print(f"📋 PROJECT: {project_id}")
    print(f"📍 LOCATION: {location}")
    print(f"📦 BUCKET: {bucket}")

    if not project_id:
        print("❌ Missing required environment variable: GOOGLE_CLOUD_PROJECT")
        return
    elif not location:
        print("❌ Missing required environment variable: GOOGLE_CLOUD_LOCATION")
        return
    elif not bucket:
        print("❌ Missing required environment variable: GOOGLE_CLOUD_STORAGE_BUCKET")
        return

    vertexai.init(
        project=project_id,
        location=location,
        staging_bucket=f"gs://{bucket}",
    )

    if FLAGS.create:
        create(env_vars)
    elif FLAGS.delete:
        if not FLAGS.resource_id:
            print("❌ resource_id is required for delete")
            return
        delete(FLAGS.resource_id)
    elif FLAGS.quicktest:
        if not FLAGS.resource_id:
            print("❌ resource_id is required for quicktest")
            return
        session_service = VertexAiSessionService(project_id, location)
        send_message(
            session_service, 
            FLAGS.resource_id, 
            "Hi Eva! I need to onboard a new employee named Alex Johnson as a Software Developer in the Engineering department starting Monday."
        )
    else:
        print("❌ Unknown command. Use --create, --delete, or --quicktest")
        print()
        print("📖 Usage Examples:")
        print("  # Create new deployment:")
        print("  python deployment/deploy_optimized.py --create")
        print()
        print("  # Test existing deployment:")
        print("  python deployment/deploy_optimized.py --quicktest --resource_id=your-resource-id")
        print()
        print("  # Delete deployment:")
        print("  python deployment/deploy_optimized.py --delete --resource_id=your-resource-id")


if __name__ == "__main__":
    app.run(main)
