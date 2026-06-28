from enum import Enum

class LLMEnums(Enum):
    OPENAI = "openai"
    cohere = "cohere"
    Gemini = "gemini"

class OpenAIEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"