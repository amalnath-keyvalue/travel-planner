from src.graph import TravelPlannerGraph

studio_graph = TravelPlannerGraph(enable_memory=False).graph


def test_graph():
    """Test the travel planner graph with one query."""
    graph = TravelPlannerGraph()

    query = "What's the weather in London?"
    print(f"Query: {query}")
    print("-" * 50)

    try:
        response = graph.chat(query)
        print("RESPONSE:")
        print(response)
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    test_graph()
