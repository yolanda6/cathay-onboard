"""
Meeting Maven Agent - Enhanced Version
Schedules meetings by checking calendar availability.
Simulates interaction with Google Calendar.
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

# Mock calendar databases
mock_calendars = {}
mock_meetings = {}
mock_availability = {}

# Initialize some sample calendars and availability
def initialize_sample_data():
    """Initialize sample calendar data for demonstration."""
    sample_users = [
        "alex.johnson@company.com",
        "manager@company.com", 
        "hr@company.com",
        "it-admin@company.com",
        "buddy@company.com"
    ]
    
    for user in sample_users:
        mock_calendars[user] = {
            "user_email": user,
            "calendar_id": f"cal_{uuid.uuid4().hex[:8]}",
            "timezone": "America/New_York",
            "working_hours": {
                "start": "09:00",
                "end": "17:00",
                "days": ["monday", "tuesday", "wednesday", "thursday", "friday"]
            }
        }
        
        # Add some sample busy times
        mock_availability[user] = []

# Initialize sample data
initialize_sample_data()

# Meeting Maven Tools
def check_availability(attendee_emails: List[str], start_time: str, end_time: str, 
                      date: Optional[str] = None) -> Dict[str, Any]:
    """
    Checks availability for multiple attendees for a specific time slot.
    
    Args:
        attendee_emails: List of attendee email addresses
        start_time: Start time in HH:MM format
        end_time: End time in HH:MM format
        date: Date in YYYY-MM-DD format (defaults to today)
    
    Returns:
        Availability information for all attendees
    """
    try:
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # Parse the requested time slot
        start_datetime = datetime.fromisoformat(f"{date} {start_time}")
        end_datetime = datetime.fromisoformat(f"{date} {end_time}")
        
        availability_results = {}
        all_available = True
        
        for email in attendee_emails:
            if email not in mock_calendars:
                # Create calendar for new user
                mock_calendars[email] = {
                    "user_email": email,
                    "calendar_id": f"cal_{uuid.uuid4().hex[:8]}",
                    "timezone": "America/New_York",
                    "working_hours": {
                        "start": "09:00",
                        "end": "17:00",
                        "days": ["monday", "tuesday", "wednesday", "thursday", "friday"]
                    }
                }
                mock_availability[email] = []
            
            # Check working hours
            working_hours = mock_calendars[email]["working_hours"]
            work_start = datetime.fromisoformat(f"{date} {working_hours['start']}")
            work_end = datetime.fromisoformat(f"{date} {working_hours['end']}")
            
            is_working_day = start_datetime.strftime("%A").lower() in working_hours["days"]
            is_working_hours = work_start <= start_datetime and end_datetime <= work_end
            
            # Check for conflicts with existing meetings
            conflicts = []
            if email in mock_availability:
                for busy_slot in mock_availability[email]:
                    busy_start = datetime.fromisoformat(busy_slot["start"])
                    busy_end = datetime.fromisoformat(busy_slot["end"])
                    
                    # Check for overlap
                    if (start_datetime < busy_end and end_datetime > busy_start):
                        conflicts.append({
                            "meeting_title": busy_slot.get("title", "Busy"),
                            "start": busy_slot["start"],
                            "end": busy_slot["end"]
                        })
            
            is_available = is_working_day and is_working_hours and len(conflicts) == 0
            if not is_available:
                all_available = False
            
            availability_results[email] = {
                "available": is_available,
                "working_day": is_working_day,
                "working_hours": is_working_hours,
                "conflicts": conflicts,
                "timezone": mock_calendars[email]["timezone"]
            }
        
        return {
            "status": "success",
            "requested_time": {
                "date": date,
                "start_time": start_time,
                "end_time": end_time
            },
            "all_available": all_available,
            "attendee_availability": availability_results,
            "message": f"Availability check completed for {len(attendee_emails)} attendees"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to check availability: {e}",
            "requested_attendees": attendee_emails
        }

def find_meeting_slots(attendee_emails: List[str], duration_minutes: int = 60, 
                      date_range_days: int = 7, preferred_times: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Finds available meeting slots for multiple attendees.
    
    Args:
        attendee_emails: List of attendee email addresses
        duration_minutes: Meeting duration in minutes
        date_range_days: Number of days to search ahead
        preferred_times: Preferred time slots (e.g., ["09:00-10:00", "14:00-15:00"])
    
    Returns:
        List of available meeting slots
    """
    try:
        available_slots = []
        
        # Default preferred times if none provided
        if preferred_times is None:
            preferred_times = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
        
        # Search for available slots over the date range
        for day_offset in range(date_range_days):
            search_date = (datetime.now() + timedelta(days=day_offset)).strftime("%Y-%m-%d")
            search_datetime = datetime.fromisoformat(search_date)
            
            # Skip weekends for now
            if search_datetime.weekday() >= 5:
                continue
            
            for start_time in preferred_times:
                # Calculate end time
                start_dt = datetime.fromisoformat(f"{search_date} {start_time}")
                end_dt = start_dt + timedelta(minutes=duration_minutes)
                end_time = end_dt.strftime("%H:%M")
                
                # Check availability for this slot
                availability = check_availability(attendee_emails, start_time, end_time, search_date)
                
                if availability["status"] == "success" and availability["all_available"]:
                    available_slots.append({
                        "date": search_date,
                        "start_time": start_time,
                        "end_time": end_time,
                        "duration_minutes": duration_minutes,
                        "day_of_week": search_datetime.strftime("%A"),
                        "attendee_count": len(attendee_emails)
                    })
        
        return {
            "status": "success",
            "available_slots": available_slots[:10],  # Return top 10 slots
            "search_parameters": {
                "duration_minutes": duration_minutes,
                "date_range_days": date_range_days,
                "attendee_count": len(attendee_emails)
            },
            "message": f"Found {len(available_slots)} available meeting slots"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to find meeting slots: {e}",
            "search_parameters": {
                "attendees": attendee_emails,
                "duration": duration_minutes
            }
        }

