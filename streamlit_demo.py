"""Streamlit demo for the travel planner."""

import streamlit as st

from src import TravelSupervisorGraph


def main():
    """Streamlit demo."""
    st.set_page_config(page_title="Travel Planner Demo", page_icon="✈️", layout="wide")

    st.title("✈️ Multi-Agent Travel Planner")
    st.markdown("**LangGraph Supervisor Pattern Demo for Senior Engineers**")

    # Initialize system
    if "travel_system" not in st.session_state:
        with st.spinner("Initializing multi-agent system..."):
            st.session_state.travel_system = TravelSupervisorGraph()
        st.success("✅ Multi-agent system initialized!")

    # Show system info
    with st.expander("🔧 System Architecture", expanded=False):
        for agent, desc in st.session_state.travel_system.get_agent_info().items():
            st.write(f"**{agent.title()}**: {desc}")

    # Demo buttons
    st.markdown("### 🎯 Quick Demo Queries")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🏖️ Find Beach Destinations", use_container_width=True):
            query = "Find me beautiful beach destinations for vacation"
            st.session_state.demo_query = query

    with col2:
        if st.button("📅 Plan Japan Trip", use_container_width=True):
            query = "Plan a 5-day itinerary for Tokyo with cultural activities"
            st.session_state.demo_query = query

    with col3:
        if st.button("💰 Calculate Budget", use_container_width=True):
            query = "Calculate budget for a week in Bali for 2 people"
            st.session_state.demo_query = query

    # Process demo query
    if "demo_query" in st.session_state:
        st.markdown("### 🤖 Agent Response")

        with st.spinner(f"Processing: {st.session_state.demo_query}"):
            try:
                response = st.session_state.travel_system.chat(
                    st.session_state.demo_query
                )
                st.success("✅ Response received!")
                st.markdown(response)
            except Exception as e:
                st.error(f"❌ Error: {e}")

        # Clear the query
        del st.session_state.demo_query

    # Custom input
    st.markdown("### 💬 Custom Query")
    user_input = st.text_input("Ask anything about travel planning:")

    if user_input:
        with st.spinner("Processing your request..."):
            try:
                response = st.session_state.travel_system.chat(user_input)
                st.markdown("**Response:**")
                st.markdown(response)
            except Exception as e:
                st.error(f"Error: {e}")


if __name__ == "__main__":
    main()
