# ./adk_agent_samples/mcp_agent/agent.py
import asyncio
import json
from typing import Any

from dotenv import load_dotenv
from google.adk.agents.llm_agent import LlmAgent
from google.adk.artifacts.in_memory_artifact_service import (
    InMemoryArtifactService,  # Optional
)
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    SseServerParams,
    StdioServerParameters,
)
from google.genai import types

# Load environment variables from .env file in the parent directory
# Place this near the top, before using env vars like API keys
load_dotenv()


def print_friendly_event(event: Any) -> None:
    """
    Print event information in a user-friendly format.

    Args:
        event: The event object from the ADK runner.
    """
    try:
        # Check if the event has content
        if hasattr(event, "content") and event.content:
            # Get the first part if available
            parts = event.content.parts if hasattr(event.content, "parts") else []

            # Handle function calls (when model decides to use a tool)
            if parts and hasattr(parts[0], "function_call") and parts[0].function_call:
                tool_name = parts[0].function_call.name
                args = parts[0].function_call.args
                print(f"🤖 MODEL ACTION: Calling tool '{tool_name}'")
                if args:
                    print(f"   with parameters: {json.dumps(args, indent=2)}")
                return

            # Handle function responses (when a tool returns results)
            if (
                parts
                and hasattr(parts[0], "function_response")
                and parts[0].function_response
            ):
                tool_name = parts[0].function_response.name
                response = parts[0].function_response.response
                print(f"☕ TOOL RESPONSE from '{tool_name}':")

                # Extract and format the result content
                if "result" in response and "content" in response["result"]:
                    for content_item in response["result"]["content"]:
                        if hasattr(content_item, "text") and content_item.text:
                            # Format the text with indentation for readability
                            formatted_text = "\n   ".join(content_item.text.split("\n"))
                            print(f"   {formatted_text}")
                return

            # Handle text content (when model provides a text response)
            if parts and hasattr(parts[0], "text") and parts[0].text:
                print(f"🤖 MODEL RESPONSE: {parts[0].text}")
                return

        # If we couldn't parse the event in a friendly way, fall back to the default representation
        print(f"EVENT (unrecognized format): {event}")
    except Exception as e:
        # If anything goes wrong during parsing, show the original event
        print(f"EVENT (parsing error: {e}): {event}")


# --- Step 1: Import Tools from MCP Server ---
async def get_tools_async():
    print("Attempting to connect to MCP Coffee Shop server...")

    tools, exit_stack = await MCPToolset.from_server(
        # Use StdioServerParameters for local process communication
        connection_params=StdioServerParameters(
            command="python",  # Command to run the server
            args=[
                "/Users/weiyih/work/github/agentic-softwares/google-adk-workshop/mcp-coffee-local-server/src/mcp_coffee_shop"
            ],
        )
    )
    print("MCP Toolset created successfully.")
    # MCP requires maintaining a connection to the local MCP Server.
    # exit_stack manages the cleanup of this connection.
    return tools, exit_stack


# --- Step 2: Agent Definition ---
async def get_agent_async():
    """Creates an ADK Agent equipped with tools from the MCP Server."""
    tools, exit_stack = await get_tools_async()
    print(f"Fetched {len(tools)} tools from MCP server.")

    root_agent = LlmAgent(
        model="gemini-2.0-flash",  # Adjust model name if needed based on availability
        name="coffee_shop_assistant",
        instruction="Help user interact with the coffee shop using available tools.",
        tools=tools,  # Provide the MCP tools to the ADK agent
    )
    return root_agent, exit_stack


# --- Step 3: Main Execution Logic ---
async def async_main():
    session_service = InMemorySessionService()
    # Artifact service might not be needed for this example
    artifacts_service = InMemoryArtifactService()

    session = session_service.create_session(
        state={}, app_name="mcp_coffee_app", user_id="user_fs"
    )

    root_agent, exit_stack = await get_agent_async()

    runner = Runner(
        app_name="mcp_coffee_app",
        agent=root_agent,
        artifact_service=artifacts_service,  # Optional
        session_service=session_service,
    )

    print("Running agent...")
    query_list = [
        "show me the a list of coffee beans",
        "what is the most expensive item in the menu?",
    ]

    for query in query_list:
        print(f"User Query: '{query}'")
        content = types.Content(role="user", parts=[types.Part(text=query)])

        events_async = runner.run_async(
            session_id=session.id, user_id=session.user_id, new_message=content
        )

        async for event in events_async:
            print_friendly_event(event)

    # Crucial Cleanup: Ensure the MCP server process connection is closed.
    print("Closing MCP server connection...")
    await exit_stack.aclose()
    print("Cleanup complete.")


if __name__ == "__main__":
    try:
        asyncio.run(async_main())
    except Exception as e:
        print(f"An error occurred: {e}")
