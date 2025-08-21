"""Verbose test to see what's happening."""

import os
import logging
from src import TravelSupervisorGraph

# Enable verbose logging
logging.basicConfig(level=logging.INFO)
os.environ["LANGCHAIN_VERBOSE"] = "true"
os.environ["LANGCHAIN_TRACING_V2"] = "false"


def main():
    """Test with verbose output."""
    print("🧳 Verbose Travel Planner Test")
    print("=" * 40)
    
    try:
        print("1. Initializing system...")
        travel_system = TravelSupervisorGraph()
        print("✅ System created")
        
        print("\n2. Testing simple query...")
        query = "Find beach destinations"
        print(f"Query: {query}")
        
        print("\n3. Processing...")
        response = travel_system.chat(query)
        
        print(f"\n4. ✅ SUCCESS!")
        print(f"Response: {response[:200]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
