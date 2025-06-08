"""
Device Depot Agent - Enhanced Version
Handles requests for physical IT hardware.
Simulates interaction with ServiceNow for ticket creation.
"""

import os
import vertexai
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from google.adk.tools.function_tool import FunctionTool
from typing import Dict, Any, List, Optional
import uuid
import json
from datetime import datetime, timedelta
import logging

# Configuration
#PROJECT_ID = "aimc-410006"
PROJECT_ID = "vital-octagon-19612"
LOCATION = "us-central1"
STAGING_BUCKET = "gs://2025-cathay-agentspace"

os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"

# Model configuration
GEMINI_2_FLASH = "gemini-2.0-flash-exp"

# Mock inventory and ticket databases
mock_inventory = {
    "laptops": {
        "macbook_pro_14": {
            "model": "MacBook Pro 14-inch",
            "specs": "M3 Pro, 18GB RAM, 512GB SSD",
            "available": 15,
            "cost": 2499,
            "category": "premium"
        },
        "macbook_air_13": {
            "model": "MacBook Air 13-inch", 
            "specs": "M2, 16GB RAM, 256GB SSD",
            "available": 25,
            "cost": 1299,
            "category": "standard"
        },
        "thinkpad_x1": {
            "model": "ThinkPad X1 Carbon",
            "specs": "Intel i7, 16GB RAM, 512GB SSD",
            "available": 20,
            "cost": 1899,
            "category": "standard"
        },
        "dell_latitude": {
            "model": "Dell Latitude 7420",
            "specs": "Intel i5, 8GB RAM, 256GB SSD",
            "available": 30,
            "cost": 1199,
            "category": "basic"
        }
    },
    "monitors": {
        "dell_27_4k": {
            "model": "Dell UltraSharp 27\" 4K",
            "specs": "27-inch, 4K UHD, USB-C",
            "available": 40,
            "cost": 599,
            "category": "premium"
        },
        "lg_24_fhd": {
            "model": "LG 24\" Full HD",
            "specs": "24-inch, 1080p, HDMI/VGA",
            "available": 60,
            "cost": 199,
            "category": "standard"
        }
    },
    "accessories": {
        "wireless_mouse": {
            "model": "Logitech MX Master 3",
            "specs": "Wireless, ergonomic, multi-device",
            "available": 100,
            "cost": 99,
            "category": "standard"
        },
        "mechanical_keyboard": {
            "model": "Keychron K2 Wireless",
            "specs": "Mechanical, wireless, compact",
            "available": 50,
            "cost": 89,
            "category": "standard"
        },
        "webcam": {
            "model": "Logitech C920 HD Pro",
            "specs": "1080p, auto-focus, stereo audio",
            "available": 75,
            "cost": 79,
            "category": "standard"
        },
        "headset": {
            "model": "Jabra Evolve2 65",
            "specs": "Wireless, noise-canceling, UC certified",
            "available": 80,
            "cost": 229,
            "category": "premium"
        },
        "docking_station": {
            "model": "CalDigit TS3 Plus",
            "specs": "Thunderbolt 3, 15 ports, 87W charging",
            "available": 35,
            "cost": 249,
            "category": "premium"
        }
    },
    "mobile_devices": {
        "iphone_15_pro": {
            "model": "iPhone 15 Pro",
            "specs": "128GB, Titanium, A17 Pro",
            "available": 20,
            "cost": 999,
            "category": "premium"
        },
        "iphone_15": {
            "model": "iPhone 15",
            "specs": "128GB, A16 Bionic",
            "available": 30,
            "cost": 799,
            "category": "standard"
        }
    }
}

mock_tickets = {}
mock_approvals = {}
mock_deployments = {}

