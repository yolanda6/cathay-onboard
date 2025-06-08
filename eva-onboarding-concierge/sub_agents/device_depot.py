"""
Device Depot Agent - IT Equipment Provisioning and Management
Handles equipment requests, inventory checking, and ServiceNow ticket creation.
"""

import random
from typing import Dict, Any, List
from google.genai import types
from adk.llm_agent import LlmAgent
from adk.tools import tool

# Equipment inventory database
EQUIPMENT_INVENTORY = {
    "laptops": {
        "MacBook Pro 14-inch": {"price": 2499, "stock": 15, "specs": "M3 Pro, 18GB RAM, 512GB SSD"},
        "MacBook Pro 16-inch": {"price": 3199, "stock": 8, "specs": "M3 Max, 36GB RAM, 1TB SSD"},
        "Dell XPS 13": {"price": 1299, "stock": 12, "specs": "Intel i7, 16GB RAM, 512GB SSD"},
        "ThinkPad X1 Carbon": {"price": 1599, "stock": 10, "specs": "Intel i7, 16GB RAM, 1TB SSD"},
        "Surface Laptop 5": {"price": 1399, "stock": 6, "specs": "Intel i7, 16GB RAM, 512GB SSD"}
    },
    "monitors": {
        "Dell 27\" 4K Monitor": {"price": 599, "stock": 20, "specs": "4K UHD, USB-C, Height Adjustable"},
        "LG 32\" UltraWide": {"price": 799, "stock": 8, "specs": "QHD, Curved, USB-C Hub"},
        "Apple Studio Display": {"price": 1599, "stock": 5, "specs": "5K Retina, Thunderbolt 3"},
        "Samsung 24\" FHD": {"price": 299, "stock": 25, "specs": "Full HD, HDMI, DisplayPort"}
    },
    "accessories": {
        "Wireless Mouse": {"price": 79, "stock": 50, "specs": "Bluetooth, Ergonomic Design"},
        "Mechanical Keyboard": {"price": 149, "stock": 30, "specs": "Backlit, USB-C, Wireless"},
        "Webcam HD": {"price": 99, "stock": 40, "specs": "1080p, Auto-focus, Privacy Shutter"},
        "Headset": {"price": 199, "stock": 35, "specs": "Noise Cancelling, Wireless, Microphone"},
        "Docking Station": {"price": 249, "stock": 15, "specs": "USB-C, Dual Monitor Support"}
    }
}

@tool
def check_inventory(item_type: str, specifications: str = "") -> str:
    """
    Check equipment inventory availability and pricing.
    
    Args:
        item_type: Type of equipment (laptops, monitors, accessories)
        specifications: Specific requirements or preferences
        
    Returns:
        Available inventory with pricing and specifications
    """
    item_type = item_type.lower()
    
    if item_type not in EQUIPMENT_INVENTORY:
        return f"❌ Unknown equipment type: {item_type}. Available types: {list(EQUIPMENT_INVENTORY.keys())}"
    
    inventory = EQUIPMENT_INVENTORY[item_type]
    
    result = f"""
📦 **Equipment Inventory - {item_type.title()}**

**Available Items:**
"""
    
    for item_name, details in inventory.items():
        availability = "✅ In Stock" if details["stock"] > 0 else "❌ Out of Stock"
        result += f"""
• **{item_name}**
  - Price: ${details['price']:,}
  - Stock: {details['stock']} units
  - Specs: {details['specs']}
  - Status: {availability}
"""
    
    # Add recommendations based on specifications
    if specifications:
        result += f"""
**Recommendations based on "{specifications}":**
"""
        if "developer" in specifications.lower() or "engineering" in specifications.lower():
            result += "• Recommended: MacBook Pro 14-inch + Dell 27\" 4K Monitor + Mechanical Keyboard\n"
        elif "design" in specifications.lower():
            result += "• Recommended: MacBook Pro 16-inch + Apple Studio Display + Wireless Mouse\n"
        elif "standard" in specifications.lower():
            result += "• Recommended: Dell XPS 13 + Samsung 24\" FHD + Wireless Mouse\n"
    
    return result

