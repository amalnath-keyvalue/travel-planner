import json
import os

from .state import AgentMemory, ConversationMessage


class MemoryManager:
    def __init__(self, file_path: str = "memory.json"):
        self.file_path = file_path
        self.memory = self._load_memory()

    def _load_memory(self) -> AgentMemory:
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    data = json.load(f)
                    return AgentMemory(**data)
            except:
                pass
        return AgentMemory()

    def _save_memory(self):
        with open(self.file_path, "w") as f:
            json.dump(self.memory.dict(), f, indent=2)

    def add_conversation(self, message: ConversationMessage):
        self.memory.conversation_history.append(message)
        self._save_memory()

    def add_short_term(self, context: str):
        self.memory.short_term.append(context)
        if len(self.memory.short_term) > 10:
            self.memory.short_term.pop(0)
        self._save_memory()

    def update_long_term(self, key: str, value: str):
        self.memory.long_term[key] = value
        self._save_memory()

    def get_context(self) -> str:
        recent = " ".join(self.memory.short_term[-3:])
        return f"Recent context: {recent}"
