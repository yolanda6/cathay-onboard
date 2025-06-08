"""
Meeting Maven Agent - Calendar Management and Meeting Coordination
Handles meeting scheduling, calendar availability, and onboarding coordination.
"""

import random
from datetime import datetime, timedelta
from typing import Dict, Any, List
from google.genai import types
from adk.llm_agent import LlmAgent
from adk.tools import tool

# Sample calendar data for demonstration
CALENDAR_DATA = {
    "managers": {
        "John Smith": {"email": "john.smith@company.com", "department": "Engineering"},
        "Sarah Davis": {"email": "sarah.davis@company.com", "department": "Marketing"},
        "Mike Johnson": {"email": "mike.johnson@company.com", "department": "Finance"},
        "Lisa Chen": {"email": "lisa.chen@company.com", "department": "HR"}
    },
    "meeting_rooms": {
        "Conference Room A": {"capacity": 12, "equipment": "Projector, Whiteboard, Video Conf"},
        "Conference Room B": {"capacity": 8, "equipment": "TV Screen, Whiteboard"},
        "Training Room": {"capacity": 20, "equipment": "Projector, Audio System, Flipcharts"},
        "Executive Boardroom": {"capacity": 16, "equipment": "Video Conf, Presentation System"}
    }
}

@tool
def check_availability(participants: str, time_range: str) -> str:
    """
    Check calendar availability for meeting participants.
    
    Args:
        participants: List of participants (names or emails)
        time_range: Preferred time range for the meeting
        
    Returns:
        Availability status and suggested meeting times
    """
    # Parse participants
    participant_list = [p.strip() for p in participants.split(',')]
    
    # Generate sample availability data
    available_slots = []
    busy_slots = []
    
    # Generate some realistic availability
    base_date = datetime.now() + timedelta(days=1)
    for i in range(5):  # Next 5 business days
        date = base_date + timedelta(days=i)
        if date.weekday() < 5:  # Monday to Friday
            # Morning slots
            if random.choice([True, False]):
                available_slots.append(f"{date.strftime('%A, %B %d')} at 9:00 AM - 10:00 AM")
            else:
                busy_slots.append(f"{date.strftime('%A, %B %d')} at 9:00 AM - 10:00 AM")
            
            # Afternoon slots
            if random.choice([True, False]):
                available_slots.append(f"{date.strftime('%A, %B %d')} at 2:00 PM - 3:00 PM")
            else:
                busy_slots.append(f"{date.strftime('%A, %B %d')} at 2:00 PM - 3:00 PM")
    
    result = f"""
📅 **Calendar Availability Check**

**Participants:** {participants}
**Requested Time Range:** {time_range}

**Available Time Slots:**
"""
    
    for slot in available_slots[:3]:  # Show top 3 available slots
        result += f"✅ {slot}\n"
    
    if busy_slots:
        result += f"""
**Conflicting Time Slots:**
"""
        for slot in busy_slots[:2]:  # Show some busy slots
            result += f"❌ {slot} - Conflicts detected\n"
    
    result += f"""
**Recommended Meeting Times:**
1. {available_slots[0] if available_slots else "No immediate availability"}
2. {available_slots[1] if len(available_slots) > 1 else "Check alternative times"}
3. {available_slots[2] if len(available_slots) > 2 else "Consider next week"}

**Meeting Room Suggestions:**
• Conference Room A (12 people) - Available with video conferencing
• Training Room (20 people) - Available with presentation equipment
• Conference Room B (8 people) - Available for smaller groups

**Next Steps:**
1. Confirm preferred time slot with all participants
2. Reserve meeting room based on group size
3. Send calendar invitations with agenda
4. Set up any required equipment or catering

**Scheduling Notes:**
• All participants will receive calendar invitations
• Meeting rooms include standard A/V equipment
• Catering can be arranged with 24-hour notice
• Remote participants can join via video conference
    """
    
    return result

