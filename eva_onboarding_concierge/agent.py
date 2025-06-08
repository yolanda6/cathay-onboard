"""
Eva Onboarding Concierge - Main Entry Point
Compatible with `adk run` and `adk web` commands.
Following travel-concierge patterns for optimal deployment.
"""

from google.adk.agents import Agent

from eva_onboarding_concierge.eva_orchestrator_agent.agent import eva_orchestrator

# Export the main agent following travel-concierge pattern
root_agent = eva_orchestrator

# For backward compatibility and direct imports
agent = root_agent
__all__ = ['agent', 'root_agent']
