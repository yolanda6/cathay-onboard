#!/usr/bin/env python3
"""
Test script to verify Eva agent identification improvements.
"""

import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from eva_orchestrator_agent.agent import process_onboarding_request

def test_agent_identification():
    """Test various ways users might ask about the agent's identity."""
    
    print("🧪 Testing Eva Agent Identification")
    print("=" * 50)
    
    test_cases = [
        "Who are you?",
        "What can you do?",
        "Hello, what is your name?",
        "What services do you provide?",
        "Can you help me with onboarding?",
        "Hi there!",
        "What's your role?",
        "Tell me about yourself"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: '{test_case}'")
        print("-" * 40)
        
        try:
            response = process_onboarding_request(test_case, f"test_user_{i}")
            print(f"✅ Eva Response: {response}")
            
            # Check if Eva properly identifies herself
            eva_mentioned = "eva" in response.lower()
            onboarding_mentioned = "onboarding" in response.lower()
            concierge_mentioned = "concierge" in response.lower()
            
            print(f"📊 Analysis:")
            print(f"   - Mentions 'Eva': {'✅' if eva_mentioned else '❌'}")
            print(f"   - Mentions 'onboarding': {'✅' if onboarding_mentioned else '❌'}")
            print(f"   - Mentions 'concierge': {'✅' if concierge_mentioned else '❌'}")
            
            if eva_mentioned and onboarding_mentioned:
                print(f"   - Overall: ✅ GOOD IDENTIFICATION")
            else:
                print(f"   - Overall: ⚠️  NEEDS IMPROVEMENT")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()

def test_onboarding_workflow():
    """Test a complete onboarding workflow to ensure agent coordination works."""
    
    print("\n🔄 Testing Complete Onboarding Workflow")
    print("=" * 50)
    
    workflow_steps = [
        "Hi Eva! I need to onboard a new employee named Sarah Chen as a Data Scientist in the Analytics department starting next Monday.",
        "What's the status of Sarah's onboarding?",
        "Sarah needs a laptop and data analysis software setup.",
        "Can you schedule a welcome meeting with her manager?",
        "What access permissions does Sarah need for the Analytics team?",
        "Sarah has questions about the company's performance review process."
    ]
    
    for i, step in enumerate(workflow_steps, 1):
        print(f"\n🔄 Step {i}: {step}")
        print("-" * 60)
        
        try:
            response = process_onboarding_request(step, "workflow_test_user")
            print(f"✅ Eva: {response}")
            
            # Check for key workflow indicators
            if i == 1:  # First step - should start onboarding
                if "session" in response.lower() or "started" in response.lower():
                    print("📊 ✅ Onboarding session initiated")
                else:
                    print("📊 ⚠️  Onboarding session may not have started")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()

if __name__ == "__main__":
    print("🚀 Eva Agent Identification & Workflow Test")
    print("=" * 60)
    
    # Test agent identification
    test_agent_identification()
    
    # Test workflow coordination
    test_onboarding_workflow()
    
    print("\n🎉 Testing completed!")
    print("\n💡 Key Improvements Made:")
    print("   1. Changed agent name from 'eva_orchestrator' to 'eva_onboarding_concierge'")
    print("   2. Added explicit identity confirmation section")
    print("   3. Added introduction protocol with standard greeting")
    print("   4. Enhanced routing rules and communication style")
    print("\n🔧 If identification issues persist, consider:")
    print("   1. Adding more explicit self-identification triggers")
    print("   2. Enhancing the introduction protocol")
    print("   3. Adding a dedicated 'introduce_myself' tool")
    print("   4. Reviewing sub-agent naming consistency")
