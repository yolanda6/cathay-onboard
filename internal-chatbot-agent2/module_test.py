#!/usr/bin/env python3
"""
Test script to verify the module structure for ADK.
"""

import sys
import os

def test_module_structure():
    """Test if the module structure is correct for ADK."""
    print("=== Testing Module Structure ===")
    
    try:
        # Try importing the module
        import internal_chatbot_agent
        print("✅ Successfully imported internal_chatbot_agent module")
    except ImportError as e:
        print(f"❌ Failed to import internal_chatbot_agent module: {e}")
        print("This might be because the module name has hyphens instead of underscores.")
        
        # Try importing directly
        try:
            from . import root_agent
            print("✅ Successfully imported root_agent from relative import")
        except (ImportError, ValueError) as e:
            print(f"❌ Failed to import root_agent from relative import: {e}")
            
            # Try importing from agent.py directly
            try:
                from agent import root_agent
                print("✅ Successfully imported root_agent from agent.py")
            except ImportError as e:
                print(f"❌ Failed to import root_agent from agent.py: {e}")
    
    # Check if we're in the correct directory
    print(f"\nCurrent working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    
    # List files in the current directory
    print("\nFiles in current directory:")
    for file in os.listdir('.'):
        print(f"  - {file}")
    
    # Check if __init__.py exists
    if os.path.exists('__init__.py'):
        print("✅ __init__.py exists")
        with open('__init__.py', 'r') as f:
            content = f.read()
            print(f"__init__.py content:\n{content}")
    else:
        print("❌ __init__.py does not exist")
    
    # Check if agent.py exists
    if os.path.exists('agent.py'):
        print("✅ agent.py exists")
    else:
        print("❌ agent.py does not exist")
    
    print("\n=== Module Structure Test Complete ===")

if __name__ == "__main__":
    test_module_structure()
