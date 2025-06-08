#!/usr/bin/env python3
"""
Simplified AdkApp test script.
"""

import os
print("Script started. Attempting imports...")

try:
    from agent import root_agent
    print(f"Successfully imported root_agent: {root_agent.name}")
except ImportError as e:
    print(f"Failed to import root_agent from agent.py: {e}")
    print("Ensure you are in the 'internal-chatbot-agent' directory.")
    exit(1)
except Exception as e:
    print(f"An unexpected error occurred during import: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("Attempting to import Vertex AI components...")
try:
    import vertexai
    from vertexai.preview import reasoning_engines
    print("Successfully imported Vertex AI components.")
except ImportError as e:
    print(f"Failed to import Vertex AI components: {e}")
    exit(1)
except Exception as e:
    print(f"An unexpected error occurred during Vertex AI import: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Minimal Vertex AI Init
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "hello-world-418507")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

print(f"Using Project ID: {PROJECT_ID}, Location: {LOCATION} for Vertex AI init.")
try:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    print("Vertex AI initialized minimally.")
except Exception as e:
    print(f"Error initializing Vertex AI (minimal): {e}")
    # Continue if possible, AdkApp might not strictly need it for instantiation

print("Attempting to create AdkApp...")
try:
    app = reasoning_engines.AdkApp(
        agent=root_agent,
        enable_tracing=False, # Keep it simple
    )
    print(f"AdkApp created successfully: {app}")
    print("Test script finished.")
except Exception as e:
    print(f"Error creating AdkApp: {e}")
    import traceback
    traceback.print_exc()
    print("AdkApp creation failed.")
