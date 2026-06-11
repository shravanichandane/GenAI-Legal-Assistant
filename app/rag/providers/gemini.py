from .base import BaseLLMProvider

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None

class GeminiLLMProvider(BaseLLMProvider):
    """
    Gemini LLM Provider using the google-genai SDK.
    """
    
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        """
        Initialize the Gemini provider.
        
        Args:
            api_key (str): The Google API key.
            model (str): The model name to use.
        """
        if genai is None:
            raise ImportError("The 'google-genai' library is not installed. Please install it.")
        
        self.client = genai.Client(api_key=api_key)
        self.model = model
        
    async def generate(self, prompt: str) -> str:
        """
        Generate a response using Gemini.
        
        Args:
            prompt (str): The prompt to send to the model.
            
        Returns:
            str: The generated text.
        """
        try:
            # Try using the async client first
            if hasattr(self.client, 'aio'):
                response = await self.client.aio.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.0,
                        response_mime_type="application/json"
                    )
                )
            else:
                # Fallback to sync in a thread
                import asyncio
                response = await asyncio.to_thread(
                    self.client.models.generate_content,
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.0,
                        response_mime_type="application/json"
                    )
                )
            return response.text
        except Exception as e:
            raise Exception(f"Failed to generate response from Gemini: {str(e)}")
