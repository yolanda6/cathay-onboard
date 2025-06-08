from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    TextContent,
    Tool,
)

DEFAULT_USER_AGENT_AUTONOMOUS = "ModelContextProtocol/1.0 (Autonomous; +https://github.com/modelcontextprotocol/servers)"
DEFAULT_USER_AGENT_MANUAL = "ModelContextProtocol/1.0 (User-Specified; +https://github.com/modelcontextprotocol/servers)"


async def serve() -> None:
    server = Server("mcp-coffee-shop")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="greeting",
                description="A simple tool that returns a greeting from Barista.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "greeting": {
                            "type": "string",
                            "description": "The greeting to return.",
                        }
                    },
                    "required": ["greeting"],
                },
            ),
            Tool(
                name="list-coffee-bean",
                description="Returns a list of sample coffee beans.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            ),
            Tool(
                name="list-menu",
                description="Returns a sample coffee shop menu with prices.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        print(f"call_tool: {name} {arguments}")

        if name == "greeting":
            return [
                TextContent(
                    type="text",
                    text=f"Barista says: {arguments['greeting']} Welcome to our coffee shop!",
                )
            ]
        elif name == "list-coffee-bean":
            coffee_beans = [
                "Ethiopian Yirgacheffe",
                "Colombian Supremo",
                "Jamaican Blue Mountain",
                "Sumatra Mandheling",
                "Kenyan AA",
                "Costa Rican Tarrazu",
                "Hawaiian Kona",
            ]
            return [
                TextContent(
                    type="text",
                    text="Available Coffee Beans:\n" + "\n".join(coffee_beans),
                )
            ]
        elif name == "list-menu":
            menu = {
                "Espresso": "$3.50",
                "Americano": "$4.00",
                "Cappuccino": "$4.50",
                "Latte": "$4.75",
                "Mocha": "$5.25",
                "Cold Brew": "$5.00",
                "Pour Over": "$5.50",
            }
            menu_text = "Coffee Shop Menu:\n" + "\n".join(
                [f"{item}: {price}" for item, price in menu.items()]
            )
            return [TextContent(type="text", text=menu_text)]

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