@tool
def create_equipment_ticket(employee_name: str, equipment_list: str, department: str = "Engineering") -> str:
    """
    Create ServiceNow ticket for equipment request.
    
    Args:
        employee_name: Name of the employee requesting equipment
        equipment_list: List of requested equipment
        department: Department for budget allocation
        
    Returns:
        ServiceNow ticket details and status
    """
    # Generate ticket ID
    ticket_id = f"EQ-{random.randint(100000, 999999)}"
    
    # Parse equipment list and calculate costs
    total_cost = 0
    parsed_items = []
    
    # Simple parsing of common equipment requests
    equipment_lower = equipment_list.lower()
    
    if "macbook pro 14" in equipment_lower or "macbook pro" in equipment_lower:
        parsed_items.append("MacBook Pro 14-inch")
        total_cost += 2499
    if "macbook pro 16" in equipment_lower:
        parsed_items.append("MacBook Pro 16-inch") 
        total_cost += 3199
    if "dell xps" in equipment_lower:
        parsed_items.append("Dell XPS 13")
        total_cost += 1299
    if "monitor" in equipment_lower or "display" in equipment_lower:
        if "4k" in equipment_lower or "dell" in equipment_lower:
            parsed_items.append("Dell 27\" 4K Monitor")
            total_cost += 599
        elif "apple" in equipment_lower or "studio" in equipment_lower:
            parsed_items.append("Apple Studio Display")
            total_cost += 1599
    if "mouse" in equipment_lower:
        parsed_items.append("Wireless Mouse")
        total_cost += 79
    if "keyboard" in equipment_lower:
        parsed_items.append("Mechanical Keyboard")
        total_cost += 149
    if "headset" in equipment_lower or "headphones" in equipment_lower:
        parsed_items.append("Headset")
        total_cost += 199
    if "webcam" in equipment_lower or "camera" in equipment_lower:
        parsed_items.append("Webcam HD")
        total_cost += 99
    if "dock" in equipment_lower:
        parsed_items.append("Docking Station")
        total_cost += 249
    
    # Determine approval requirements
    approval_required = total_cost > 2000
    priority = "High" if total_cost > 5000 else "Medium" if total_cost > 1000 else "Low"
    
    result = f"""
🎫 **ServiceNow Ticket Created**

**Ticket Details:**
• Ticket ID: {ticket_id}
• Type: Equipment Request
• Requestor: {employee_name}
• Department: {department}
• Priority: {priority}
• Status: Submitted

**Requested Equipment:**
"""
    
    for item in parsed_items:
        result += f"• {item}\n"
    
    if not parsed_items:
        result += f"• {equipment_list}\n"
    
    result += f"""
**Cost Summary:**
• Estimated Total: ${total_cost:,}
• Budget Code: {department.upper()}-EQUIP-2025
• Approval Required: {"Yes" if approval_required else "No"}

**Workflow Status:**
1. ✅ Ticket created and submitted
2. 🔄 Pending budget approval ({department} manager)
3. ⏳ Procurement team assignment
4. ⏳ Vendor ordering and delivery
5. ⏳ Asset tagging and deployment

**Expected Timeline:**
• Approval: 1-2 business days
• Procurement: 2-3 business days  
• Delivery: 3-5 business days
• Setup: 1 business day

**Next Steps:**
1. Manager approval notification sent
2. Employee will receive status updates via email
3. Delivery will be coordinated with facilities team
    """
    
    return result

