import json
from typing import Any, cast

from loguru import logger
from pydantic_ai import AgentRunResult


def _get_metadata_from_result(result: AgentRunResult) -> dict[str, Any]:
    """Extract metadata from the agent result.

    Searches through agent message history in reverse chronological order
    to find the most recent tool output containing metadata.

    Args:
        result: The AgentRunResult containing all messages and tool outputs.

    Returns:
        The metadata dictionary if found, otherwise an empty dict.
    """
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
    """Extract the UI component data from agent result metadata.

    Args:
        result: The AgentRunResult containing tool output metadata.

    Returns:
        The UI component code if found in metadata, or an empty string.
    """
    metadata = _get_metadata_from_result(result)
    val = metadata.get("ui_component")
    if isinstance(val, str) and val:
        return val
    return "No UI component found in metadata."


def get_config_data(result: AgentRunResult) -> dict[str, Any]:
    """Extract the configuration data from agent result metadata.

    Args:
        result: The AgentRunResult containing tool output metadata.

    Returns:
        The config dictionary if found in metadata, or an empty dict.
    """
    metadata = _get_metadata_from_result(result)
    val = metadata.get("config")
    if isinstance(val, dict) and val:
        return val
    return {}
