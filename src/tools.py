from langchain_core.tools import tool

from .memory import add_memory, search_memories


@tool
def add_long_term_memory(
    content: str,
    importance: str = "medium",
    tags: str = "",
) -> str:
    """Add information to long-term memory for future reference.

    Args:
        content: The information to be stored in memory
        importance: Priority level of the memory (low, medium, high)
        tags: Comma-separated tags for categorizing the memory

    Returns:
        Confirmation message indicating the content was added to memory

    Example:
        add_long_term_memory("User prefers beach destinations", "high", "preferences,beach")
    """
    print(
        f"Called add_long_term_memory: content={content}, importance={importance}, tags={tags}"
    )

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
    """Search all memory types for relevant information based on a query.

    Args:
        query: Search term to find relevant memories
        limit: Maximum number of memories to return (default: 5)

    Returns:
        Formatted string containing found memories or "No relevant memories found"

    Example:
        search_long_term_memory("beach destinations", 3)
    """
    print(f"Called search_long_term_memory: query={query}, limit={limit}")

    memories = search_memories("demo", query, limit)

    if not memories:
        return "No relevant memories found."

    results = []
    for memory in memories:
        results.append(f"[{memory.memory_type}] - {memory.content}")

    return f"Found {len(memories)} relevant memories: {results}"
