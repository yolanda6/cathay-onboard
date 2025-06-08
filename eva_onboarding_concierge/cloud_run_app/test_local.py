"""
Local Testing Script for Eva Onboarding Concierge Streamlit App
Run this to test the application locally before deploying to Cloud Run.
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

def test_eva_import():
    """Test if Eva system can be imported."""
    print("\n🤖 Testing Eva system import...")
    
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
        
        try:
            # Try direct import first
            from shared_libraries.config import EvaConfig
            print("✅ Eva configuration imported successfully (direct import)")
        except ImportError:
            # Try with eva_onboarding_concierge prefix
            from eva_onboarding_concierge.shared_libraries.config import EvaConfig
            print("✅ Eva configuration imported successfully (package import)")
        
        config = EvaConfig.get_project_config()
        print(f"✅ Configuration loaded: {config}")
        
        # Test agent imports (just check if modules exist, don't import the full agents)
        try:
            import eva_orchestrator_agent.agent
            import device_depot_agent.agent
            print("✅ Agent modules found successfully (direct import)")
        except ImportError:
            try:
                import eva_onboarding_concierge.eva_orchestrator_agent.agent
                import eva_onboarding_concierge.device_depot_agent.agent
                print("✅ Agent modules found successfully (package import)")
            except ImportError as e:
                print(f"❌ Failed to find agent modules: {e}")
                return False
        
        return True
    except ImportError as e:
        print(f"❌ Failed to import Eva system: {e}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Python path: {sys.path[:3]}...")
        return False

def run_streamlit_app():
    """Run the Streamlit application locally."""
    print("\n🚀 Starting Streamlit application...")
    print("📱 The app will open in your browser at: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the application")
    
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
    print("🧪 Eva Onboarding Concierge - Local Testing")
    print("=" * 50)
    
    # Setup environment
    setup_environment()
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed")
        return
    
    # Test Eva import
    if not test_eva_import():
        print("❌ Eva system import failed")
        print("💡 Make sure you're running from the cloud_run_app directory")
        return
    
    print("\n✅ All checks passed! Starting the application...")
    print("\n📋 What to test:")
    print("• Chat with Eva in different agent modes")
    print("• Check the Dashboard tab for sample data")
    print("• View Analytics charts")
    print("• Test Admin panel functionality")
    print("• Try exporting chat history")
    
    # Run the app
    run_streamlit_app()

if __name__ == "__main__":
    main()