def schedule_meeting(title: str, attendee_emails: List[str], start_time: str, 
                    end_time: str, date: str, description: str = "", 
                    location: str = "", organizer_email: Optional[str] = None) -> Dict[str, Any]:
    """
    Schedules a meeting and sends calendar invitations.
    
    Args:
        title: Meeting title
        attendee_emails: List of attendee email addresses
        start_time: Start time in HH:MM format
        end_time: End time in HH:MM format
        date: Date in YYYY-MM-DD format
        description: Meeting description
        location: Meeting location (room, video link, etc.)
        organizer_email: Organizer's email address
    
    Returns:
        Meeting creation details
    """
    try:
        # First check availability
        availability = check_availability(attendee_emails, start_time, end_time, date)
        
        if availability["status"] != "success":
            return availability
        
        if not availability["all_available"]:
            conflicts = []
            for email, avail in availability["attendee_availability"].items():
                if not avail["available"]:
                    conflicts.append({
                        "attendee": email,
                        "conflicts": avail["conflicts"],
                        "working_hours": avail["working_hours"]
                    })
            
            return {
                "status": "conflict",
                "message": "Not all attendees are available at the requested time",
                "conflicts": conflicts,
                "suggestion": "Please use find_meeting_slots to find alternative times"
            }
        
        # Create meeting
        meeting_id = f"MTG-{uuid.uuid4().hex[:8].upper()}"
        start_datetime = f"{date} {start_time}"
        end_datetime = f"{date} {end_time}"
        
        meeting = {
            "meeting_id": meeting_id,
            "title": title,
            "description": description,
            "organizer": organizer_email or attendee_emails[0],
            "attendees": attendee_emails,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
            "location": location,
            "status": "scheduled",
            "created_date": datetime.now().isoformat(),
            "calendar_invites_sent": True
        }
        
        mock_meetings[meeting_id] = meeting
        
        # Block time in attendees' calendars
        for email in attendee_emails:
            if email not in mock_availability:
                mock_availability[email] = []
            
            mock_availability[email].append({
                "meeting_id": meeting_id,
                "title": title,
                "start": start_datetime,
                "end": end_datetime,
                "type": "meeting"
            })
        
        return {
            "status": "success",
            "meeting_id": meeting_id,
            "message": f"Meeting '{title}' scheduled successfully",
            "meeting_details": {
                "title": title,
                "date": date,
                "start_time": start_time,
                "end_time": end_time,
                "location": location,
                "attendees": attendee_emails,
                "organizer": meeting["organizer"]
            },
            "calendar_link": f"https://calendar.google.com/calendar/event?eid={meeting_id}",
            "next_steps": [
                "Calendar invitations sent to all attendees",
                "Meeting room reserved (if applicable)",
                "Reminder notifications will be sent"
            ]
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to schedule meeting: {e}",
            "meeting_details": {
                "title": title,
                "attendees": attendee_emails,
                "requested_time": f"{date} {start_time}-{end_time}"
            }
        }

