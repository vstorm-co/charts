# FastAPI Server

Use Charts through a REST API server.

## Overview

The `api_server_adv_tools.py` provides endpoints for component generation using the `FunctionToolset` and `EngineProtocol` architecture.

## Running the API Server

```bash
cd preview_app
uv run python api_server_adv_tools.py
```

The server will be available at `http://localhost:8000`.

## Endpoints

### GET /api/health

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

### GET /api/status

Get current generation status.

**Response:**
```json
{
  "status": "Rendered Successfully",
  "lastUpdated": "10:30:45"
}
```

### POST /api/generate

Generate a component from a prompt.

**Request:**
```json
{
  "prompt": "Create a bar chart showing monthly sales"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Component generated successfully",
  "lastUpdated": "10:30:45"
}
```

## Using the API

### Python Example

```python
import requests

API_URL = "http://localhost:8000"

# Generate a component
response = requests.post(
    f"{API_URL}/api/generate",
    json={"prompt": "Show me a pie chart of browser usage"}
)
print(response.json())
```

## Component Generation Flow

1. Client sends POST to `/api/generate` with a prompt.
2. The `toolset_agent` analyzes the request.
3. Agent calls tools from the `create_ui_toolset()` (e.g., `create_chart`).
4. The tool uses the `Shadcn` engine to render the component.
5. The generated TSX is extracted from the tool call metadata in the agent's message history.
6. Generated component written to `src/GeneratedComponent.tsx`.
7. Response returned to client.

## Extraction Logic

In `api_server_adv_tools.py`, the UI component is extracted from the message history:

```python
result = await toolset_agent.run(prompt, deps=deps)
messages = json.loads(result.all_messages_json())

for msg in messages:
    if "parts" in msg:
        for part in msg["parts"]:
            if "metadata" in part and "ui_component" in part["metadata"]:
                ui_component = part["metadata"]["ui_component"]
```
