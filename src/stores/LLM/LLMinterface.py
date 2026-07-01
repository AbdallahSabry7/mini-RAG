from abc import ABC, abstractmethod

class LLMInterface(ABC):
    @abstractmethod
    def set_generator(self, model_id:str):
        pass

    @abstractmethod
    def set_embedding(self, model_id:str,embedding_size:int = 1536):
        pass

    @abstractmethod
    def generate_text(self, prompt:str , chat_history:list = [], max_output_tokens:int = None, temperature:float = 0.1, top_p:float = None):
        pass

    @abstractmethod
    def generate_embedding(self, text:str , document_type:str):
        pass

    @abstractmethod
    def construct_prompt(self, prompt:str, role:str):
        pass