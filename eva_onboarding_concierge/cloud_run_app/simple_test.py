"""
Simple Local Testing Script for Eva Onboarding Concierge Streamlit App
This version avoids agent import conflicts by only testing basic functionality.
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_environment():
    """Set up local environment variables."""
    print("🔧 Setting up local environment...")
    
    # Set environment variables for local testing
    os.environ["GOOGLE_CLOUD_PROJECT"] = os.getenv("GOOGLE_CLOUD_PROJECT", "vital-octagon-19612")
    os.environ["GOOGLE_CLOUD_LOCATION"] = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"
    
    print(f"✅ PROJECT: {os.environ['GOOGLE_CLOUD_PROJECT']}")
    print(f"✅ LOCATION: {os.environ['GOOGLE_CLOUD_LOCATION']}")
    print(f"✅ VERTEXAI: {os.environ['GOOGLE_GENAI_USE_VERTEXAI']}")

def check_dependencies():
    """Check if required dependencies are installed."""
    print("\n🔍 Checking dependencies...")
    
    required_packages = [
        "streamlit",
        "pandas",
        "numpy"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages)
        return True
    
    return True

def test_basic_imports():
    """Test basic imports without instantiating agents."""
    print("\n🤖 Testing basic Eva system structure...")
    
    try:
        # Add parent directory (eva_onboarding_concierge) to Python path
        current_dir = Path(__file__).parent
        parent_dir = current_dir.parent
        sys.path.insert(0, str(parent_dir))
        
        # Also add the grandparent directory for when running from cloud_run_app
        grandparent_dir = parent_dir.parent
        sys.path.insert(0, str(grandparent_dir))
        
        print(f"Current directory: {current_dir}")
        print(f"Parent directory: {parent_dir}")
        print(f"Grandparent directory: {grandparent_dir}")
        
        # Test basic config import
        try:
            from shared_libraries.config import EvaConfig
            print("✅ Eva configuration imported successfully (direct import)")
        except ImportError:
            from eva_onboarding_concierge.shared_libraries.config import EvaConfig
            print("✅ Eva configuration imported successfully (package import)")
        
        config = EvaConfig.get_project_config()
        print(f"✅ Configuration loaded: {config}")
        
        # Check if agent directories exist
        agent_dirs = [
            "eva_orchestrator_agent",
            "device_depot_agent", 
            "hr_helper_agent",
            "meeting_maven_agent",
            "id_master_agent"
        ]
        
        for agent_dir in agent_dirs:
            agent_path = parent_dir / agent_dir
            if agent_path.exists():
                print(f"✅ {agent_dir} directory found")
            else:
                print(f"❌ {agent_dir} directory not found")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to test Eva system: {e}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Python path: {sys.path[:3]}...")
        return False

def run_streamlit_app():
    """Run the Streamlit application locally."""
    print("\n🚀 Starting Streamlit application...")
    print("📱 The app will open in your browser at: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the application")
    print("\n⚠️  Note: Agent functionality will be loaded when you first interact with the chat.")
    
    try:
        subprocess.run([
            "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--server.headless", "false",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except FileNotFoundError:
        print("❌ Streamlit not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit"])
        print("✅ Streamlit installed. Please run the script again.")

def main():
    """Main testing function."""
    print("🧪 Eva Onboarding Concierge - Simple Local Testing")
    print("=" * 55)
    
    # Setup environment
    setup_environment()
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed")
        return
    
    # Test basic imports
    if not test_basic_imports():
        print("❌ Basic import test failed")
        print("💡 Make sure you're running from the cloud_run_app directory")
        return
    
    print("\n✅ Basic checks passed! Starting the application...")
    print("\n📋 What to test:")
    print("• The app will start with dashboard and analytics working")
    print("• Chat functionality will load when you first send a message")
    print("• If you get agent errors, they're expected on first load")
    print("• Try refreshing the page if you encounter issues")
    print("• Test different agent modes in the sidebar")
    
    # Run the app
    run_streamlit_app()

if __name__ == "__main__":
    main()