# Device Depot Tools
def request_equipment(employee_name: str, employee_email: str, department: str,
                     job_title: str, equipment_list: List[Dict[str, Any]], 
                     business_justification: str = "", manager_email: Optional[str] = None) -> Dict[str, Any]:
    """
    Creates an equipment request ticket in ServiceNow.
    
    Args:
        employee_name: Name of the employee requesting equipment
        employee_email: Email of the employee
        department: Employee's department
        job_title: Employee's job title
        equipment_list: List of equipment items with quantities
        business_justification: Business reason for the request
        manager_email: Manager's email for approval
    
    Returns:
        Equipment request ticket details
    """
    try:
        ticket_id = f"REQ-{uuid.uuid4().hex[:8].upper()}"
        
        # Validate equipment availability and calculate costs
        validated_items = []
        total_cost = 0
        unavailable_items = []
        
        for item in equipment_list:
            item_type = item.get("type", "").lower()
            item_model = item.get("model", "").lower()
            quantity = item.get("quantity", 1)
            
            # Find item in inventory
            found_item = None
            for category, items in mock_inventory.items():
                if item_type in category or category in item_type:
                    for model_key, model_data in items.items():
                        if item_model in model_key or model_key in item_model:
                            found_item = {
                                "category": category,
                                "model_key": model_key,
                                "model_data": model_data,
                                "requested_quantity": quantity
                            }
                            break
                    if found_item:
                        break
            
            if found_item:
                available = found_item["model_data"]["available"]
                if quantity <= available:
                    item_cost = found_item["model_data"]["cost"] * quantity
                    total_cost += item_cost
                    validated_items.append({
                        "category": found_item["category"],
                        "model": found_item["model_data"]["model"],
                        "specs": found_item["model_data"]["specs"],
                        "quantity": quantity,
                        "unit_cost": found_item["model_data"]["cost"],
                        "total_cost": item_cost,
                        "availability": "available"
                    })
                else:
                    unavailable_items.append({
                        "requested": item,
                        "available_quantity": available,
                        "requested_quantity": quantity
                    })
            else:
                unavailable_items.append({
                    "requested": item,
                    "reason": "Item not found in inventory"
                })
        
        # Determine approval requirements based on cost and role
        requires_approval = total_cost > 2000 or any(item["category"] == "premium" for item in validated_items)
        approval_level = "manager" if total_cost < 5000 else "director"
        
        # Create ticket
        ticket = {
            "ticket_id": ticket_id,
            "employee_name": employee_name,
            "employee_email": employee_email,
            "department": department,
            "job_title": job_title,
            "manager_email": manager_email,
            "business_justification": business_justification,
            "requested_items": validated_items,
            "unavailable_items": unavailable_items,
            "total_cost": total_cost,
            "requires_approval": requires_approval,
            "approval_level": approval_level,
            "status": "pending_approval" if requires_approval else "approved",
            "created_date": datetime.now().isoformat(),
            "estimated_delivery": (datetime.now() + timedelta(days=3 if not requires_approval else 5)).isoformat()
        }
        
        mock_tickets[ticket_id] = ticket
        
        # Auto-approve low-cost standard equipment
        if not requires_approval:
            ticket["status"] = "approved"
            ticket["approved_date"] = datetime.now().isoformat()
            ticket["approved_by"] = "auto_approval_system"
        
        return {
            "status": "success",
            "ticket_id": ticket_id,
            "message": f"Equipment request {ticket_id} created successfully",
            "total_cost": total_cost,
            "requires_approval": requires_approval,
            "approval_level": approval_level if requires_approval else None,
            "validated_items": validated_items,
            "unavailable_items": unavailable_items,
            "estimated_delivery": ticket["estimated_delivery"],
            "next_steps": [
                f"{'Awaiting approval from ' + approval_level if requires_approval else 'Request auto-approved'}",
                "Equipment will be prepared for deployment",
                "Delivery notification will be sent"
            ]
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to create equipment request: {e}",
            "employee_details": {
                "name": employee_name,
                "email": employee_email,
                "department": department
            }
        }

