from langchain_core.tools import tool

from .memory import add_memory, search_memories


@tool
def add_long_term_memory(
    content: str,
    importance: str = "medium",
    tags: str = "",
) -> str:
    """Add information to long-term memory for future reference."""
    add_memory(
        "demo",
        content,
        "long_term",
        {
            "importance": importance,
            "tags": tags.split(",") if tags else [],
            "source": "supervisor",
        },
    )
    return f"Added to long-term memory: {content}"


@tool
def search_long_term_memory(
    query: str,
    limit: int = 5,
) -> str:
    """Search long-term memory for relevant information."""
    memories = search_memories("demo", query, limit)

    if not memories:
        return "No relevant memories found."

    results = []
    for memory in memories:
        results.append(f"- {memory.content}")

    return f"Found {len(memories)} relevant memories:\n" + "\n".join(results)
