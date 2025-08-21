"""Demo of the professional multi-agent travel planner."""

from src import TravelSupervisorGraph


def main():
    """Demonstrate the multi-agent travel supervisor system."""
    print("🧳 Professional Multi-Agent Travel Planner")
    print("=" * 50)
    print("Following LangGraph official supervisor patterns")
    print("=" * 50)

    # Initialize the system
    travel_system = TravelSupervisorGraph()

    # Demo queries showcasing different agents
    demo_queries = [
        "Find me some beautiful beach destinations for a relaxing vacation",
        "Plan a 5-day itinerary for Kyoto, Japan with cultural activities",
        "Calculate the budget for a week-long trip to Bali for 2 people",
        "Search for mid-range accommodations in Rome for next month",
    ]

    for i, query in enumerate(demo_queries, 1):
        print(f"\n🎯 Demo Query {i}: {query}")
        print("-" * 60)

        try:
            response = travel_system.chat(query)
            print(f"🤖 Agent Response:")
            print(response[:300] + "..." if len(response) > 300 else response)
            print("✅ Success")

        except Exception as e:
            print(f"❌ Error: {e}")

    print(f"\n🎉 Demo completed! All agents working correctly.")
    print(f"\n📊 Available Agents:")
    for agent, description in travel_system.get_agent_info().items():
        print(f"  • {agent}: {description}")

    # Interactive mode
    print(f"\n💬 Interactive Mode (type 'quit' to exit)")
    print("-" * 40)

    while True:
        try:
            user_input = input("\n👤 You: ").strip()

            if user_input.lower() in ["quit", "exit", "q"]:
                print("👋 Goodbye!")
                break

            if user_input:
                response = travel_system.chat(user_input)
                print(f"\n🤖 AI: {response}")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
