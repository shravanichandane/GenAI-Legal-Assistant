from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    """
    Abstract base class for LLM providers used in the RAG pipeline.
    """
    
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """
        Generates a response from the LLM based on the prompt.
        
        Args:
            prompt (str): The constructed prompt.
            
        Returns:
            str: The raw generated text from the LLM.
        """
        pass
