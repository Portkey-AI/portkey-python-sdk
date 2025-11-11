"""
Test NotGiven serialization functionality.

This test verifies that NotGiven sentinel objects can be properly serialized
to JSON, which is necessary for compatibility with external libraries like
openai-agents that may attempt to serialize client objects for logging/tracing.
"""

import json
import pytest
from portkey_ai._vendor.openai._types import NOT_GIVEN, NotGiven
from portkey_ai.utils.json_utils import (
    PortkeyJSONEncoder,
    enable_notgiven_serialization,
    disable_notgiven_serialization,
)


def test_notgiven_with_custom_encoder():
    """Test that PortkeyJSONEncoder can serialize NotGiven objects."""
    test_obj = {
        "key1": "value1",
        "key2": NOT_GIVEN,
        "key3": 123,
        "nested": {
            "key4": NOT_GIVEN,
            "key5": "value5"
        }
    }
    
    # Should not raise TypeError
    result = json.dumps(test_obj, cls=PortkeyJSONEncoder)
    parsed = json.loads(result)
    
    # NOT_GIVEN should be serialized as None
    assert parsed["key1"] == "value1"
    assert parsed["key2"] is None
    assert parsed["key3"] == 123
    assert parsed["nested"]["key4"] is None
    assert parsed["nested"]["key5"] == "value5"


def test_notgiven_in_list():
    """Test that NotGiven objects in lists are properly serialized."""
    test_list = [1, "test", NOT_GIVEN, {"key": NOT_GIVEN}]
    
    result = json.dumps(test_list, cls=PortkeyJSONEncoder)
    parsed = json.loads(result)
    
    assert parsed[0] == 1
    assert parsed[1] == "test"
    assert parsed[2] is None
    assert parsed[3]["key"] is None


def test_enable_notgiven_serialization():
    """Test that enable_notgiven_serialization allows standard json.dumps to work."""
    # Note: Serialization is now enabled by default when portkey_ai is imported
    # This test verifies it works correctly
    
    # It should work automatically (already enabled by module import)
    result = json.dumps({"key": NOT_GIVEN})
    parsed = json.loads(result)
    assert parsed["key"] is None
    
    # Test with nested structures
    complex_obj = {
        "a": NOT_GIVEN,
        "b": [1, NOT_GIVEN, 3],
        "c": {"nested": NOT_GIVEN}
    }
    result = json.dumps(complex_obj)
    parsed = json.loads(result)
    assert parsed["a"] is None
    assert parsed["b"] == [1, None, 3]
    assert parsed["c"]["nested"] is None
    
    # Test that we can disable and re-enable
    disable_notgiven_serialization()
    with pytest.raises(TypeError, match="not JSON serializable"):
        json.dumps({"key": NOT_GIVEN})
    
    # Re-enable
    enable_notgiven_serialization()
    result = json.dumps({"key": NOT_GIVEN})
    parsed = json.loads(result)
    assert parsed["key"] is None


def test_disable_notgiven_serialization():
    """Test that disable_notgiven_serialization restores original behavior."""
    enable_notgiven_serialization()
    
    # Should work with patch enabled
    json.dumps({"key": NOT_GIVEN})
    
    # Disable the patch
    disable_notgiven_serialization()
    
    # Should fail again
    with pytest.raises(TypeError, match="not JSON serializable"):
        json.dumps({"key": NOT_GIVEN})


def test_notgiven_instance_check():
    """Test that NotGiven instance checking works correctly."""
    assert isinstance(NOT_GIVEN, NotGiven)
    assert not isinstance(None, NotGiven)
    assert not isinstance("NOT_GIVEN", NotGiven)


def test_notgiven_boolean_behavior():
    """Test that NotGiven behaves correctly in boolean contexts."""
    # NotGiven should evaluate to False
    assert not NOT_GIVEN
    assert bool(NOT_GIVEN) is False


def test_notgiven_repr():
    """Test that NotGiven has proper string representation."""
    assert repr(NOT_GIVEN) == "NOT_GIVEN"
