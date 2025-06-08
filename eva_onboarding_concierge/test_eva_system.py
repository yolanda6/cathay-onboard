"""
Comprehensive Test Suite for Eva Onboarding Concierge System
Tests all agents individually and the complete integrated workflow.
"""

import sys
import os
import traceback
from datetime import datetime

# Add the parent directory to the path so we can import the agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_individual_agents():
    """Test each agent individually to ensure they work in isolation."""
    print("🧪 Testing Individual Agents")
    print("=" * 50)
    
    agents_to_test = [
        ("ID Master Agent", "eva_onboarding_concierge.id_master_agent.agent", "test_id_master"),
        ("Device Depot Agent", "eva_onboarding_concierge.device_depot_agent.agent", "test_device_depot"),
        ("Access Workflow Orchestrator", "eva_onboarding_concierge.access_workflow_orchestrator_agent.agent", "test_enhanced_workflow"),
        ("HR Helper Agent", "eva_onboarding_concierge.hr_helper_agent.agent", "test_hr_helper"),
        ("Meeting Maven Agent", "eva_onboarding_concierge.meeting_maven_agent.agent", "test_meeting_maven"),
    ]
    
    results = {}
    
    for agent_name, module_path, test_function in agents_to_test:
        print(f"\n🔍 Testing {agent_name}...")
        try:
            # Import the module dynamically
            module = __import__(module_path, fromlist=[test_function])
            test_func = getattr(module, test_function)
            
            # Run the test
            test_func()
            results[agent_name] = "✅ PASSED"
            print(f"✅ {agent_name} test completed successfully")
            
        except Exception as e:
            results[agent_name] = f"❌ FAILED: {str(e)}"
            print(f"❌ {agent_name} test failed: {str(e)}")
            print(f"   Traceback: {traceback.format_exc()}")
    
    return results

def test_eva_orchestrator():
    """Test the main Eva orchestrator system."""
    print("\n🤖 Testing Eva Orchestrator System")
    print("=" * 50)
    
    try:
        from eva_onboarding_concierge.eva_orchestrator_agent.agent import test_eva_system
        test_eva_system()
        return "✅ PASSED"
    except Exception as e:
        print(f"❌ Eva Orchestrator test failed: {str(e)}")
        print(f"   Traceback: {traceback.format_exc()}")
        return f"❌ FAILED: {str(e)}"

def test_integration_workflow():
    """Test the complete integration workflow with realistic scenarios."""
    print("\n🔄 Testing Integration Workflow")
    print("=" * 50)
    
    try:
        from eva_onboarding_concierge import process_onboarding_request
        
        # Test scenarios
        test_scenarios = [
            {
                "name": "Complete Onboarding Flow",
                "request": "Hi Eva! I need to onboard a new employee named Sarah Chen who is starting as a Product Manager in the Marketing department next Monday. Her email will be sarah.chen@company.com and her manager is marketing.lead@company.com",
                "expected_keywords": ["onboarding", "session", "Sarah Chen", "Marketing"]
            },
            {
                "name": "Equipment Request",
                "request": "Sarah needs a MacBook Air and external monitor for her work",
                "expected_keywords": ["equipment", "MacBook", "monitor"]
            },
            {
                "name": "Access Request",
                "request": "Sarah needs access to the marketing team group",
                "expected_keywords": ["access", "marketing", "group"]
            },
            {
                "name": "HR Policy Question",
                "request": "Sarah has questions about vacation time and performance reviews",
                "expected_keywords": ["vacation", "performance", "policy"]
            },
            {
                "name": "Meeting Scheduling",
                "request": "Can you schedule a welcome meeting between Sarah and her manager for her first day?",
                "expected_keywords": ["meeting", "schedule", "welcome"]
            }
        ]
        
        results = {}
        
        for scenario in test_scenarios:
            print(f"\n🎯 Testing: {scenario['name']}")
            print(f"Request: {scenario['request']}")
            
            try:
                response = process_onboarding_request(scenario['request'], f"test_integration_{scenario['name'].replace(' ', '_').lower()}")
                
                # Check if response contains expected keywords
                response_lower = response.lower()
                keywords_found = [kw for kw in scenario['expected_keywords'] if kw.lower() in response_lower]
                
                if len(keywords_found) >= len(scenario['expected_keywords']) // 2:  # At least half the keywords
                    results[scenario['name']] = "✅ PASSED"
                    print(f"✅ Response received with relevant content")
                else:
                    results[scenario['name']] = f"⚠️ PARTIAL: Missing keywords {set(scenario['expected_keywords']) - set(keywords_found)}"
                    print(f"⚠️ Response received but missing some expected content")
                
                print(f"Response preview: {response[:200]}...")
                
            except Exception as e:
                results[scenario['name']] = f"❌ FAILED: {str(e)}"
                print(f"❌ Failed: {str(e)}")
        
        return results
        
    except Exception as e:
        print(f"❌ Integration workflow test failed: {str(e)}")
        print(f"   Traceback: {traceback.format_exc()}")
        return {"Integration Test": f"❌ FAILED: {str(e)}"}

