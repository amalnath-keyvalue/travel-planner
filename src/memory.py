import time
from dataclasses import dataclass
from typing import Any, Dict, List

from langchain.embeddings import init_embeddings
from langgraph.store.memory import InMemoryStore


@dataclass
class MemoryEntry:
    content: str
    memory_type: str
    timestamp: float
    metadata: Dict[str, Any]


class TravelMemoryStore:
    def __init__(self):
        embeddings = init_embeddings(
            "huggingface:sentence-transformers/all-MiniLM-L6-v2"
        )
        self.store = InMemoryStore(
            index={
                "embed": embeddings,
                "dims": 384,
            }
        )

    def store_memory(
        self, session_id: str, content: str, memory_type: str, metadata: Dict[str, Any]
    ) -> None:
        memory_id = f"{memory_type}_{int(time.time())}"

        self.store.put(
            (session_id, "memories"),
            memory_id,
            {"text": content, "metadata": metadata, "type": memory_type},
        )

    def get_memories(self, session_id: str, memory_type: str) -> List[MemoryEntry]:
        try:
            search_results = self.store.search(
                (session_id, "memories"), query=f"type:{memory_type}", limit=100
            )

            result = []
            for item in search_results:
                if item.value.get("type") == memory_type:
                    result.append(
                        MemoryEntry(
                            content=item.value.get("text", ""),
                            memory_type=memory_type,
                            timestamp=time.time(),
                            metadata=item.value.get("metadata", {}),
                        )
                    )
            return result
        except Exception as e:
            print(f"Error getting memories: {e}")
            return []

    def get_all_memories(self, session_id: str) -> Dict[str, List[MemoryEntry]]:
        result = {}
        for mem_type in ["booking", "long_term"]:
            result[mem_type] = self.get_memories(session_id, mem_type)
        return result

    def search_memories(
        self, session_id: str, query: str, limit: int = 5
    ) -> List[MemoryEntry]:
        try:
            search_results = self.store.search(
                (session_id, "memories"), query=query, limit=limit
            )

            result = []
            for item in search_results:
                result.append(
                    MemoryEntry(
                        content=item.value.get("text", ""),
                        memory_type=item.value.get("type", "unknown"),
                        timestamp=time.time(),
                        metadata=item.value.get("metadata", {}),
                    )
                )

            return result
        except Exception as e:
            print(f"Error searching memories: {e}")
            return []


memory_store = TravelMemoryStore()


def add_memory(
    session_id: str, content: str, memory_type: str, metadata: Dict[str, Any]
) -> None:
    memory_store.store_memory(session_id, content, memory_type, metadata)


def get_session_memories(session_id: str) -> Dict[str, List[MemoryEntry]]:
    return memory_store.get_all_memories(session_id)


def search_memories(session_id: str, query: str, limit: int = 5) -> List[MemoryEntry]:
    return memory_store.search_memories(session_id, query, limit)
