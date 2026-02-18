# FastAPI Server

Use Charts through a REST API server.

## Overview

The `api_server.py` provides endpoints for component generation via an AI agent.

## Running the API Server

```bash
cd preview_app
uvicorn api_server:app --host 127.0.0.1 --port 8000 --reload
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

# Check health
response = requests.get(f"{API_URL}/api/health")
print(response.json())

# Generate a component
response = requests.post(
    f"{API_URL}/api/generate",
    json={"prompt": "Show me a pie chart of browser usage"}
)
print(response.json())

# Check status
response = requests.get(f"{API_URL}/api/status")
print(response.json())
```

### JavaScript Example

```javascript
const API_URL = 'http://localhost:8000';

// Generate a component
async function generateComponent(prompt) {
    const response = await fetch(`${API_URL}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
    });

    return response.json();
}

generateComponent('Create a line chart of website traffic')
    .then(data => console.log(data));
```

## Component Generation Flow

1. Client sends POST to `/api/generate` with a prompt
2. Agent analyzes the request and gathers necessary data
3. Agent calls appropriate tools (chart, table, card, etc.)
4. Engine renders component to TSX
5. Status updated in `src/status.json`
6. Generated component written to `src/GeneratedComponent.tsx`
7. Response returned with success status

## Frontend Integration

The frontend polls `/api/status` to monitor generation:

```typescript
const [status, setStatus] = useState('Waiting...');

async function pollStatus() {
    const response = await fetch('/api/status');
    const data = await response.json();
    setStatus(data.status);
}

// Poll every 500ms
setInterval(pollStatus, 500);
```
