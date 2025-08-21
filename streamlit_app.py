import streamlit as st
from dotenv import load_dotenv

from src import ExecutionStatus, LangGraphTravelPlanner, MessageRole

load_dotenv()

st.set_page_config(page_title="AI Travel Planner", page_icon="✈️", layout="wide")


def main():
    st.title("✈️ AI Travel Planner")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        if message["role"] == MessageRole.USER:
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**AI:** {message['content']}")

            if message.get("thinking_process"):
                with st.expander("🧠 Thinking Process"):
                    for step in message["thinking_process"]:
                        status = (
                            "✅"
                            if step.status == ExecutionStatus.SUCCESS
                            else "❌" if step.status == ExecutionStatus.ERROR else "ℹ️"
                        )
                        st.markdown(
                            f"{status} **{step.step.replace('_', ' ').title()}**"
                        )
                        st.markdown(f"*{step.description}*")
                        if step.reasoning:
                            st.info(f"Reasoning: {step.reasoning}")
                        if step.output:
                            st.code(step.output)
                        st.divider()

    query = st.text_area(
        "Ask about your trip:",
        height=100,
        placeholder="e.g., Find hotels in Paris, plan Bali trip...",
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔍 Find Destinations"):
            st.session_state.quick_query = "Search for beach destinations"
            st.rerun()
    with col2:
        if st.button("📅 Plan Itinerary"):
            st.session_state.quick_query = "Create 5-day Tokyo itinerary"
            st.rerun()

    if st.button("Send", type="primary") and query.strip():
        st.session_state.messages.append({"role": MessageRole.USER, "content": query})

        with st.spinner("Thinking..."):
            planner = LangGraphTravelPlanner()
            result = planner.process_request(query)

            st.session_state.messages.append(
                {
                    "role": MessageRole.ASSISTANT,
                    "content": result.final_result,
                    "thinking_process": result.execution_steps,
                }
            )
            st.rerun()


if __name__ == "__main__":
    main()
