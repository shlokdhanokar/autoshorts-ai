"""
Free LLM Provider for AutoShorts AI.
Supports Ollama (local), Groq (free API), and Hugging Face (free API).
"""

from typing import Dict, Any, Optional, List
import asyncio

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

try:
    from groq import AsyncGroq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    from huggingface_hub import InferenceClient
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

from config import log, settings


class FreeLLMProvider:
    """
    Free LLM provider supporting multiple backends.
    
    Supports:
    - Ollama (local, 100% free)
    - Groq (free API, fast)
    - Hugging Face (free API)
    """
    
    def __init__(self):
        """Initialize the free LLM provider."""
        self.provider = getattr(settings, 'llm_provider', 'ollama').lower()
        
        if self.provider == 'ollama':
            if not OLLAMA_AVAILABLE:
                log.warning("Ollama not installed. Install with: pip install ollama")
            self.base_url = getattr(settings, 'ollama_base_url', 'http://localhost:11434')
            self.model = getattr(settings, 'ollama_model', 'llama3.2')
            
        elif self.provider == 'groq':
            if not GROQ_AVAILABLE:
                log.warning("Groq not installed. Install with: pip install groq")
            api_key = getattr(settings, 'groq_api_key', None)
            if api_key:
                self.client = AsyncGroq(api_key=api_key)
            self.model = getattr(settings, 'groq_model', 'llama-3.3-70b-versatile')
            
        elif self.provider == 'huggingface':
            if not HF_AVAILABLE:
                log.warning("Hugging Face not installed. Install with: pip install huggingface-hub")
            api_key = getattr(settings, 'huggingface_api_key', None)
            if api_key:
                self.client = InferenceClient(token=api_key)
            self.model = getattr(settings, 'hf_model', 'meta-llama/Llama-3.2-3B-Instruct')
        
        log.info(f"Initialized free LLM provider: {self.provider}")
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Generate text using the configured provider.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        if self.provider == 'ollama':
            return await self._generate_ollama(prompt, system_prompt, temperature)
        elif self.provider == 'groq':
            return await self._generate_groq(prompt, system_prompt, temperature, max_tokens)
        elif self.provider == 'huggingface':
            return await self._generate_huggingface(prompt, system_prompt, temperature, max_tokens)
        else:
            log.error(f"Unknown provider: {self.provider}")
            return "Error: Unknown LLM provider"
    
    async def _generate_ollama(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float
    ) -> str:
        """Generate using Ollama (local)."""
        if not OLLAMA_AVAILABLE:
            return "Error: Ollama not installed"
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = await asyncio.to_thread(
                ollama.chat,
                model=self.model,
                messages=messages,
                options={"temperature": temperature}
            )
            
            return response['message']['content']
            
        except Exception as e:
            log.error(f"Ollama generation failed: {str(e)}")
            return f"Error: {str(e)}"
    
    async def _generate_groq(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate using Groq API (free)."""
        if not GROQ_AVAILABLE or not hasattr(self, 'client'):
            return "Error: Groq not configured"
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            log.error(f"Groq generation failed: {str(e)}")
            return f"Error: {str(e)}"
    
    async def _generate_huggingface(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate using Hugging Face API (free)."""
        if not HF_AVAILABLE or not hasattr(self, 'client'):
            return "Error: Hugging Face not configured"
        
        try:
            # Combine system and user prompts
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            response = await asyncio.to_thread(
                self.client.text_generation,
                full_prompt,
                model=self.model,
                max_new_tokens=max_tokens,
                temperature=temperature
            )
            
            return response
            
        except Exception as e:
            log.error(f"Hugging Face generation failed: {str(e)}")
            return f"Error: {str(e)}"


# Global instance
_llm_provider = None

def get_llm_provider() -> FreeLLMProvider:
    """Get or create the global LLM provider instance."""
    global _llm_provider
    if _llm_provider is None:
        _llm_provider = FreeLLMProvider()
    return _llm_provider
