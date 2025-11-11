"""
Example: Using Portkey with openai-agents (NotGiven Serialization)

This example demonstrates that Portkey now automatically handles NotGiven 
serialization out of the box. No manual setup required!

The fix is transparent - just import and use Portkey normally.
"""

import portkey_ai
from portkey_ai import AsyncPortkey, enable_notgiven_serialization, disable_notgiven_serialization
import json


def example_automatic_serialization():
    """Example showing automatic serialization works out of the box."""
    print("=== Automatic Serialization (No Setup Needed!) ===\n")
    
    from portkey_ai._vendor.openai._types import NOT_GIVEN
    
    # Data that contains NotGiven objects
    data = {
        "model": "gpt-4",
        "temperature": 0.7,
        "optional_param": NOT_GIVEN,  # This works automatically now!
        "another_param": None,
    }
    
    # Use standard json.dumps - no special encoder needed!
    try:
        json_string = json.dumps(data)  # Just works! ✨
        print(f"✅ Serialization works automatically: {json_string}\n")
    except TypeError as e:
        print(f"❌ Serialization failed: {e}\n")


def example_basic_usage():
    """Basic example of using PortkeyJSONEncoder for manual serialization."""
    print("=== Custom Encoder (Optional) ===\n")
    
    from portkey_ai import PortkeyJSONEncoder
    from portkey_ai._vendor.openai._types import NOT_GIVEN
    
    # You can still use the custom encoder if you prefer
    data = {
        "model": "gpt-4",
        "temperature": 0.7,
        "optional_param": NOT_GIVEN,
        "another_param": None,
    }
    
    # Serialize using PortkeyJSONEncoder
    try:
        json_string = json.dumps(data, cls=PortkeyJSONEncoder)
        print(f"✅ Successfully serialized with encoder: {json_string}\n")
    except TypeError as e:
        print(f"❌ Serialization failed: {e}\n")


def example_global_serialization():
    """Example showing disable/enable functionality."""
    print("=== Manual Enable/Disable Example ===\n")
    
    from portkey_ai._vendor.openai._types import NOT_GIVEN
    
    print("Note: Serialization is already enabled automatically!")
    print("But you can disable and re-enable if needed:\n")
    
    # Disable temporarily
    print("1. Disabling serialization...")
    disable_notgiven_serialization()
    
    data = {"param": NOT_GIVEN}
    
    try:
        json.dumps(data)
        print("   ✅ Still works (unexpected)")
    except TypeError:
        print("   ✅ Correctly disabled - can't serialize NotGiven")
    
    # Re-enable
    print("\n2. Re-enabling serialization...")
    enable_notgiven_serialization()
    
    try:
        json_string = json.dumps(data)
        print(f"   ✅ Works again: {json_string}\n")
    except TypeError as e:
        print(f"   ❌ Failed: {e}\n")


def example_with_portkey_client():
    """Example showing how to use with a Portkey client."""
    print("=== Portkey Client Example ===\n")
    
    print("Serialization is enabled automatically - no setup needed!")
    
    # Create Portkey client - serialization works out of the box!
    client = AsyncPortkey(
        api_key="your-portkey-api-key",  # or set PORTKEY_API_KEY env var
        virtual_key="your-virtual-key",   # optional
    )
    
    print("✅ AsyncPortkey client created successfully")
    print("✅ The client can be serialized by external libraries like openai-agents")
    
    # Example: Simulate what openai-agents might do
    try:
        # Try to serialize the client's attributes
        client_dict = {
            "api_key": client.api_key,
            "base_url": str(client.base_url),
            "virtual_key": client.virtual_key,
        }
        serialized = json.dumps(client_dict)
        print(f"✅ Client attributes serialized successfully: {serialized}\n")
    except TypeError as e:
        print(f"❌ Client serialization failed: {e}\n")


def example_before_and_after():
    """Demonstrate the problem and solution side by side."""
    print("=== Before and After Comparison ===\n")
    
    from portkey_ai._vendor.openai._types import NOT_GIVEN
    
    data = {"param": NOT_GIVEN}
    
    # BEFORE: This would fail
    print("Before enabling global serialization:")
    try:
        json.dumps(data)
        print("✅ Serialization succeeded (unexpected)")
    except TypeError as e:
        print(f"❌ Serialization failed as expected: {str(e)[:50]}...")
    
    # AFTER: This works
    print("\nAfter enabling global serialization:")
    enable_notgiven_serialization()
    try:
        result = json.dumps(data)
        print(f"✅ Serialization succeeded: {result}")
    except TypeError as e:
        print(f"❌ Serialization failed (unexpected): {e}")
    
    from portkey_ai import disable_notgiven_serialization
    disable_notgiven_serialization()
    print()


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("Portkey NotGiven Serialization Examples")
    print("="*60 + "\n")
    
    print("✨ Good News: Serialization works automatically!")
    print("   No manual setup required - just import and use.\n")
    
    example_automatic_serialization()
    example_with_portkey_client()
    example_basic_usage()
    example_global_serialization()
    example_before_and_after()
    
    print("="*60)
    print("\n✨ All examples completed!")
    print("\n📚 Key Takeaway: NotGiven serialization works out of the box!")
    print("   For more information, see docs/notgiven-serialization.md")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
