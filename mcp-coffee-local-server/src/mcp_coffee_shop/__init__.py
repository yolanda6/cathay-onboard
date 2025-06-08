from .server import serve


def main():
    """MCP Coffee Shop"""
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(
        description="give a model the ability to run a function"
    )

    _ = parser.parse_args()
    # asyncio.run(serve())

    print("Launching MCP Server exposing ADK tools...")
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        print("\nMCP Server stopped by user.")
    except Exception as e:
        print(f"MCP Server encountered an error: {e}")
    finally:
        print("MCP Server process exiting.")