@tool
def schedule_onboarding_meetings(employee_name: str, department: str, manager_name: str = "") -> str:
    """
    Schedule comprehensive onboarding meetings for new employee.
    
    Args:
        employee_name: Name of the new employee
        department: Department the employee is joining
        manager_name: Name of the direct manager (optional)
        
    Returns:
        Complete onboarding meeting schedule
    """
    # Generate meeting schedule
    start_date = datetime.now() + timedelta(days=1)
    meetings = []
    
    # Day 1: Welcome and orientation
    day1 = start_date
    meetings.append({
        "day": 1,
        "date": day1.strftime("%A, %B %d"),
        "time": "9:00 AM - 10:00 AM",
        "title": "Welcome & Company Orientation",
        "attendees": f"{employee_name}, HR Representative, {manager_name or 'Direct Manager'}",
        "location": "Conference Room A",
        "agenda": "Company overview, culture, policies, first-day logistics"
    })
    
    meetings.append({
        "day": 1,
        "date": day1.strftime("%A, %B %d"),
        "time": "10:30 AM - 11:30 AM",
        "title": "IT Setup & Security Briefing",
        "attendees": f"{employee_name}, IT Support, Security Officer",
        "location": "IT Department",
        "agenda": "Equipment setup, account creation, security policies"
    })
    
    meetings.append({
        "day": 1,
        "date": day1.strftime("%A, %B %d"),
        "time": "2:00 PM - 3:00 PM",
        "title": "Department Introduction",
        "attendees": f"{employee_name}, {department} Team, {manager_name or 'Department Manager'}",
        "location": f"{department} Conference Room",
        "agenda": "Team introductions, department overview, current projects"
    })
    
    # Day 2: Role-specific training
    day2 = start_date + timedelta(days=1)
    meetings.append({
        "day": 2,
        "date": day2.strftime("%A, %B %d"),
        "time": "9:00 AM - 11:00 AM",
        "title": "Role-Specific Training",
        "attendees": f"{employee_name}, {manager_name or 'Direct Manager'}, Senior Team Member",
        "location": "Training Room",
        "agenda": "Job responsibilities, tools, processes, initial assignments"
    })
    
    meetings.append({
        "day": 2,
        "date": day2.strftime("%A, %B %d"),
        "time": "2:00 PM - 3:00 PM",
        "title": "Benefits Enrollment",
        "attendees": f"{employee_name}, Benefits Coordinator",
        "location": "HR Office",
        "agenda": "Health insurance, retirement plans, other benefits"
    })
    
    # Week 1: Follow-up meetings
    week1_end = start_date + timedelta(days=4)
    meetings.append({
        "day": 5,
        "date": week1_end.strftime("%A, %B %d"),
        "time": "3:00 PM - 4:00 PM",
        "title": "Week 1 Check-in",
        "attendees": f"{employee_name}, {manager_name or 'Direct Manager'}",
        "location": "Manager's Office",
        "agenda": "First week feedback, questions, adjustments needed"
    })
    
    # 30-day review
    day30 = start_date + timedelta(days=30)
    meetings.append({
        "day": 30,
        "date": day30.strftime("%A, %B %d"),
        "time": "2:00 PM - 3:00 PM",
        "title": "30-Day Review",
        "attendees": f"{employee_name}, {manager_name or 'Direct Manager'}, HR Representative",
        "location": "Conference Room B",
        "agenda": "Performance review, goal setting, feedback session"
    })
    
    result = f"""
📅 **Onboarding Meeting Schedule for {employee_name}**

**Department:** {department}
**Manager:** {manager_name or 'To be assigned'}
**Start Date:** {start_date.strftime('%A, %B %d, %Y')}

**Complete Meeting Schedule:**

"""
    
    for meeting in meetings:
        result += f"""
**Day {meeting['day']} - {meeting['date']}**
• **Time:** {meeting['time']}
• **Meeting:** {meeting['title']}
• **Attendees:** {meeting['attendees']}
• **Location:** {meeting['location']}
• **Agenda:** {meeting['agenda']}

"""
    
    result += f"""
**Additional Scheduled Activities:**

**Week 2:**
• Buddy System Assignment - Paired with experienced team member
• Department Lunch - Informal team building
• Training Modules - Online compliance and skills training

**Month 1:**
• Project Assignment - First real project or task
• Peer Introductions - Meet cross-functional team members
• Goal Setting Session - Establish 90-day objectives

**Ongoing:**
• Weekly 1:1s with manager
• Monthly team meetings
• Quarterly performance check-ins

**Meeting Logistics:**
• All meetings include calendar invitations with dial-in information
• Meeting rooms reserved with appropriate A/V equipment
• Agendas and materials will be shared 24 hours in advance
• Remote participation available for all meetings

**Preparation Required:**
• Employee handbook review before Day 1
• Complete pre-boarding paperwork
• Prepare questions for orientation sessions
• Review department information and team bios

**Contact Information:**
• Meeting Coordination: {manager_name or 'Direct Manager'} - manager@company.com
• HR Support: hr@company.com or ext. 2222
• IT Support: it-helpdesk@company.com or ext. 5555
• Facilities: facilities@company.com or ext. 3333

**Calendar Integration:**
All meetings have been added to company calendar system and invitations will be sent to all participants.
    """
    
    return result

