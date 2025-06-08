import random
import os

from google.adk.agents import Agent

from dotenv import load_dotenv

load_dotenv()


def get_hotel_listings():
    """
    Returns a list of simulated hotel listings for development and testing purposes.
    This function provides dummy data that mimics what a real hotel API might return.
    """
    hotels = [
        {
            "id": "h001",
            "name": "Grand Plaza Hotel",
            "location": "Downtown",
            "price_per_night": 199.99,
            "rating": 4.7,
            "amenities": ["Pool", "Spa", "Restaurant", "Free WiFi", "Fitness Center"],
            "available": True,
        },
        {
            "id": "h002",
            "name": "Oceanview Resort",
            "location": "Beachfront",
            "price_per_night": 299.99,
            "rating": 4.9,
            "amenities": [
                "Private Beach",
                "Multiple Pools",
                "Spa",
                "5 Restaurants",
                "Room Service",
            ],
            "available": True,
        },
        {
            "id": "h003",
            "name": "Budget Inn",
            "location": "Airport Area",
            "price_per_night": 89.99,
            "rating": 3.5,
            "amenities": ["Free WiFi", "Breakfast Included", "Shuttle Service"],
            "available": True,
        },
        {
            "id": "h004",
            "name": "Mountain View Lodge",
            "location": "Countryside",
            "price_per_night": 159.99,
            "rating": 4.5,
            "amenities": ["Hiking Trails", "Restaurant", "Fireplace", "Scenic Views"],
            "available": False,
        },
        {
            "id": "h005",
            "name": "City Center Suites",
            "location": "Downtown",
            "price_per_night": 179.99,
            "rating": 4.2,
            "amenities": ["Kitchen", "Workspace", "Gym Access", "Laundry Service"],
            "available": True,
        },
    ]

    return hotels


# Define the Agent
agent = Agent(
    name="hotel_agent",
    description="An agent that provides hotel listing information based on user queries and preferences.",
    model="gemini-2.0-flash",
    instruction=(
        "You are the Hotel Booking Assistant. Your primary task is to help users find suitable hotel accommodations."
        "1. **Identify Intent:** Determine if the user is asking about hotel availability, pricing, amenities, or locations."
        "2. **Determine Requirements:** Identify user preferences such as price range, location, rating, or specific amenities."
        "3. **Call Tool:** You MUST call the `get_hotel_listings` tool to retrieve hotel information. "
        "   Format: get_hotel_listings()"
        "4. **Present Results:** Format the returned hotel information in a clear, organized manner. Highlight key details "
        "   like price, location, rating, and amenities."
        "5. **Filter Results:** If the user has specific requirements, filter the results to show only relevant options."
        "6. **Handle Unavailable Options:** Clearly indicate when hotels are not available for booking."
        "7. **Important:** Never fabricate hotel information. Only present information returned by the tool."
    ),
    tools=[get_hotel_listings],
)
