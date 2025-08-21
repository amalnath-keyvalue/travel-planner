from src.supervisor import LangGraphTravelPlanner


def main():
    print("🚀 Travel Planner Agent - Simple Demo")
    print("=" * 50)

    planner = LangGraphTravelPlanner()

    demo_queries = [
        "Search for beach destinations",
        "What's the weather in Paris?",
        "Create a 5-day itinerary for Tokyo",
        "Calculate budget for Bali trip",
        "Find cheap accommodation in New York",
        "Confirm my hotel booking",
    ]

    for i, query in enumerate(demo_queries, 1):
        print(f"\n👤 Query {i}: {query}")
        print("-" * 30)

        try:
            result = planner.process_request(query)
            print(f"🤖 Response: {result}")
            print("✅ Query completed successfully")
        except Exception as e:
            print(f"❌ Error: {e}")
            print(f"🛑 Stopping at query {i}. Fix the error and restart the demo.")
            return

    print("\n🎉 All queries completed successfully!")


if __name__ == "__main__":
    main()