def check_ticket_status(ticket_id: str) -> Dict[str, Any]:
    """
    Checks the status of an equipment request ticket.
    
    Args:
        ticket_id: The ticket ID to check
    
    Returns:
        Current ticket status and details
    """
    if ticket_id not in mock_tickets:
        return {
            "status": "error",
            "message": f"Ticket {ticket_id} not found"
        }
    
    ticket = mock_tickets[ticket_id]
    
    # Mock approval process for demo
    if ticket["status"] == "pending_approval":
        # Auto-approve after some time for demo
        ticket["status"] = "approved"
        ticket["approved_date"] = datetime.now().isoformat()
        ticket["approved_by"] = ticket.get("manager_email", "manager@company.com")
    
    return {
        "status": "success",
        "ticket_id": ticket_id,
        "current_status": ticket["status"],
        "employee_name": ticket["employee_name"],
        "total_cost": ticket["total_cost"],
        "approved_by": ticket.get("approved_by"),
        "approved_date": ticket.get("approved_date"),
        "estimated_delivery": ticket["estimated_delivery"],
        "requested_items": ticket["requested_items"],
        "message": f"Ticket {ticket_id} status: {ticket['status']}"
    }

def get_available_equipment(category: Optional[str] = None) -> Dict[str, Any]:
    """
    Lists available equipment in inventory.
    
    Args:
        category: Optional category filter (laptops, monitors, accessories, mobile_devices)
    
    Returns:
        Available equipment list
    """
    if category and category.lower() not in mock_inventory:
        return {
            "status": "error",
            "message": f"Category '{category}' not found",
            "available_categories": list(mock_inventory.keys())
        }
    
    equipment_list = []
    categories_to_show = [category.lower()] if category else mock_inventory.keys()
    
    for cat in categories_to_show:
        if cat in mock_inventory:
            for model_key, model_data in mock_inventory[cat].items():
                equipment_list.append({
                    "category": cat,
                    "model": model_data["model"],
                    "specs": model_data["specs"],
                    "available_quantity": model_data["available"],
                    "cost": model_data["cost"],
                    "tier": model_data["category"]
                })
    
    return {
        "status": "success",
        "equipment": equipment_list,
        "total_items": len(equipment_list),
        "categories": list(categories_to_show)
    }

def create_deployment_schedule(ticket_id: str, delivery_date: Optional[str] = None, 
                             delivery_location: str = "Office") -> Dict[str, Any]:
    """
    Creates a deployment schedule for approved equipment.
    
    Args:
        ticket_id: The approved ticket ID
        delivery_date: Preferred delivery date
        delivery_location: Delivery location
    
    Returns:
        Deployment schedule details
    """
    if ticket_id not in mock_tickets:
        return {
            "status": "error",
            "message": f"Ticket {ticket_id} not found"
        }
    
    ticket = mock_tickets[ticket_id]
    
    if ticket["status"] != "approved":
        return {
            "status": "error",
            "message": f"Ticket {ticket_id} is not approved. Current status: {ticket['status']}"
        }
    
    # Parse delivery date or use default
    if delivery_date:
        try:
            delivery_datetime = datetime.fromisoformat(delivery_date)
        except:
            delivery_datetime = datetime.now() + timedelta(days=2)
    else:
        delivery_datetime = datetime.now() + timedelta(days=2)
    
    deployment_id = f"DEP-{uuid.uuid4().hex[:8].upper()}"
    
    deployment = {
        "deployment_id": deployment_id,
        "ticket_id": ticket_id,
        "employee_name": ticket["employee_name"],
        "employee_email": ticket["employee_email"],
        "delivery_date": delivery_datetime.isoformat(),
        "delivery_location": delivery_location,
        "items_to_deploy": ticket["requested_items"],
        "total_cost": ticket["total_cost"],
        "status": "scheduled",
        "created_date": datetime.now().isoformat(),
        "technician_assigned": f"tech_{uuid.uuid4().hex[:4]}@company.com"
    }
    
    mock_deployments[deployment_id] = deployment
    
    # Update ticket status
    ticket["status"] = "deployment_scheduled"
    ticket["deployment_id"] = deployment_id
    
    return {
        "status": "success",
        "deployment_id": deployment_id,
        "message": f"Deployment {deployment_id} scheduled successfully",
        "delivery_date": delivery_datetime.isoformat(),
        "delivery_location": delivery_location,
        "technician_assigned": deployment["technician_assigned"],
        "items_to_deploy": deployment["items_to_deploy"],
        "preparation_steps": [
            "Equipment will be prepared and configured",
            "Software installation and updates",
            "Security configuration and enrollment",
            "Quality assurance testing"
        ]
    }