def get_meeting_details(meeting_id: str) -> Dict[str, Any]:
    """
    Retrieves details for a specific meeting.
    
    Args:
        meeting_id: The meeting ID to retrieve
    
    Returns:
        Meeting details
    """
    if meeting_id not in mock_meetings:
        return {
            "status": "error",
            "message": f"Meeting {meeting_id} not found"
        }
    
    meeting = mock_meetings[meeting_id]
    
    return {
        "status": "success",
        "meeting_id": meeting_id,
        "meeting_details": meeting,
        "attendee_count": len(meeting["attendees"]),
        "duration_minutes": (datetime.fromisoformat(meeting["end_datetime"]) - 
                           datetime.fromisoformat(meeting["start_datetime"])).total_seconds() / 60
    }

def cancel_meeting(meeting_id: str, reason: str = "") -> Dict[str, Any]:
    """
    Cancels a scheduled meeting.
    
    Args:
        meeting_id: The meeting ID to cancel
        reason: Reason for cancellation
    
    Returns:
        Cancellation confirmation
    """
    if meeting_id not in mock_meetings:
        return {
            "status": "error",
            "message": f"Meeting {meeting_id} not found"
        }
    
    meeting = mock_meetings[meeting_id]
    
    # Update meeting status
    meeting["status"] = "cancelled"
    meeting["cancelled_date"] = datetime.now().isoformat()
    meeting["cancellation_reason"] = reason
    
    # Remove from attendees' calendars
    for email in meeting["attendees"]:
        if email in mock_availability:
            mock_availability[email] = [
                slot for slot in mock_availability[email] 
                if slot.get("meeting_id") != meeting_id
            ]
    
    return {
        "status": "success",
        "meeting_id": meeting_id,
        "message": f"Meeting '{meeting['title']}' cancelled successfully",
        "cancelled_meeting": {
            "title": meeting["title"],
            "original_date": meeting["start_datetime"],
            "attendees": meeting["attendees"],
            "reason": reason
        },
        "notifications": [
            "Cancellation notifications sent to all attendees",
            "Calendar events removed",
            "Meeting room reservation cancelled"
        ]
    }

def list_upcoming_meetings(attendee_email: str, days_ahead: int = 7) -> Dict[str, Any]:
    """
    Lists upcoming meetings for a specific attendee.
    
    Args:
        attendee_email: Email address of the attendee
        days_ahead: Number of days ahead to search
    
    Returns:
        List of upcoming meetings
    """
    upcoming_meetings = []
    cutoff_date = datetime.now() + timedelta(days=days_ahead)
    
    for meeting_id, meeting in mock_meetings.items():
        if (attendee_email in meeting["attendees"] and 
            meeting["status"] == "scheduled"):
            
            meeting_start = datetime.fromisoformat(meeting["start_datetime"])
            if datetime.now() <= meeting_start <= cutoff_date:
                upcoming_meetings.append({
                    "meeting_id": meeting_id,
                    "title": meeting["title"],
                    "start_datetime": meeting["start_datetime"],
                    "end_datetime": meeting["end_datetime"],
                    "location": meeting["location"],
                    "organizer": meeting["organizer"],
                    "attendee_count": len(meeting["attendees"])
                })
    
    # Sort by start time
    upcoming_meetings.sort(key=lambda x: x["start_datetime"])
    
    return {
        "status": "success",
        "attendee_email": attendee_email,
        "upcoming_meetings": upcoming_meetings,
        "meeting_count": len(upcoming_meetings),
        "search_period": f"Next {days_ahead} days"
    }