@tool
def create_team_introduction(new_employee: str, team_members: str, department: str) -> str:
    """
    Organize team introduction sessions and social coordination.
    
    Args:
        new_employee: Name of the new employee
        team_members: List of team members to meet
        department: Department for context
        
    Returns:
        Team introduction plan and social coordination details
    """
    # Parse team members
    members = [member.strip() for member in team_members.split(',')]
    
    # Generate introduction schedule
    intro_date = datetime.now() + timedelta(days=2)
    
    result = f"""
👋 **Team Introduction Plan for {new_employee}**

**Department:** {department}
**Introduction Date:** {intro_date.strftime('%A, %B %d, %Y')}

**Team Introduction Session:**
• **Time:** 2:00 PM - 3:30 PM
• **Location:** {department} Conference Room
• **Format:** Informal meet-and-greet with structured introductions

**Team Members to Meet:**
"""
    
    for i, member in enumerate(members, 1):
        role = random.choice(["Senior Developer", "Product Manager", "Designer", "Analyst", "Team Lead"])
        result += f"{i}. **{member}** - {role}\n"
    
    result += f"""

**Introduction Session Agenda:**
• **2:00 - 2:15 PM:** Welcome and overview
• **2:15 - 2:45 PM:** Individual introductions (5 minutes each)
  - Name, role, and responsibilities
  - Current projects and priorities
  - Fun fact or personal interest
• **2:45 - 3:15 PM:** Team dynamics and collaboration
  - How the team works together
  - Communication preferences
  - Meeting schedules and processes
• **3:15 - 3:30 PM:** Q&A and next steps

**Follow-up Activities:**

**Week 1: One-on-One Coffee Chats**
"""
    
    for member in members[:3]:  # Schedule coffee chats with first 3 members
        chat_date = intro_date + timedelta(days=random.randint(1, 5))
        result += f"• **{member}** - {chat_date.strftime('%A, %B %d')} at 10:00 AM (30 minutes)\n"
    
    result += f"""

**Week 2: Team Lunch**
• **Date:** {(intro_date + timedelta(days=7)).strftime('%A, %B %d')}
• **Time:** 12:00 PM - 1:00 PM
• **Location:** Company cafeteria or nearby restaurant
• **Purpose:** Informal team bonding and relationship building

**Ongoing Integration:**
• **Buddy Assignment:** {members[0] if members else 'Senior team member'} assigned as onboarding buddy
• **Project Pairing:** Shadow experienced team members on current projects
• **Team Meetings:** Include in all regular team meetings and standups
• **Social Events:** Invite to team happy hours, birthday celebrations, etc.

**Communication Setup:**
• Add to team Slack channels and distribution lists
• Include in recurring meeting invitations
• Share team contact list and org chart
• Provide access to shared drives and project documentation

**Team Resources:**
• Team handbook and processes documentation
• Project management tools access (Jira, Asana, etc.)
• Code repositories and development environments
• Design tools and shared asset libraries

**Cultural Integration:**
• Share team traditions and inside jokes
• Explain team communication style and preferences
• Introduce team rituals (daily standups, retrospectives, etc.)
• Discuss work-life balance and team norms

**Success Metrics:**
• New employee feels welcomed and included
• Clear understanding of team dynamics and roles
• Established working relationships with key team members
• Comfortable participating in team meetings and discussions

**Feedback Collection:**
• **Week 1:** Quick check-in on introduction experience
• **Week 2:** Feedback on team integration progress
• **Month 1:** Comprehensive review of team onboarding experience

**Contact for Questions:**
• **Team Lead:** teamlead@company.com
• **HR Business Partner:** hr-bp@company.com
• **Onboarding Buddy:** {members[0].lower().replace(' ', '.')}@company.com

**Special Considerations:**
• Remote team members will join via video conference
• Dietary restrictions accommodated for team lunch
• Flexible scheduling for individual coffee chats
• Cultural sensitivity for diverse team backgrounds
    """
    
    return result