def track_deployment(deployment_id: str) -> Dict[str, Any]:
    """
    Tracks the status of equipment deployment.
    
    Args:
        deployment_id: The deployment ID to track
    
    Returns:
        Deployment tracking information
    """
    if deployment_id not in mock_deployments:
        return {
            "status": "error",
            "message": f"Deployment {deployment_id} not found"
        }
    
    deployment = mock_deployments[deployment_id]
    
    # Mock deployment progress
    current_time = datetime.now()
    delivery_time = datetime.fromisoformat(deployment["delivery_date"])
    
    if current_time >= delivery_time:
        deployment["status"] = "completed"
        deployment["completed_date"] = current_time.isoformat()
    elif current_time >= delivery_time - timedelta(hours=4):
        deployment["status"] = "in_transit"
    elif current_time >= delivery_time - timedelta(days=1):
        deployment["status"] = "prepared"
    
    return {
        "status": "success",
        "deployment_id": deployment_id,
        "current_status": deployment["status"],
        "employee_name": deployment["employee_name"],
        "delivery_date": deployment["delivery_date"],
        "delivery_location": deployment["delivery_location"],
        "technician_assigned": deployment["technician_assigned"],
        "items_to_deploy": deployment["items_to_deploy"],
        "completed_date": deployment.get("completed_date"),
        "tracking_info": {
            "prepared": deployment["status"] in ["prepared", "in_transit", "completed"],
            "in_transit": deployment["status"] in ["in_transit", "completed"],
            "delivered": deployment["status"] == "completed"
        }
    }

def generate_equipment_report(department: Optional[str] = None, date_range_days: int = 30) -> Dict[str, Any]:
    """
    Generates equipment request and deployment reports.
    
    Args:
        department: Filter by department
        date_range_days: Number of days to include in report
    
    Returns:
        Equipment report data
    """
    cutoff_date = datetime.now() - timedelta(days=date_range_days)
    
    # Filter tickets
    filtered_tickets = []
    total_cost = 0
    
    for ticket_id, ticket in mock_tickets.items():
        ticket_date = datetime.fromisoformat(ticket["created_date"])
        if ticket_date >= cutoff_date:
            if not department or ticket["department"].lower() == department.lower():
                filtered_tickets.append({
                    "ticket_id": ticket_id,
                    "employee_name": ticket["employee_name"],
                    "department": ticket["department"],
                    "total_cost": ticket["total_cost"],
                    "status": ticket["status"],
                    "created_date": ticket["created_date"],
                    "item_count": len(ticket["requested_items"])
                })
                total_cost += ticket["total_cost"]
    
    # Calculate statistics
    status_counts = {}
    department_costs = {}
    
    for ticket in filtered_tickets:
        status = ticket["status"]
        dept = ticket["department"]
        
        status_counts[status] = status_counts.get(status, 0) + 1
        department_costs[dept] = department_costs.get(dept, 0) + ticket["total_cost"]
    
    return {
        "status": "success",
        "report_period": f"Last {date_range_days} days",
        "department_filter": department,
        "summary": {
            "total_requests": len(filtered_tickets),
            "total_cost": total_cost,
            "average_cost": total_cost / len(filtered_tickets) if filtered_tickets else 0
        },
        "status_breakdown": status_counts,
        "department_costs": department_costs,
        "recent_requests": filtered_tickets[:10]  # Show last 10 requests
    }

