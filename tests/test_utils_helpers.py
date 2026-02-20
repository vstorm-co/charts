"""Tests for utils/helpers module."""

import json
from unittest.mock import Mock

from pydantic_ai import AgentRunResult

from charts.utils.helpers import _get_metadata_from_result, get_config_data, get_ui_component


class TestGetMetadataFromResult:
    """Tests for _get_metadata_from_result helper function."""

    def test_extract_metadata_from_message_parts(self):
        """Test extracting metadata from message parts."""
        # Create a mock result with metadata in the message parts
        messages = [
            {
                "role": "assistant",
                "parts": [
                    {
                        "type": "tool-call",
                        "tool_name": "create_chart",
                        "tool_arguments": {},
                    },
                    {
                        "type": "tool-result",
                        "tool_name": "create_chart",
                        "result": {"data": "test"},
                        "metadata": {
                            "ui_component": "<div>Test Component</div>",
                            "config": {"theme": "dark"},
                        },
                    },
                ],
            }
        ]

        # Create a mock AgentRunResult
        mock_result = Mock(spec=AgentRunResult)
        mock_result.all_messages_json.return_value = json.dumps(messages)
        metadata = _get_metadata_from_result(mock_result)

        assert metadata == {
            "ui_component": "<div>Test Component</div>",
            "config": {"theme": "dark"},
        }

    def test_returns_first_metadata_from_last_message_when_multiple_messages(self):
        """Test that metadata from the first part of the last message is returned."""
        messages = [
            {
                "role": "assistant",
                "parts": [{"type": "tool-call", "metadata": {"first_msg": "metadata"}}],
            },
            {
                "role": "assistant",
                "parts": [
                    {"type": "tool-call", "metadata": {"second_msg": "metadata"}},
                    {"type": "tool-result", "metadata": {"from_last_message": "data"}},
                ],
            },
        ]

        mock_result = Mock(spec=AgentRunResult)
        mock_result.all_messages_json.return_value = json.dumps(messages)

        metadata = _get_metadata_from_result(mock_result)

        # Because messages are reversed, the last message (index 1) is processed first.
        # Within that message, parts are iterated in order, so the first part's metadata
        # (tool-call with second_msg) is returned.
        assert metadata == {"second_msg": "metadata"}

    def test_returns_metadata_from_last_message_single_part(self):
        """Test that metadata from last message is found when it has a single part."""
        messages = [
            {
                "role": "assistant",
                "parts": [{"type": "tool-call", "metadata": {"first": "metadata"}}],
            },
            {
                "role": "assistant",
                "parts": [{"type": "tool-result", "metadata": {"last": "metadata"}}],
            },
        ]

        mock_result = Mock(spec=AgentRunResult)
        mock_result.all_messages_json.return_value = json.dumps(messages)

        metadata = _get_metadata_from_result(mock_result)

        # With reversed iteration, the last message (index 1) is processed first,
        # so its metadata should be returned.
        assert metadata == {"last": "metadata"}

    def test_returns_empty_dict_when_no_metadata(self):
        """Test returns empty dict when no metadata in messages."""
        messages = [
            {
                "role": "assistant",
                "parts": [{"type": "tool-call", "tool_name": "test"}],
            }
        ]

        mock_result = Mock(spec=AgentRunResult)
        mock_result.all_messages_json.return_value = json.dumps(messages)
        metadata = _get_metadata_from_result(mock_result)

        assert metadata == {}

    def test_returns_empty_dict_when_invalid_json(self):
        """Test returns empty dict when JSON is invalid."""
        mock_result = Mock(spec=AgentRunResult)
        mock_result.all_messages_json.return_value = "invalid json"

        metadata = _get_metadata_from_result(mock_result)

        assert metadata == {}

    def test_returns_empty_dict_when_exception_occurs(self):
        """Test returns empty dict when an exception occurs."""
        mock_result = Mock(spec=AgentRunResult)
        mock_result.all_messages_json.side_effect = Exception("Test error")
        metadata = _get_metadata_from_result(mock_result)

        assert metadata == {}

    def test_returns_empty_dict_when_parts_missing(self):
        """Test returns empty dict when parts key is missing."""
        messages = [{"role": "assistant"}]

        mock_result = Mock(spec=AgentRunResult)
        mock_result.all_messages_json.return_value = json.dumps(messages)
        metadata = _get_metadata_from_result(mock_result)

        assert metadata == {}

    def test_returns_empty_dict_when_message_has_no_parts(self):
        """Test returns empty dict when message has no parts key."""
        messages = [{"role": "assistant", "content": "test"}]

        mock_result = Mock(spec=AgentRunResult)
        mock_result.all_messages_json.return_value = json.dumps(messages)
        metadata = _get_metadata_from_result(mock_result)

        assert metadata == {}


