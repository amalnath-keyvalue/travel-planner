"""Terminal demo showing chat-based approval workflow."""

import time
from datetime import datetime

from src import TravelPlannerGraph


def log_step(step: str, details: str = ""):
    """Log demo steps with timestamps."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {step}")
    if details:
        print(f"           {details}")


def demonstrate_agent_communication():
    """Demonstrate multi-agent communication with chat-based approval."""

    print("🤖 Multi-Agent Travel Planner Demo")
    print("=" * 40)

    log_step("🚀 Initializing", "Creating travel planner graph")
    graph = TravelPlannerGraph(enable_human_loop=True, enable_memory=True)

    scenarios = [
        {
            "query": "Plan a 4-day cultural trip to Kyoto with temples and gardens",
            "expected": "Supervisor handles directly",
        },
        {
            "query": "What's the weather like in Tokyo right now?",
            "expected": "Delegates to search agent",
        },
        {
            "query": "Find hotels in Paris for 3 nights next month",
            "expected": "Delegates to booking agent (no interrupt)",
        },
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📋 Scenario {i}: {scenario['query']}")
        print(f"💭 Expected: {scenario['expected']}")
        print("-" * 40)

        log_step("📨 User Input", f"'{scenario['query']}'")
        log_step("🧠 Supervisor", "Analyzing request")

        start_time = time.time()
        result = graph.chat(scenario["query"], conversation_id=f"demo_{i}")
        end_time = time.time()

        if isinstance(result, dict) and result.get("interrupted"):
            log_step("⏸️ Interrupt", "Workflow paused for approval")
            print(f"\n🔄 Interrupted: {result['message']}")

            log_step("👤 Human", "Sending approval message")
            time.sleep(1)

            # Send approval message - chat will auto-resume
            approval_result = graph.chat("approve", conversation_id=f"demo_{i}")

            log_step("▶️ Resumed", "Workflow continued")
            print("\n🎯 Final Response:")
            print(f"{approval_result}")
        else:
            log_step("✅ Complete", f"({end_time - start_time:.1f}s)")
            print("\n🎯 Response:")
            print(f"{result}")

        print()
        time.sleep(1)

    # Test booking confirmation with chat-based approval
    print("\n📋 Testing booking confirmation with chat approval")
    print("-" * 50)
    log_step("📨 User Input", "'Confirm booking for Hotel Paris, check-in Dec 15'")
    result = graph.chat(
        "Confirm booking for Hotel Paris, check-in Dec 15 for John Doe",
        conversation_id="confirmation_test",
    )

    if isinstance(result, dict) and result.get("interrupted"):
        log_step("⏸️ Interrupt", "Workflow paused")
        print(f"\n🔄 Interrupted: {result['message']}")

        log_step("👤 Human", "Sending rejection message")
        reject_result = graph.chat("reject", conversation_id="confirmation_test")

        log_step("❌ Rejected", "Workflow stopped")
        print(f"\n🚫 Response: {reject_result}")
    else:
        print(f"\n🎯 Response: {result}")

    print("\n✅ Demo complete")


if __name__ == "__main__":
    demonstrate_agent_communication()
