import json
from typing import Any, cast

from loguru import logger
from pydantic_ai import AgentRunResult


def _get_metadata_from_result(result: AgentRunResult) -> dict[str, Any]:
    """Extract metadata from the agent result."""
    try:
        messages = json.loads(result.all_messages_json())
        for msg in reversed(messages):
            if "parts" in msg:
                for part in msg["parts"]:
                    if "metadata" in part and part["metadata"]:
                        # Ensure the dict matches the return signature
                        return cast(dict[str, Any], part["metadata"])
        return {}
    except Exception as e:
        logger.exception(f"Error extracting metadata: {e}")
        return {}


def get_ui_component(result: AgentRunResult) -> str:
    """Extract the UI component from the agent result metadata."""
    metadata = _get_metadata_from_result(result)
    val = metadata.get("ui_component")
    if isinstance(val, str) and val:
        return val
    return "No UI component found in metadata."


def get_config_data(result: AgentRunResult) -> dict[str, Any]:
    """Extract the UI component from the agent result metadata."""
    metadata = _get_metadata_from_result(result)
    val = metadata.get("config")
    if isinstance(val, dict) and val:
        return val
    return {}
