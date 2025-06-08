"""
Cloud Run Deployment Script for Eva Onboarding Concierge
Deploys the Streamlit application to Google Cloud Run.
"""

import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "vital-octagon-19612")
REGION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
SERVICE_NAME = "eva-onboarding-concierge"
IMAGE_NAME = f"gcr.io/{PROJECT_ID}/{SERVICE_NAME}"

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n🔄 {description}")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def check_prerequisites():
    """Check if required tools are installed."""
    print("🔍 Checking prerequisites...")
    
    # Check if gcloud is installed
    try:
        subprocess.run(["gcloud", "version"], check=True, capture_output=True)
        print("✅ Google Cloud CLI is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Google Cloud CLI is not installed")
        print("Please install it from: https://cloud.google.com/sdk/docs/install")
        return False
    
    # Check if Docker is installed
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        print("✅ Docker is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker is not installed")
        print("Please install Docker from: https://docs.docker.com/get-docker/")
        return False
    
    return True

def setup_gcloud():
    """Set up Google Cloud configuration."""
    print(f"\n🔧 Setting up Google Cloud configuration...")
    
    # Set project
    if not run_command(f"gcloud config set project {PROJECT_ID}", "Setting project"):
        return False
    
    # Enable required APIs
    apis = [
        "cloudbuild.googleapis.com",
        "run.googleapis.com",
        "containerregistry.googleapis.com"
    ]
    
    for api in apis:
        if not run_command(f"gcloud services enable {api}", f"Enabling {api}"):
            return False
    
    return True

def build_and_push_image():
    """Build and push Docker image to Google Container Registry."""
    print(f"\n🐳 Building and pushing Docker image...")
    
    # Build the image
    if not run_command(f"docker build -t {IMAGE_NAME} .", "Building Docker image"):
        return False
    
    # Configure Docker to use gcloud as credential helper
    if not run_command("gcloud auth configure-docker", "Configuring Docker authentication"):
        return False
    
    # Push the image
    if not run_command(f"docker push {IMAGE_NAME}", "Pushing image to Container Registry"):
        return False
    
    return True

def deploy_to_cloud_run():
    """Deploy the application to Cloud Run."""
    print(f"\n🚀 Deploying to Cloud Run...")
    
    # Deploy command
    deploy_cmd = f"""
    gcloud run deploy {SERVICE_NAME} \
        --image {IMAGE_NAME} \
        --platform managed \
        --region {REGION} \
        --allow-unauthenticated \
        --port 8080 \
        --memory 2Gi \
        --cpu 2 \
        --timeout 3600 \
        --concurrency 80 \
        --max-instances 10 \
        --set-env-vars GOOGLE_CLOUD_PROJECT={PROJECT_ID} \
        --set-env-vars GOOGLE_CLOUD_LOCATION={REGION} \
        --set-env-vars GOOGLE_GENAI_USE_VERTEXAI=TRUE
    """.strip().replace('\n    ', ' ')
    
    if not run_command(deploy_cmd, "Deploying to Cloud Run"):
        return False
    
    return True

def get_service_url():
    """Get the deployed service URL."""
    print(f"\n🔗 Getting service URL...")
    
    try:
        result = subprocess.run(
            f"gcloud run services describe {SERVICE_NAME} --region {REGION} --format 'value(status.url)'",
            shell=True, check=True, capture_output=True, text=True
        )
        url = result.stdout.strip()
        print(f"✅ Service deployed successfully!")
        print(f"🌐 URL: {url}")
        return url
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to get service URL: {e.stderr}")
        return None

def main():
    """Main deployment function."""
    print("🤖 Eva Onboarding Concierge - Cloud Run Deployment")
    print("=" * 60)
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Setup Google Cloud
    if not setup_gcloud():
        print("❌ Failed to setup Google Cloud configuration")
        sys.exit(1)
    
    # Build and push image
    if not build_and_push_image():
        print("❌ Failed to build and push Docker image")
        sys.exit(1)
    
    # Deploy to Cloud Run
    if not deploy_to_cloud_run():
        print("❌ Failed to deploy to Cloud Run")
        sys.exit(1)
    
    # Get service URL
    url = get_service_url()
    
    if url:
        print("\n🎉 Deployment completed successfully!")
        print("=" * 60)
        print(f"🌐 Eva Onboarding Concierge is now live at: {url}")
        print("\n📋 What you can do:")
        print("• Chat with Eva in the main interface")
        print("• View onboarding dashboard and analytics")
        print("• Manage system administration")
        print("• Export data and chat logs")
        print("\n🔧 To update the deployment:")
        print("1. Make changes to your code")
        print("2. Run this script again")
        print("3. The new version will be deployed automatically")
    else:
        print("❌ Deployment may have issues. Check the logs.")
        sys.exit(1)

if __name__ == "__main__":
    main()
