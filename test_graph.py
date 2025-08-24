from dotenv import load_dotenv

from src.graph import TravelPlannerGraph

load_dotenv()


def test_graph():
    graph = TravelPlannerGraph(enable_memory=False)
    query = "What's the weather in Rome and what are the top attractions to visit?"
    response = graph.chat(query)
    print("RESPONSE:")
    print(response)


if __name__ == "__main__":
    test_graph()
