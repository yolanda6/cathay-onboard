## MCP Server

Start the server:

```bash
cd mcp-wiki-remote-server/http-sse-mcp-starter
uv sync
uv run server.py
```

Test the server with client:

```bash
uv run -- client.py http://localhost:8000/sse "https://en.wikipedia.org/wiki/Gemini_(chatbot)"
```


## Use MCP Server with ADK


```bash
cd mcp-wiki-remote-server
uv sync
uv run test_agent.py
```
