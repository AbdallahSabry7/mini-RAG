from .LLMEnums import LLMEnums
from .LLM_providers import Cohere_provider, OPENAI_provider , Gemini_provider


class LLMProviderFactory:
    def __init__(self, config: dict):
        self.config = config
        

    def create_provider(self, provider_name: str):
        if provider_name == LLMEnums.OPENAI.value:
            return OPENAI_provider(
                api_key=self.config.OPENAI_API_KEY,
                api_url=self.config.OPENAI_API_URL,
                default_input_max_tokens=self.config.INPUT_DEFAULT_MAX_TOKENS,
                default_output_max_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE
            )
        elif provider_name == LLMEnums.COHERE.value:
            return Cohere_provider(
                api_key=self.config.COHERE_API_KEY,
                default_input_max_tokens=self.config.INPUT_DEFAULT_MAX_TOKENS,
                default_output_max_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE
            )
        elif provider_name == LLMEnums.GEMINI.value:
            return Gemini_provider(
                api_key=self.config.GEMINI_API_KEY,
                default_input_max_tokens=self.config.INPUT_DEFAULT_MAX_TOKENS,
                default_output_max_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE
            )
        else:
            raise ValueError(f"Unsupported provider: {provider_name}")