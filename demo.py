"""Terminal demo showing multi-agent communication with interrupts."""

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
    """Demonstrate multi-agent communication with interrupts."""

    print("🤖 Multi-Agent Travel Planner Demo")
    print("=" * 40)

    log_step("🚀 Initializing", "Creating supervisor graph")
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
            "query": "Book a hotel in Paris for 3 nights next month",
            "expected": "Delegates to booking agent with interrupt",
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
            log_step("⏸️ Interrupt", "Workflow paused before booking")
            print(f"\n🔄 Interrupted: {result['message']}")

            log_step("👤 Human", "Approving request")
            time.sleep(1)

            continue_result = graph.approve_and_continue(conversation_id=f"demo_{i}")

            log_step("▶️ Resumed", "Workflow continued")
            print(f"\n🎯 Final Response:")
            print(f"{continue_result}")
        else:
            log_step("✅ Complete", f"({end_time - start_time:.1f}s)")
            print(f"\n🎯 Response:")
            print(f"{result}")

        print()
        time.sleep(1)

    # Test rejection
    print(f"\n📋 Testing rejection")
    print("-" * 20)
    log_step("📨 User Input", "'Reserve a flight to London'")
    result = graph.chat("Reserve a flight to London", conversation_id="rejection_test")

    if isinstance(result, dict) and result.get("interrupted"):
        log_step("⏸️ Interrupt", "Workflow paused")
        log_step("👤 Human", "Rejecting request")

        reject_result = graph.reject_and_stop(conversation_id="rejection_test")

        log_step("❌ Rejected", "Workflow stopped")
        print(f"\n🚫 Response: {reject_result}")

    print("\n✅ Demo complete")


if __name__ == "__main__":
    demonstrate_agent_communication()
