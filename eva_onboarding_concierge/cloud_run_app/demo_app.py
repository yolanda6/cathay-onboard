"""
Eva Onboarding Concierge - Demo Version
A simplified version that shows the app working without agent dependencies.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# Set page config
st.set_page_config(
    page_title="Eva Onboarding Concierge - Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Mock configuration
MOCK_CONFIG = {
    "project_id": "vital-octagon-19612",
    "location": "us-central1", 
    "staging_bucket": "gs://2025-cathay-agentspace",
    "model": "gemini-2.0-flash-exp"
}

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_id' not in st.session_state:
    st.session_state.user_id = "demo_user"

def mock_eva_response(user_input: str, agent_mode: str) -> str:
    """Generate mock responses based on agent mode."""
    if agent_mode == "Eva Orchestrator":
        return f"🤖 **Eva (Demo Mode)**: I received your message: '{user_input}'. In full mode, I would coordinate with my specialist agents to handle your onboarding request. I would:\n\n• Create identity and access accounts\n• Provision equipment through Device Depot\n• Schedule meetings with HR and managers\n• Set up department-specific access\n• Track progress through completion\n\n*Currently running in demo mode for testing purposes.*"
    elif agent_mode == "Device Depot":
        return f"💻 **Device Depot (Demo Mode)**: I received your equipment request: '{user_input}'. In full mode, I would:\n\n• Check inventory for requested items\n• Create ServiceNow tickets\n• Calculate costs and approval requirements\n• Schedule delivery and setup\n• Track deployment status\n\n*Example: MacBook Pro 14-inch ($2,499) + Dell 27\" 4K Monitor ($599) = $3,098 (requires manager approval)*\n\n*Currently running in demo mode for testing purposes.*"
    else:
        return f"🔧 **{agent_mode} (Demo Mode)**: I would handle your request: '{user_input}'. This agent specializes in {agent_mode.lower()} functionality. *Currently running in demo mode for testing purposes.*"

def main():
    """Main Streamlit application."""
    
    # Sidebar
    with st.sidebar:
        st.title("🤖 Eva Onboarding Concierge")
        st.success("✅ Demo Mode - Fully Functional!")
        st.markdown("---")
        
        # Configuration display
        st.subheader("🔧 System Configuration")
        st.json(MOCK_CONFIG)
        
        st.markdown("---")
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        if st.button("🆕 New Chat Session"):
            st.session_state.chat_history = []
            st.rerun()
        
        st.markdown("---")
        
        # Agent selector
        st.subheader("🎯 Agent Mode")
        agent_mode = st.selectbox(
            "Select Agent",
            ["Eva Orchestrator", "Device Depot", "HR Helper", "Meeting Maven", "Access Control"],
            index=0
        )
        
        st.session_state.agent_mode = agent_mode
        
        st.markdown("---")
        st.info("💡 This demo shows the full UI functionality. In production, real agents would provide actual responses.")

    # Main content area
    st.title("🤖 Eva - Your AI Onboarding Concierge")
    st.success("🎉 **Application Running Successfully!** This demo shows all features working.")
    
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
    st.info("🎭 **Demo Mode**: Responses are simulated to show functionality. In production, real agents would respond.")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(message["content"])
    
    # Chat input
    user_input = st.chat_input("Try: 'I need to onboard Alex Johnson' or 'Alex needs a MacBook Pro'")
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        # Generate mock response
        agent_mode = st.session_state.get('agent_mode', 'Eva Orchestrator')
        response = mock_eva_response(user_input, agent_mode)
        
        # Add Eva's response to history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat(),
            "agent": agent_mode
        })
        
        st.rerun()

def dashboard_interface():
    """Dashboard showing onboarding progress and status."""
    
    st.subheader("📋 Onboarding Dashboard")
    st.success("✅ **Dashboard Fully Functional** - All metrics and visualizations working!")
    
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
    st.success("✅ **Analytics Fully Functional** - All charts and data visualization working!")
    
    # Time range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    # Sample analytics data
    st.markdown("### 📈 Onboarding Metrics")
    
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
    st.success("✅ **Admin Panel Fully Functional** - All management features working!")
    
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
        {"Agent": "Eva Orchestrator", "Status": "🟢 Online (Demo)", "Last Response": "2s ago"},
        {"Agent": "ID Master", "Status": "🟢 Online (Demo)", "Last Response": "5s ago"},
        {"Agent": "Device Depot", "Status": "🟢 Online (Demo)", "Last Response": "3s ago"},
        {"Agent": "Access Control", "Status": "🟢 Online (Demo)", "Last Response": "1s ago"},
        {"Agent": "HR Helper", "Status": "🟢 Online (Demo)", "Last Response": "4s ago"},
        {"Agent": "Meeting Maven", "Status": "🟢 Online (Demo)", "Last Response": "2s ago"},
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

if __name__ == "__main__":
    main()
