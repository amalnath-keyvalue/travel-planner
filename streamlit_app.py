import streamlit as st
from dotenv import load_dotenv

from src.supervisor import LangGraphTravelPlanner

load_dotenv()

st.set_page_config(page_title="AI Travel Planner", page_icon="✈️", layout="wide")


def main():
    st.title("✈️ AI Travel Planner")

    col1, col2 = st.columns([3, 1])

    with col1:
        if st.button("🔍 Find destinations"):
            st.session_state.query = "Search for beach destinations"
            st.rerun()
        if st.button("📅 Plan itinerary"):
            st.session_state.query = "Create 5-day Tokyo itinerary"
            st.rerun()

    col1, col2 = st.columns([3, 1])

    with col1:
        query = st.text_area(
            "Ask about your trip:",
            value=st.session_state.get("query", ""),
            height=80,
            placeholder="e.g., Find hotels in Paris, plan Bali trip, check weather...",
        )

        if st.button("Send", type="primary"):
            if query.strip():
                process_request(query)

    with col2:
        st.markdown("**Available Agents:**")
        st.markdown("- 🔍 Search")
        st.markdown("- 📅 Plan")
        st.markdown("- 📚 Book")

    if "chat_history" in st.session_state:
        for msg, response in st.session_state.chat_history:
            with st.expander(f"Q: {msg[:30]}..."):
                st.markdown(f"**A:** {response}")


def process_request(query):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    try:
        with st.spinner("Processing..."):
            planner = LangGraphTravelPlanner()
            result = planner.process_request(query)

            st.session_state.chat_history.append((query, result))
            st.success("Done!")
            st.session_state.query = ""

    except Exception as e:
        st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
