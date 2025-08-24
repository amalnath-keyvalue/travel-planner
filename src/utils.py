from typing import Any


def debug_hook(
    event: Any,
    hook_type: str = "POST",
) -> None:
    print(f"\n🔍 {hook_type}_HOOK:")

    if not isinstance(event, dict) or "messages" not in event:
        print(f"   Event type: {type(event).__name__}")
        print()
        return

    messages = event["messages"]
    print(f"   Messages count: {len(messages)}")

    for i, msg in enumerate(messages):
        msg_name = getattr(msg, "name", None)

        content = msg.content or "(no content)"
        content_preview = content[:100]
        if len(content) > 100:
            content_preview += "..."

        tool_calls = getattr(msg, "tool_calls", None)
        if tool_calls:
            tool_info = f" 🔧 {len(tool_calls)} tool call(s)"
        else:
            tool_info = ""

        if msg_name:
            print(f"   [{i}] {msg_name}: {content_preview}{tool_info}")
        else:
            msg_type = type(msg).__name__
            print(f"   [{i}] {msg_type}: {content_preview}{tool_info}")

        if tool_calls:
            for j, tool_call in enumerate(tool_calls):
                if isinstance(tool_call, dict):
                    if "function" in tool_call:
                        tool_name = tool_call["function"].get("name", "unknown")
                        tool_args = tool_call["function"].get("arguments", "{}")
                    else:
                        tool_name = tool_call.get("name", "unknown")
                        tool_args = tool_call.get("args", "{}")
                else:
                    tool_name = str(tool_call)
                    tool_args = "{}"

                args_preview = str(tool_args)[:80]
                if len(str(tool_args)) > 80:
                    args_preview += "..."
                print(f"      🔧 Tool {j+1}: {tool_name}({args_preview})")

    print()
