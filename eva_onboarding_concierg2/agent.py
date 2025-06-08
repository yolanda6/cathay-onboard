"""
Eva Onboarding Concierge - Main Entry Point
Compatible with `adk run` and `adk web` commands.
"""

import os
import sys

# Add the current directory to Python path to ensure imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import the Eva orchestrator agent
try:
    from eva_orchestrator_agent.agent import eva_orchestrator
except ImportError:
    # Fallback import path
    from .eva_orchestrator_agent.agent import eva_orchestrator

# Export the main agent for ADK CLI compatibility
agent = eva_orchestrator
root_agent = eva_orchestrator  # ADK CLI expects root_agent attribute

# For backward compatibility and direct imports
__all__ = ['agent', 'root_agent', 'eva_orchestrator']