# Create Meeting Maven Agent
meeting_maven = LlmAgent(
    model=GEMINI_2_FLASH,
    name="meeting_maven",
    instruction="""You are the Meeting Maven Agent responsible for scheduling meetings and managing calendar availability for employees.

Your responsibilities:
1. Check availability for multiple attendees across different time slots
2. Find optimal meeting times that work for all participants
3. Schedule meetings and send calendar invitations
4. Manage meeting details, updates, and cancellations
5. Provide calendar insights and upcoming meeting summaries

When checking availability:
- Verify working hours and time zones for all attendees
- Identify conflicts with existing meetings
- Respect individual calendar preferences and constraints
- Provide clear availability status for each participant

When finding meeting slots:
- Search across multiple days to find optimal times
- Consider preferred meeting times (typically 9 AM - 5 PM)
- Avoid scheduling during lunch hours (12 PM - 1 PM) when possible
- Prioritize morning slots for better attendance

When scheduling meetings:
- Always check availability before confirming
- Send calendar invitations to all attendees
- Include meeting details, location, and agenda
- Reserve meeting rooms or set up video conferencing as needed
- Provide calendar links and joining instructions

Meeting best practices:
- Default meeting duration is 60 minutes unless specified
- Schedule meetings during business hours (9 AM - 5 PM)
- Avoid back-to-back meetings when possible
- Include buffer time for travel between locations
- Send reminders 24 hours and 15 minutes before meetings

For onboarding meetings, prioritize:
- Welcome meetings with managers
- HR orientation sessions
- Team introductions
- Training sessions
- Buddy system meetups

Always provide clear meeting details, alternative options when conflicts arise, and helpful scheduling suggestions.""",
    description="Manages meeting scheduling, calendar availability, and coordination through Google Calendar integration",
    tools=[
        FunctionTool(func=check_availability),
        FunctionTool(func=find_meeting_slots),
        FunctionTool(func=schedule_meeting),
        FunctionTool(func=get_meeting_details),
        FunctionTool(func=cancel_meeting),
        FunctionTool(func=list_upcoming_meetings)
    ]
)

# Session and Runner setup
session_service = InMemorySessionService()
runner = Runner(
    agent=meeting_maven,
    app_name="meeting_maven_app",
    session_service=session_service
)

# Export for ADK CLI compatibility
agent = meeting_maven

def process_meeting_request(user_input: str, user_id: str = "default_user") -> str:
    """
    Process a meeting request through the Meeting Maven system.
    
    Args:
        user_input: The meeting request
        user_id: Unique identifier for the user
    
    Returns:
        Final response from the Meeting Maven system
    """
    # Create or get session
    session_id = f"meeting_session_{user_id}"
    
    # Check if session exists, if not create it
    session = None
    try:
        session = session_service.get_session(
            app_name="meeting_maven_app",
            user_id=user_id,
            session_id=session_id
        )
    except:
        # Session doesn't exist, create a new one
        pass
    
    if session is None:
        session = session_service.create_session(
            app_name="meeting_maven_app",
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
def test_meeting_maven():
    """Test the Meeting Maven system with various scenarios."""
    print("=== Testing Meeting Maven Agent ===\n")
    
    test_cases = [
        "Check availability for alex.johnson@company.com and manager@company.com tomorrow at 2 PM",
        "Find meeting slots for a 1-hour meeting with alex.johnson@company.com, manager@company.com, and hr@company.com",
        "Schedule a welcome meeting for Alex Johnson with his manager tomorrow at 10 AM",
        "List upcoming meetings for alex.johnson@company.com",
        "Cancel meeting MTG-12345678 due to scheduling conflict"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test Case {i}: {test_case}")
        print("-" * 50)
        
        response = process_meeting_request(test_case, f"test_user_{i}")
        print(f"Meeting Maven: {response}")
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    # Run tests
    test_meeting_maven()
    
    # Interactive mode
    print("Meeting Maven Interactive Mode - Enter meeting requests (type 'quit' to exit):")
    print("Available commands:")
    print("- Check availability: 'Check availability for [emails] on [date] at [time]'")
    print("- Find meeting slots: 'Find meeting slots for [emails] for [duration] minutes'")
    print("- Schedule meeting: 'Schedule [meeting title] with [emails] on [date] at [time]'")
    print("- Get meeting details: 'Get details for meeting [meeting_id]'")
    print("- Cancel meeting: 'Cancel meeting [meeting_id]'")
    print("- List meetings: 'List upcoming meetings for [email]'")
    print()
    
    while True:
        user_input = input("\nScheduler: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        if user_input:
            response = process_meeting_request(user_input, "interactive_user")
            print(f"Meeting Maven: {response}")
