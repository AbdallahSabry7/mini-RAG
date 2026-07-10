from enum import Enum

class LLMEnums(Enum):
    OPENAI = "openai"
    COHERE = "cohere"
    GEMINI = "gemini"

class OpenAIEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class CohereEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "CHATBOT"
    DOCUMENT = "search_document"
    QUERY = "search_query"

class GeminiEnums(Enum):
    SYSTEM = "model"
    USER = "user"

class DocumentTypeEnums(Enum):
    DOCUMENT = "document"
    QUERY = "query"
    RETRIEVAL_DOCUMENT = "RETRIEVAL_DOCUMENT"
    RETRIEVAL_QUERY = "RETRIEVAL_QUERY"