@tool
def setup_training_calendar(employee_name: str, training_plan: str, department: str = "Engineering") -> str:
    """
    Schedule required training sessions and learning activities.
    
    Args:
        employee_name: Name of the employee
        training_plan: Type of training plan (basic, advanced, leadership)
        department: Department for role-specific training
        
    Returns:
        Comprehensive training schedule and learning plan
    """
    if training_plan not in ["basic", "advanced", "leadership"]:
        training_plan = "basic"
    
    start_date = datetime.now() + timedelta(days=3)
    
    # Define training modules by plan type
    training_modules = {
        "basic": [
            {"name": "Company Orientation", "duration": "2 hours", "type": "In-person"},
            {"name": "Security Awareness", "duration": "1 hour", "type": "Online"},
            {"name": "Compliance Training", "duration": "1.5 hours", "type": "Online"},
            {"name": "Communication Tools", "duration": "1 hour", "type": "Hands-on"},
            {"name": "Department Overview", "duration": "3 hours", "type": "In-person"}
        ],
        "advanced": [
            {"name": "Leadership Fundamentals", "duration": "4 hours", "type": "Workshop"},
            {"name": "Project Management", "duration": "6 hours", "type": "Workshop"},
            {"name": "Advanced Security", "duration": "2 hours", "type": "Online"},
            {"name": "Industry Best Practices", "duration": "3 hours", "type": "Seminar"},
            {"name": "Mentoring Skills", "duration": "2 hours", "type": "Workshop"}
        ],
        "leadership": [
            {"name": "Executive Leadership", "duration": "8 hours", "type": "Workshop"},
            {"name": "Strategic Planning", "duration": "6 hours", "type": "Workshop"},
            {"name": "Team Management", "duration": "4 hours", "type": "Workshop"},
            {"name": "Financial Management", "duration": "3 hours", "type": "Seminar"},
            {"name": "Change Management", "duration": "4 hours", "type": "Workshop"}
        ]
    }
    
    modules = training_modules[training_plan]
    
    result = f"""
🎓 **Training Calendar for {employee_name}**

**Training Plan:** {training_plan.title()}
**Department:** {department}
**Start Date:** {start_date.strftime('%A, %B %d, %Y')}

**Training Schedule:**

"""
    
    current_date = start_date
    for i, module in enumerate(modules, 1):
        # Schedule training sessions across different days
        if module["type"] == "Online":
            time_slot = "Self-paced (complete within 1 week)"
            location = "Online Learning Platform"
        else:
            time_slot = f"9:00 AM - {(datetime.strptime('9:00 AM', '%I:%M %p') + timedelta(hours=int(module['duration'].split()[0]))).strftime('%I:%M %p')}"
            location = "Training Room" if module["type"] == "Workshop" else "Conference Room A"
        
        result += f"""
**Week {(i-1)//2 + 1}, Session {i}**
• **Date:** {current_date.strftime('%A, %B %d')}
• **Training:** {module['name']}
• **Duration:** {module['duration']}
• **Type:** {module['type']}
• **Time:** {time_slot}
• **Location:** {location}

"""
        
        # Advance date for next session
        current_date += timedelta(days=2 if module["type"] != "Online" else 1)
    
    result += f"""
**Department-Specific Training:**

**{department} Specialization:**
"""
    
    if department == "Engineering":
        result += """
• **Development Tools Training** - 4 hours
• **Code Review Process** - 2 hours
• **Architecture Overview** - 3 hours
• **Testing Methodologies** - 2 hours
• **Deployment Procedures** - 2 hours
"""
    elif department == "Marketing":
        result += """
• **Marketing Tools Training** - 3 hours
• **Brand Guidelines** - 2 hours
• **Campaign Management** - 4 hours
• **Analytics and Reporting** - 2 hours
• **Content Creation** - 3 hours
"""
    elif department == "Finance":
        result += """
• **Financial Systems Training** - 4 hours
• **Reporting Procedures** - 3 hours
• **Compliance Requirements** - 2 hours
• **Budget Management** - 3 hours
• **Audit Processes** - 2 hours
"""
    else:
        result += """
• **Department Tools Training** - 3 hours
• **Process Overview** - 2 hours
• **Quality Standards** - 2 hours
• **Reporting Requirements** - 2 hours
• **Best Practices** - 2 hours
"""
    
    result += f"""

**Learning Resources:**

**Online Learning Platform:**
• Access to 500+ courses and certifications
• Progress tracking and completion certificates
• Mobile app for learning on-the-go
• Personalized learning paths

**Training Materials:**
• Employee handbook and policy documents
• Department-specific documentation
• Video tutorials and recorded sessions
• Interactive simulations and exercises

**Mentorship Program:**
• Assigned learning mentor for guidance
• Monthly check-ins on progress
• Career development discussions
• Skill assessment and feedback

**Certification Opportunities:**
• Industry-standard certifications supported
• Company-sponsored exam fees
• Study groups and preparation sessions
• Recognition for completed certifications

**Training Schedule Management:**
• All sessions added to company calendar
• Automatic reminders 24 hours before sessions
• Makeup sessions available for missed training
• Flexible scheduling for online modules

**Progress Tracking:**
• **Week 2:** Initial progress review
• **Week 4:** Mid-training assessment
• **Week 6:** Completion review and feedback
• **Month 3:** Skills application evaluation

**Support Resources:**
• **Training Coordinator:** training@company.com or ext. 2215
• **IT Support:** For technical issues with online platforms
• **HR Business Partner:** For training policy questions
• **Department Mentor:** For role-specific guidance

**Completion Requirements:**
• Attend all mandatory in-person sessions
• Complete online modules with 80% or higher scores
• Participate in hands-on exercises and workshops
• Submit training feedback and evaluation forms

**Next Steps:**
1. Review training schedule and confirm availability
2. Access online learning platform and set up profile
3. Download mobile app for convenient learning
4. Connect with assigned mentor for introduction
5. Begin with Company Orientation session

**Training Investment:**
The company invests $2,000 per employee annually in training and development.
Additional specialized training may be approved based on role requirements and career goals.
    """
    
    return result

# Meeting Maven Agent Configuration
meeting_maven_agent = LlmAgent(
    agent_id="meeting_maven",
    model=types.Model(model_name="gemini-2.0-flash-exp"),
    system_instruction="""
You are Meeting Maven, a specialist agent responsible for calendar management and meeting coordination.
Your expertise includes:

- Scheduling meetings and checking calendar availability
- Coordinating comprehensive onboarding meeting schedules
- Organizing team introductions and social integration
- Setting up training calendars and learning schedules
- Managing meeting logistics and room reservations

When handling meeting requests:
1. Check availability for all participants and suggest optimal times
2. Create comprehensive onboarding schedules with appropriate progression
3. Organize meaningful team introductions that foster relationships
4. Design training schedules that balance learning with work responsibilities
5. Provide complete logistics including rooms, equipment, and preparation

Always be thorough in scheduling and consider time zones, work-life balance, and meeting effectiveness.
Ensure all meetings have clear agendas and expected outcomes.
Coordinate with other systems for room bookings and resource allocation.
    """,
    tools=[
        check_availability,
        schedule_onboarding_meetings,
        create_team_introduction,
        setup_training_calendar
    ]
)

# Export the agent
__all__ = ["meeting_maven_agent"]
