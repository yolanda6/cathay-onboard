"""
Internal Chatbot Multi-Agent System

This __init__.py attempts to be compatible with both 'adk run .'
and 'adk web .'.
"""

import os
from vertexai.preview import reasoning_engines

# Import the actual agent logic from agent.py
from . import agent as agent_module

# Get the root_agent instance
actual_root_agent = agent_module.root_agent

# --- AdkApp instance for 'adk web' and deployment ---
# This 'app' instance should be picked up by 'adk web .'
app = reasoning_engines.AdkApp(
    agent=actual_root_agent,
    enable_tracing=True, # Set to False if tracing causes issues
)

# --- Structure for 'adk run .' (module.agent.root_agent) ---
# This provides the 'agent.root_agent' structure if 'adk run .'
# specifically looks for that.
class AdkAgentContainer:
    def __init__(self):
        self.root_agent = actual_root_agent

agent_obj = AdkAgentContainer() # Renamed to avoid conflict with 'agent_module'

# Expose both 'app' (for adk web) and 'agent_obj' as 'agent' (for adk run)
# ADK CLI typically looks for an attribute named 'agent' that has 'root_agent'
# or an attribute named 'app'.
__all__ = ['app', 'agent_obj'] # Note: 'adk run' might specifically look for 'agent'

# To be very specific for 'adk run .' which expects module.agent.root_agent
# we can assign agent_obj to a variable named 'agent'
agent = agent_obj
if 'agent' not in __all__:
    __all__.append('agent')
