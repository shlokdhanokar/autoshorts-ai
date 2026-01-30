"""
Caption and Metadata Agent for AutoShorts AI.
Generates optimized titles, descriptions, and hashtags for social media.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime

from core import BaseAgent
from config import log, settings
from core.free_llm_provider import get_llm_provider

class CaptionMetadataAgent(BaseAgent):
    """
    Agent responsible for generating captions and metadata.
    """
    
    def __init__(self, agent_id: str = "caption_metadata_001"):
        """Initialize the Caption & Metadata Agent."""
        super().__init__(agent_id=agent_id, agent_type="caption_metadata")
        
        # Initialize LLM provider
        self.llm = get_llm_provider()
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute caption and metadata generation.
        """
        topic = input_data["topic"]
        script = input_data.get("script", {})
        niche = input_data.get("niche", "general")
        video_id = input_data.get("video_id", f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        log.info(f"Generating metadata for video {video_id}")
        
        # Generate metadata
        title = await self._generate_title(script, niche)
        desc = await self._generate_description(script, niche)
        caption = await self._generate_instagram_caption(script, niche)
        
        result = {
            "video_id": video_id,
            "youtube": {
                "title": title,
                "description": desc,
                "tags": []
            },
            "instagram": {
                "caption": caption,
                "hashtags": []
            },
            "generated_at": datetime.now().isoformat()
        }
        
        self.memory.store_long_term(f"metadata_{video_id}", result)
        return result
    
    async def _generate_title(self, script: Dict[str, Any], niche: str) -> str:
        prompt = f"Generate 1 viral YouTube Short title for niche {niche}. Script snippet: {str(script)[:200]}..."
        try:
            return await self.llm.generate(prompt)
        except:
            return "Amazing Video 🔥"

    async def _generate_description(self, script: Dict[str, Any], niche: str) -> str:
        prompt = f"Generate YouTube description for niche {niche}."
        try:
            return await self.llm.generate(prompt)
        except:
            return "Check this out! #shorts"

    async def _generate_instagram_caption(self, script: Dict[str, Any], niche: str) -> str:
        prompt = f"Generate Instagram caption for niche {niche}."
        try:
            return await self.llm.generate(prompt)
        except:
            return "Double tap! ❤️ #viral"

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        return "topic" in input_data
    
    def validate_output(self, output_data: Dict[str, Any]) -> bool:
        return "youtube" in output_data