# Create Device Depot Agent
device_depot = LlmAgent(
    model=GEMINI_2_FLASH,
    name="device_depot",
    instruction="""You are the Device Depot Agent responsible for managing IT equipment requests and deployments for new and existing employees.

Your responsibilities:
1. Process equipment requests and create ServiceNow tickets
2. Check equipment availability and validate requests
3. Handle approval workflows based on cost and equipment type
4. Schedule equipment deployment and delivery
5. Track deployment status and provide updates
6. Generate equipment reports and analytics

When processing equipment requests:
- Validate equipment availability in inventory
- Calculate total costs and determine approval requirements
- Create ServiceNow tickets with proper categorization
- Handle auto-approval for standard, low-cost items
- Route high-value requests through proper approval channels

Equipment categories and approval rules:
- Basic equipment (<$1000): Auto-approved
- Standard equipment ($1000-$2000): Manager approval
- Premium equipment (>$2000): Director approval
- Mobile devices: Always require manager approval

When scheduling deployments:
- Coordinate delivery dates with employee availability
- Assign technicians for setup and configuration
- Ensure proper software installation and security setup
- Provide tracking information and status updates

Available equipment categories:
- Laptops (MacBook Pro/Air, ThinkPad, Dell Latitude)
- Monitors (4K, Full HD, various sizes)
- Accessories (mouse, keyboard, webcam, headset, docking station)
- Mobile devices (iPhone models)

Always provide clear cost breakdowns, delivery timelines, and next steps. Ensure all equipment requests follow company policies and budget guidelines.""",
    description="Manages IT equipment requests, approvals, and deployments through ServiceNow integration",
    tools=[
        FunctionTool(func=request_equipment),
        FunctionTool(func=check_ticket_status),
        FunctionTool(func=get_available_equipment),
        FunctionTool(func=create_deployment_schedule),
        FunctionTool(func=track_deployment),
        FunctionTool(func=generate_equipment_report)
    ]
)

# Session and Runner setup
session_service = InMemorySessionService()
runner = Runner(
    agent=device_depot,
    app_name="device_depot_app",
    session_service=session_service
)

# Export for ADK CLI compatibility
agent = device_depot

def process_equipment_request(user_input: str, user_id: str = "default_user") -> str:
    """
    Process an equipment request through the Device Depot system.
    
    Args:
        user_input: The equipment request
        user_id: Unique identifier for the user
    
    Returns:
        Final response from the Device Depot system
    """
    # Create or get session
    session_id = f"device_session_{user_id}"
    
    # Check if session exists, if not create it
    session = None
    try:
        session = session_service.get_session(
            app_name="device_depot_app",
            user_id=user_id,
            session_id=session_id
        )
    except:
        # Session doesn't exist, create a new one
        pass
    
    if session is None:
        session = session_service.create_session(
            app_name="device_depot_app",
            user_id=user_id,
            session_id=session_id
        )
    
    # Process the request
    content = types.Content(role="user", parts=[types.Part(text=user_input)])
    events = runner.run(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )
    
    final_response = ""
    for event in events:
        if event.is_final_response() and event.content and event.content.parts:
            final_response = event.content.parts[0].text
            break
    
    return final_response

# Test function
def test_device_depot():
    """Test the Device Depot system with various scenarios."""
    print("=== Testing Device Depot Agent ===\n")
    
    test_cases = [
        "I need to request a MacBook Pro and monitor for Alex Johnson in Engineering",
        "What equipment is available for new hires?",
        "Check the status of ticket REQ-12345678",
        "Schedule deployment for an approved equipment request",
        "Generate an equipment report for the Engineering department"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test Case {i}: {test_case}")
        print("-" * 50)
        
        response = process_equipment_request(test_case, f"test_user_{i}")
        print(f"Device Depot: {response}")
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    # Run tests
    test_device_depot()
    
    # Interactive mode
    print("Device Depot Interactive Mode - Enter equipment requests (type 'quit' to exit):")
    print("Available commands:")
    print("- Request equipment: 'Request [equipment] for [employee] in [department]'")
    print("- Check availability: 'What [equipment type] is available?'")
    print("- Check ticket status: 'Check status of ticket [ticket_id]'")
    print("- Schedule deployment: 'Schedule deployment for ticket [ticket_id]'")
    print("- Track deployment: 'Track deployment [deployment_id]'")
    print("- Generate report: 'Generate equipment report for [department]'")
    print()
    
    while True:
        user_input = input("\nIT Admin: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        if user_input:
            response = process_equipment_request(user_input, "interactive_user")
            print(f"Device Depot: {response}")