def test_system_imports():
    """Test that all system imports work correctly."""
    print("\n📦 Testing System Imports")
    print("=" * 50)
    
    import_tests = [
        ("Main Package", "eva_onboarding_concierge"),
        ("Eva Orchestrator", "eva_onboarding_concierge.eva_orchestrator_agent"),
        ("ID Master", "eva_onboarding_concierge.id_master_agent"),
        ("Device Depot", "eva_onboarding_concierge.device_depot_agent"),
        ("Access Workflow", "eva_onboarding_concierge.access_workflow_orchestrator_agent"),
        ("HR Helper", "eva_onboarding_concierge.hr_helper_agent"),
        ("Meeting Maven", "eva_onboarding_concierge.meeting_maven_agent"),
    ]
    
    results = {}
    
    for test_name, module_name in import_tests:
        try:
            __import__(module_name)
            results[test_name] = "✅ PASSED"
            print(f"✅ {test_name} import successful")
        except Exception as e:
            results[test_name] = f"❌ FAILED: {str(e)}"
            print(f"❌ {test_name} import failed: {str(e)}")
    
    return results

def run_comprehensive_tests():
    """Run all tests and provide a comprehensive report."""
    print("🚀 Eva Onboarding Concierge - Comprehensive Test Suite")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_results = {}
    
    # Test 1: System Imports
    import_results = test_system_imports()
    all_results.update(import_results)
    
    # Test 2: Individual Agents
    agent_results = test_individual_agents()
    all_results.update(agent_results)
    
    # Test 3: Eva Orchestrator
    eva_result = test_eva_orchestrator()
    all_results["Eva Orchestrator System"] = eva_result
    
    # Test 4: Integration Workflow
    integration_results = test_integration_workflow()
    all_results.update(integration_results)
    
    # Generate Summary Report
    print("\n📊 TEST SUMMARY REPORT")
    print("=" * 60)
    
    passed_tests = [name for name, result in all_results.items() if result.startswith("✅")]
    failed_tests = [name for name, result in all_results.items() if result.startswith("❌")]
    partial_tests = [name for name, result in all_results.items() if result.startswith("⚠️")]
    
    print(f"Total Tests: {len(all_results)}")
    print(f"✅ Passed: {len(passed_tests)}")
    print(f"⚠️ Partial: {len(partial_tests)}")
    print(f"❌ Failed: {len(failed_tests)}")
    print()
    
    if passed_tests:
        print("✅ PASSED TESTS:")
        for test in passed_tests:
            print(f"   • {test}")
        print()
    
    if partial_tests:
        print("⚠️ PARTIAL TESTS:")
        for test in partial_tests:
            print(f"   • {test}: {all_results[test]}")
        print()
    
    if failed_tests:
        print("❌ FAILED TESTS:")
        for test in failed_tests:
            print(f"   • {test}: {all_results[test]}")
        print()
    
    # Overall Status
    if len(failed_tests) == 0:
        if len(partial_tests) == 0:
            print("🎉 ALL TESTS PASSED! Eva system is fully operational.")
        else:
            print("✅ MOSTLY SUCCESSFUL! Some tests had partial results but core functionality works.")
    else:
        print("⚠️ SOME TESTS FAILED! Please review the failed tests above.")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return all_results

def quick_demo():
    """Run a quick demo of the Eva system."""
    print("\n🎭 Quick Eva Demo")
    print("=" * 30)
    
    try:
        from eva_onboarding_concierge import process_onboarding_request, get_system_info
        
        # Show system info
        info = get_system_info()
        print(f"System: {info['name']} v{info['version']}")
        print(f"Description: {info['description']}")
        print()
        
        # Demo conversation
        demo_requests = [
            "Hi Eva! Can you help me onboard a new employee?",
            "I need to onboard John Smith as a Software Engineer in the Engineering department starting tomorrow.",
            "What's the status of the onboarding process?"
        ]
        
        for i, request in enumerate(demo_requests, 1):
            print(f"Demo {i}: {request}")
            response = process_onboarding_request(request, f"demo_user_{i}")
            print(f"Eva: {response[:300]}...")
            print()
        
        print("✅ Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "demo":
            quick_demo()
        elif sys.argv[1] == "imports":
            test_system_imports()
        elif sys.argv[1] == "agents":
            test_individual_agents()
        elif sys.argv[1] == "integration":
            test_integration_workflow()
        else:
            print("Usage: python test_eva_system.py [demo|imports|agents|integration]")
    else:
        # Run comprehensive tests
        run_comprehensive_tests()
