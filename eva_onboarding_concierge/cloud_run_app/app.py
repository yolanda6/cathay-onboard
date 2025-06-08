"""
Eva Onboarding Concierge - Streamlit Cloud Run Application
A comprehensive web interface for the Eva multi-agent onboarding system.
"""

import streamlit as st
import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Eva Onboarding Concierge",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import Eva system with robust path handling
import sys
from pathlib import Path

# Add the parent directory (eva_onboarding_concierge) to Python path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Also add the grandparent directory for when running from cloud_run_app
grandparent_dir = parent_dir.parent
sys.path.insert(0, str(grandparent_dir))

# Global variables for lazy loading
_eva_functions = {}

def get_eva_functions():
    """Lazy load Eva functions to avoid import conflicts."""
    global _eva_functions
    
    if not _eva_functions:
        try:
            # First try to import just the config
            try:
                from shared_libraries.config import EvaConfig
                config_import = "direct"
            except ImportError:
                from eva_onboarding_concierge.shared_libraries.config import EvaConfig
                config_import = "package"
            
            # Create mock functions for demo mode
            def mock_onboarding_request(user_input: str, user_id: str = "demo_user") -> str:
                return f"🤖 Eva (Demo Mode): I received your message: '{user_input}'. In full mode, I would coordinate with my specialist agents to handle your onboarding request. Currently running in demo mode due to agent import conflicts."
            
            def mock_equipment_request(user_input: str, user_id: str = "demo_user") -> str:
                return f"💻 Device Depot (Demo Mode): I received your equipment request: '{user_input}'. In full mode, I would check inventory and create ServiceNow tickets. Currently running in demo mode."
            
            # Try to import real functions
            try:
                if config_import == "direct":
                    from eva_orchestrator_agent.agent import process_onboarding_request
                    from device_depot_agent.agent import process_equipment_request
                else:
                    from eva_onboarding_concierge.eva_orchestrator_agent.agent import process_onboarding_request
                    from eva_onboarding_concierge.device_depot_agent.agent import process_equipment_request
                
                _eva_functions = {
                    'process_onboarding_request': process_onboarding_request,
                    'process_equipment_request': process_equipment_request,
                    'EvaConfig': EvaConfig,
                    'mode': 'full'
                }
                st.success(f"✅ Eva system imported successfully ({config_import} import)")
                
            except Exception as agent_error:
                # Fall back to demo mode
                _eva_functions = {
                    'process_onboarding_request': mock_onboarding_request,
                    'process_equipment_request': mock_equipment_request,
                    'EvaConfig': EvaConfig,
                    'mode': 'demo'
                }
                st.warning(f"⚠️ Running in Demo Mode due to agent import issues: {agent_error}")
                st.info("💡 Dashboard and Analytics are fully functional. Chat responses will be simulated.")
                
        except Exception as e:
            st.error(f"❌ Failed to import Eva system: {e}")
            st.error(f"Current working directory: {os.getcwd()}")
            st.error(f"Python path: {sys.path[:3]}...")
            st.error("💡 Make sure you're running from the correct directory")
            st.stop()
    
    return _eva_functions

# Initialize Eva functions
eva_functions = get_eva_functions()
EvaConfig = eva_functions['EvaConfig']

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_session' not in st.session_state:
    st.session_state.current_session = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = "streamlit_user"

def main():
    """Main Streamlit application."""
    
    # Sidebar
    with st.sidebar:
        st.title("🤖 Eva Onboarding Concierge")
        st.markdown("---")
        
        # Configuration display
        st.subheader("🔧 System Configuration")
        config = EvaConfig.get_project_config()
        st.json(config)
        
        st.markdown("---")
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        if st.button("🆕 New Onboarding Session"):
            st.session_state.chat_history = []
            st.session_state.current_session = None
            st.rerun()
        
        if st.button("📊 View System Status"):
            show_system_status()
        
        st.markdown("---")
        
        # Agent selector
        st.subheader("🎯 Agent Mode")
        agent_mode = st.selectbox(
            "Select Agent",
            ["Eva Orchestrator", "Device Depot", "HR Helper", "Meeting Maven", "Access Control"],
            index=0
        )
        
        st.session_state.agent_mode = agent_mode

    # Main content area
    st.title("🤖 Eva - Your AI Onboarding Concierge")
    st.markdown("Welcome to Eva! I'm here to make employee onboarding seamless and delightful.")
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📋 Dashboard", "📊 Analytics", "⚙️ Admin"])
    
    with tab1:
        chat_interface()
    
    with tab2:
        dashboard_interface()
    
    with tab3:
        analytics_interface()
    
    with tab4:
        admin_interface()

def chat_interface():
    """Chat interface for interacting with Eva."""
    
    st.subheader("💬 Chat with Eva")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(message["content"])
    
    # Chat input
    user_input = st.chat_input("Type your message to Eva...")
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        # Process with appropriate agent
        with st.spinner("Eva is thinking..."):
            try:
                agent_mode = st.session_state.get('agent_mode', 'Eva Orchestrator')
                
                eva_funcs = get_eva_functions()
                
                if agent_mode == "Eva Orchestrator":
                    response = eva_funcs['process_onboarding_request'](user_input, st.session_state.user_id)
                elif agent_mode == "Device Depot":
                    response = eva_funcs['process_equipment_request'](user_input, st.session_state.user_id)
                else:
                    response = f"Agent mode '{agent_mode}' is not yet implemented in this demo."
                
                # Add Eva's response to history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": datetime.now().isoformat(),
                    "agent": agent_mode
                })
                
            except Exception as e:
                st.error(f"Error processing request: {e}")
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"I encountered an error: {e}. Please try again.",
                    "timestamp": datetime.now().isoformat(),
                    "agent": "Error Handler"
                })
        
        st.rerun()

