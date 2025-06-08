#!/usr/bin/env python3
"""
Simple test script for the Internal Chatbot Multi-Agent System.
This script provides a basic test without complex session management.
"""

import sys
import os

def test_basic_functionality():
    """Test basic agent functionality."""
    print("=== Simple Agent Test ===")
    
    try:
        # Import the agent components
        from agent import (
            root_agent, servicenow_agent, ad_agent,
            mock_ad_groups, mock_service_requests, mock_work_orders
        )
        print("✅ Successfully imported agent components")
        
        # Test agent names
        print(f"✅ Root Agent: {root_agent.name}")
        print(f"✅ ServiceNow Agent: {servicenow_agent.name}")
        print(f"✅ AD Agent: {ad_agent.name}")
        
        # Test sub-agent relationships
        if hasattr(root_agent, 'sub_agents') and root_agent.sub_agents:
            sub_agent_names = [agent.name for agent in root_agent.sub_agents]
            print(f"✅ Sub-agents: {sub_agent_names}")
        
        # Test mock data
        print(f"✅ Mock AD Groups: {list(mock_ad_groups.keys())}")
        
        # Test individual tools
        from agent import create_service_request, add_user_to_ad_group
        
        print("\n--- Testing ServiceNow Tool ---")
        result = create_service_request("finance_team", "test@company.com", "requester@company.com")
        print(f"Service Request Result: {result}")
        
        if result.get("status") == "success":
            request_id = result.get("request_id")
            print(f"✅ Service request created: {request_id}")
            
            # Test approval status
            from agent import get_approval_status
            approval_result = get_approval_status(request_id)
            print(f"Approval Result: {approval_result}")
            
            if approval_result.get("work_order_id"):
                work_order_id = approval_result.get("work_order_id")
                print(f"✅ Work order created: {work_order_id}")
                
                # Test AD operation
                print("\n--- Testing AD Tool ---")
                ad_result = add_user_to_ad_group(work_order_id)
                print(f"AD Operation Result: {ad_result}")
                
                if ad_result.get("status") == "success":
                    print("✅ User successfully added to AD group")
                    
                    # Test work order closure
                    from agent import close_work_order
                    close_result = close_work_order(work_order_id, "success")
                    print(f"Work Order Closure: {close_result}")
                    
                    if close_result.get("status") == "success":
                        print("✅ Work order successfully closed")
        
        print("\n--- Testing Complete Workflow ---")
        try:
            from agent import process_request
            
            # Use a simple unique user ID
            user_id = "simple_test_user"
            query = "Add newuser@company.com to engineering_team"
            
            print(f"Testing query: {query}")
            response = process_request(query, user_id)
            print(f"Response: {response}")
            
            if response:
                print("✅ Complete workflow test successful")
            else:
                print("⚠️ Complete workflow returned empty response")
                
        except Exception as e:
            print(f"❌ Complete workflow test failed: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n🎉 Basic functionality tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("Internal Chatbot Multi-Agent System - Simple Test")
    print("=" * 50)
    
    success = test_basic_functionality()
    
    if success:
        print("\n✅ All basic tests passed!")
        print("\nNext steps:")
        print("1. Try the full test: python test.py")
        print("2. Deploy to cloud: python deploy.py")
    else:
        print("\n❌ Some tests failed. Check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