@tool
def calculate_total_cost(equipment_items: List[str]) -> str:
    """
    Calculate total cost and approval requirements for equipment list.
    
    Args:
        equipment_items: List of equipment items to price
        
    Returns:
        Cost breakdown and approval requirements
    """
    total_cost = 0
    cost_breakdown = []
    
    # Flatten inventory for easier lookup
    all_items = {}
    for category, items in EQUIPMENT_INVENTORY.items():
        all_items.update(items)
    
    for item in equipment_items:
        # Find matching item in inventory
        found = False
        for inv_item, details in all_items.items():
            if item.lower() in inv_item.lower() or inv_item.lower() in item.lower():
                cost_breakdown.append(f"• {inv_item}: ${details['price']:,}")
                total_cost += details['price']
                found = True
                break
        
        if not found:
            cost_breakdown.append(f"• {item}: Price TBD (custom quote required)")
    
    # Determine approval levels
    approval_levels = []
    if total_cost > 10000:
        approval_levels.append("VP Approval Required")
    if total_cost > 5000:
        approval_levels.append("Director Approval Required")
    if total_cost > 2000:
        approval_levels.append("Manager Approval Required")
    if total_cost <= 2000:
        approval_levels.append("Auto-Approved")
    
    result = f"""
💰 **Cost Analysis**

**Equipment Breakdown:**
{chr(10).join(cost_breakdown)}

**Total Cost: ${total_cost:,}**

**Approval Requirements:**
{chr(10).join(f"• {level}" for level in approval_levels)}

**Budget Impact:**
• Quarterly Budget Remaining: ${50000 - total_cost:,}
• Percentage of Budget: {(total_cost/50000)*100:.1f}%
• Recommended Action: {"Proceed" if total_cost < 40000 else "Review with Finance"}

**Procurement Timeline:**
• Standard Items: 3-5 business days
• Custom/Special Orders: 7-14 business days
• International Shipping: 14-21 business days
    """
    
    return result

@tool
def track_delivery_status(ticket_id: str) -> str:
    """
    Track equipment delivery and setup progress.
    
    Args:
        ticket_id: ServiceNow ticket ID to track
        
    Returns:
        Current delivery status and tracking information
    """
    # Simulate delivery tracking
    statuses = [
        "Order Placed with Vendor",
        "Items Picked and Packed", 
        "Shipped - In Transit",
        "Out for Delivery",
        "Delivered to Facilities",
        "Ready for Employee Pickup"
    ]
    
    current_status = random.choice(statuses)
    tracking_number = f"TRK{random.randint(100000000, 999999999)}"
    
    result = f"""
🚚 **Delivery Tracking - {ticket_id}**

**Current Status:** {current_status}
**Tracking Number:** {tracking_number}
**Estimated Delivery:** 2-3 business days

**Delivery Timeline:**
✅ Order Approved and Submitted
✅ Vendor Processing
{"✅" if statuses.index(current_status) >= 1 else "⏳"} Items Picked and Packed
{"✅" if statuses.index(current_status) >= 2 else "⏳"} Shipped - In Transit  
{"✅" if statuses.index(current_status) >= 3 else "⏳"} Out for Delivery
{"✅" if statuses.index(current_status) >= 4 else "⏳"} Delivered to Facilities
{"✅" if statuses.index(current_status) >= 5 else "⏳"} Ready for Employee Pickup

**Delivery Details:**
• Carrier: FedEx Express
• Delivery Address: Company Facilities Dock
• Signature Required: Yes
• Special Instructions: Deliver to IT Asset Management

**Next Steps:**
1. Facilities team will receive and log delivery
2. IT will perform asset tagging and initial setup
3. Employee notification for pickup/delivery
4. Setup appointment scheduling if needed

**Contact Information:**
• Facilities: ext. 3333
• IT Asset Management: ext. 4444
• Delivery Questions: facilities@company.com
    """
    
    return result

# Device Depot Agent Configuration
device_depot_agent = LlmAgent(
    agent_id="device_depot",
    model=types.Model(model_name="gemini-2.0-flash-exp"),
    system_instruction="""
You are Device Depot, a specialist agent responsible for IT equipment provisioning and management.
Your expertise includes:

- Managing equipment inventory and availability
- Creating ServiceNow tickets for equipment requests
- Calculating costs and approval requirements
- Tracking delivery and deployment status
- Providing equipment recommendations based on role and department

When handling equipment requests:
1. Check inventory availability and provide current stock levels
2. Create detailed ServiceNow tickets with proper cost calculations
3. Determine appropriate approval workflows based on cost thresholds
4. Provide realistic timelines for procurement and delivery
5. Track orders and provide status updates

Always be thorough in cost calculations and provide clear next steps.
Consider department-specific needs and standard configurations when making recommendations.
Ensure all requests follow proper procurement and approval processes.
    """,
    tools=[
        check_inventory,
        create_equipment_ticket,
        calculate_total_cost,
        track_delivery_status
    ]
)

# Export the agent
__all__ = ["device_depot_agent"]