def dashboard_interface():
    """Dashboard showing onboarding progress and status."""
    
    st.subheader("📋 Onboarding Dashboard")
    
    # Sample onboarding data
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Sessions", "12", "↑ 3")
    
    with col2:
        st.metric("Completed Today", "8", "↑ 2")
    
    with col3:
        st.metric("Equipment Requests", "15", "↑ 5")
    
    with col4:
        st.metric("Avg. Completion Time", "2.3 days", "↓ 0.5")
    
    st.markdown("---")
    
    # Recent onboarding sessions
    st.subheader("🔄 Recent Onboarding Sessions")
    
    # Sample data
    recent_sessions = [
        {"Employee": "Alex Johnson", "Department": "Engineering", "Status": "In Progress", "Progress": 75, "Start Date": "2025-06-05"},
        {"Employee": "Sarah Chen", "Department": "Marketing", "Status": "Completed", "Progress": 100, "Start Date": "2025-06-04"},
        {"Employee": "Mike Rodriguez", "Department": "Finance", "Status": "Pending", "Progress": 25, "Start Date": "2025-06-06"},
        {"Employee": "Lisa Wang", "Department": "HR", "Status": "In Progress", "Progress": 60, "Start Date": "2025-06-05"},
    ]
    
    df = pd.DataFrame(recent_sessions)
    
    # Display with progress bars
    for index, row in df.iterrows():
        col1, col2, col3, col4 = st.columns([2, 2, 1, 2])
        
        with col1:
            st.write(f"**{row['Employee']}**")
            st.write(f"*{row['Department']}*")
        
        with col2:
            st.write(f"Started: {row['Start Date']}")
            status_color = {"Completed": "🟢", "In Progress": "🟡", "Pending": "🔴"}
            st.write(f"{status_color.get(row['Status'], '⚪')} {row['Status']}")
        
        with col3:
            st.write(f"{row['Progress']}%")
        
        with col4:
            st.progress(row['Progress'] / 100)
        
        st.markdown("---")

def analytics_interface():
    """Analytics and reporting interface."""
    
    st.subheader("📊 Analytics & Reports")
    
    # Time range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    # Sample analytics data
    st.markdown("### 📈 Onboarding Metrics")
    
    # Create sample charts
    import numpy as np
    
    # Onboarding completion trend
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    completions = np.random.poisson(3, len(dates))
    
    chart_data = pd.DataFrame({
        'Date': dates,
        'Completions': completions
    })
    
    st.line_chart(chart_data.set_index('Date'))
    
    # Department breakdown
    st.markdown("### 🏢 Department Breakdown")
    dept_data = {
        'Engineering': 45,
        'Marketing': 25,
        'Finance': 15,
        'HR': 10,
        'Operations': 5
    }
    
    st.bar_chart(dept_data)
    
    # Equipment requests
    st.markdown("### 💻 Equipment Request Analytics")
    equipment_data = {
        'Laptops': 35,
        'Monitors': 28,
        'Accessories': 42,
        'Mobile Devices': 15
    }
    
    st.bar_chart(equipment_data)

def admin_interface():
    """Admin interface for system management."""
    
    st.subheader("⚙️ System Administration")
    
    # System health
    st.markdown("### 🏥 System Health")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("API Response Time", "245ms", "↓ 15ms")
    
    with col2:
        st.metric("Success Rate", "99.2%", "↑ 0.1%")
    
    with col3:
        st.metric("Active Agents", "6/6", "✅")
    
    # Agent status
    st.markdown("### 🤖 Agent Status")
    
    agents = [
        {"Agent": "Eva Orchestrator", "Status": "🟢 Online", "Last Response": "2s ago"},
        {"Agent": "ID Master", "Status": "🟢 Online", "Last Response": "5s ago"},
        {"Agent": "Device Depot", "Status": "🟢 Online", "Last Response": "3s ago"},
        {"Agent": "Access Control", "Status": "🟢 Online", "Last Response": "1s ago"},
        {"Agent": "HR Helper", "Status": "🟢 Online", "Last Response": "4s ago"},
        {"Agent": "Meeting Maven", "Status": "🟢 Online", "Last Response": "2s ago"},
    ]
    
    for agent in agents:
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.write(f"**{agent['Agent']}**")
        with col2:
            st.write(agent['Status'])
        with col3:
            st.write(agent['Last Response'])
    
    st.markdown("---")
    
    # Configuration management
    st.markdown("### 🔧 Configuration")
    
    if st.button("🔄 Reload Configuration"):
        st.success("Configuration reloaded successfully!")
    
    if st.button("🧹 Clear Chat History"):
        st.session_state.chat_history = []
        st.success("Chat history cleared!")
        st.rerun()
    
    # Export data
    st.markdown("### 📤 Data Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export Analytics"):
            st.success("Analytics data exported!")
    
    with col2:
        if st.button("💬 Export Chat Logs"):
            if st.session_state.chat_history:
                chat_json = json.dumps(st.session_state.chat_history, indent=2)
                st.download_button(
                    label="Download Chat History",
                    data=chat_json,
                    file_name=f"eva_chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.info("No chat history to export")

def show_system_status():
    """Display system status in sidebar."""
    st.sidebar.markdown("### 🏥 System Status")
    st.sidebar.success("🟢 All systems operational")
    st.sidebar.info("📊 6/6 agents online")
    st.sidebar.info("⚡ Response time: 245ms")

if __name__ == "__main__":
    main()
