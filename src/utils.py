from langchain_core.messages import AIMessage, ToolMessage
from langgraph.types import interrupt


def debug_hook(
    state: dict,
    hook_type: str = "POST",
) -> None:
    if not isinstance(state, dict) or "messages" not in state:
        print(f"   State type: {type(state).__name__}")
        print()
        return

    print(f"\n🔍 {hook_type}_HOOK:")
    # print(f"\n🔍 State dict: {state}")

    messages = state["messages"]
    print(f"   Messages count: {len(messages)}")

    for i, msg in enumerate(messages):
        msg_name: str | None = getattr(msg, "name", None)
        msg_content: str | None = getattr(msg, "content", None)

        content = msg_content.split("\n")[0] if msg_content else "(no content)"
        content_preview = content[:100]
        if len(content) > 100:
            content_preview += "..."

        tool_calls: list[dict] | None = getattr(msg, "tool_calls", None)
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


def human_in_the_loop(state, tools: list[str]) -> dict:
    """Interrupt execution for risky booking tools requiring human approval."""
    last = state["messages"][-1]

    if isinstance(last, AIMessage) and last.tool_calls:
        for tool_call in last.tool_calls:
            if tool_call["name"] in tools:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                display_name = tool_name.replace("_", " ").title()

                if isinstance(tool_args, dict):
                    args_display = ", ".join(
                        [f"{k}: {v}" for k, v in tool_args.items() if v]
                    )
                else:
                    args_display = str(tool_args)

                decision = interrupt(
                    {
                        "tool_name": tool_name,
                        "tool_input": tool_args,
                        "display_name": display_name,
                        "args_display": args_display,
                        "message": f"Human approval required for {display_name}. "
                        f"Please approve or reject this action.",
                    }
                )

                if isinstance(decision, dict) and decision.get("is_approved"):
                    message_content = "✅ BOOKING CONFIRMED: The user has approved this booking action."

                else:
                    message_content = "❌ BOOKING CANCELLED: The user explicitly rejected this booking action."

                state["messages"].append(
                    ToolMessage(
                        content=message_content,
                        tool_call_id=tool_call["id"],
                        name=tool_call["name"],
                    )
                )