class TestGetUiComponent:
    """Tests for get_ui_component helper function."""

    def test_extract_ui_component(self):
        """Test extracting UI component from metadata."""
        messages = [
            {
                "role": "assistant",
                "parts": [
                    {
                        "type": "tool-result",
                        "result": {"data": "test"},
                        "metadata": {
                            "ui_component": "<div>Chart Component</div>",
                            "config": {},
                        },
                    },
                ],
            }
        ]

        mock_result = Mock(spec=AgentRunResult)
        mock_result.all_messages_json.return_value = json.dumps(messages)

        ui_component = get_ui_component(mock_result)

        assert ui_component == "<div>Chart Component</div>"

    def test_returns_default_when_no_metadata(self):
        """Test returns default message when no metadata."""
        mock_result = Mock(spec=AgentRunResult)
        mock_result.all_messages_json.return_value = json.dumps([])

        ui_component = get_ui_component(mock_result)

        assert ui_component == "No UI component found in metadata."

    def test_returns_default_when_ui_component_missing(self):
        """Test returns default when ui_component key is missing."""
        messages = [
            {
                "role": "assistant",
                "parts": [
                    {"type": "tool-result", "metadata": {"config": {}}},
                ],
            }
        ]

        mock_result = Mock(spec=AgentRunResult)
        mock_result.all_messages_json.return_value = json.dumps(messages)

        ui_component = get_ui_component(mock_result)

        assert ui_component == "No UI component found in metadata."

    def test_returns_empty_string_when_metadata_empty(self):
        """Test returns default when metadata is empty dict."""
        mock_result = Mock(spec=AgentRunResult)
        mock_result.all_messages_json.return_value = json.dumps([])

        ui_component = get_ui_component(mock_result)

        assert ui_component == "No UI component found in metadata."


class TestGetConfigData:
    """Tests for get_config_data helper function."""

    def test_extract_config_data(self):
        """Test extracting config data from metadata."""
        messages = [
            {
                "role": "assistant",
                "parts": [
                    {
                        "type": "tool-result",
                        "result": {"data": "test"},
                        "metadata": {
                            "config": {"theme": "dark", "responsive": True},
                            "ui_component": "<div>Test</div>",
                        },
                    },
                ],
            }
        ]

        mock_result = Mock(spec=AgentRunResult)
        mock_result.all_messages_json.return_value = json.dumps(messages)
        config_data = get_config_data(mock_result)

        assert config_data == {"theme": "dark", "responsive": True}

    def test_returns_default_when_no_metadata(self):
        """Test returns default message when no metadata."""
        mock_result = Mock(spec=AgentRunResult)
        mock_result.all_messages_json.return_value = json.dumps([])

        config_data = get_config_data(mock_result)
        assert config_data == {}

    def test_returns_default_when_config_missing(self):
        """Test returns default when config key is missing."""
        messages = [
            {
                "role": "assistant",
                "parts": [
                    {"type": "tool-result", "metadata": {"ui_component": "<div/>"}},
                ],
            }
        ]

        mock_result = Mock(spec=AgentRunResult)
        mock_result.all_messages_json.return_value = json.dumps(messages)

        config_data = get_config_data(mock_result)

        assert config_data == {}

    def test_handles_metadata_with_none(self):
        """Test handles None metadata gracefully."""
        messages = [
            {
                "role": "assistant",
                "parts": [{"type": "tool-result", "metadata": None}],
            }
        ]

        mock_result = Mock(spec=AgentRunResult)
        mock_result.all_messages_json.return_value = json.dumps(messages)

        config_data = get_config_data(mock_result)
        assert config_data == {}
