"""Test the TravelPlannerGraph with button-based approval."""

from src import TravelPlannerGraph

# Initialize graph
graph = TravelPlannerGraph()

# Test booking flow
print("Testing booking flow...")
try:
    # Step 1: Initial booking request
    print("\nStep 1: Initial booking request")
    response = graph.chat(
        "I want to book Park Hotel Tokyo for Dec 15-17. "
        "My name is Test User and I'll pay with credit card."
    )
    print("Response:", response)

    # Step 2: Simulate button click (True = Confirm, False = Cancel)
    print("\nStep 2: Simulating button click (Confirm)")
    response = graph.chat("True")  # This simulates clicking the Confirm button
    print("Response:", response)

except Exception as e:
    print(f"\nError occurred: {type(e).__name__}: {str(e)}")
print("\nTest completed")
