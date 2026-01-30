"""
Scriptwriting Agent for AutoShorts AI.
Generates optimized short-form video scripts.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import re

from core import BaseAgent
from config import log, settings
from core.free_llm_provider import get_llm_provider

class ScriptwritingAgent(BaseAgent):
    """
    Agent responsible for generating short-form optimized scripts.
    """
    
    def __init__(self, agent_id: str = "scriptwriting_001"):
        """Initialize the Scriptwriting Agent."""
        super().__init__(agent_id=agent_id, agent_type="scriptwriting")
        
        # Initialize LLM provider
        self.llm = get_llm_provider()
        self.temperature = settings.llm_temperature
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute script generation task.
        """
        topic = input_data["topic"]
        niche = input_data.get("niche", "general")
        hook = input_data.get("hook", "")
        duration = input_data.get("duration", 45)
        tone = input_data.get("tone", "educational")
        
        log.info(f"Generating script for topic: {topic}")
        
        # Generate generic script
        script_data = await self._generate_script_variant(topic, niche, tone, 0)
        
        # Final safety check
        if not script_data or "scenes" not in script_data:
            log.warning("Script generation failed or missing scenes, using emergency fallback")
            script_data = self._get_emergency_fallback(topic)

        result = {
            "video_id": input_data.get("video_id", f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
            "topic": topic,
            "script": script_data, # Must contain 'scenes'
            "generated_at": datetime.now().isoformat()
        }
        
        self.memory.store_long_term(f"script_{result['video_id']}", result)
        return result

    async def _generate_script_variant(
        self,
        topic: str,
        niche: str,
        style: str,
        variant_id: int
    ) -> Optional[Dict[str, Any]]:
        """Generate a single script variant."""
        prompt = self._construct_prompt(topic, niche, style)
        
        try:
            log.info(f"Generating script variant {variant_id} ({style})")
            
            response_text = await self.llm.generate(
                prompt=prompt,
                system_prompt="You are an expert short-form video scriptwriter. Return ONLY valid JSON.",
                temperature=0.7
            )
            
            # Clean and Parse JSON
            script_data = self._clean_and_parse_json(response_text)
            
            if not script_data:
                # If parsing fails, try to just return fallback immediately or raise
                raise ValueError("Parsed JSON is None")
                
            script_data["variant_id"] = variant_id
            script_data["style"] = style
            
            return script_data
            
        except Exception as e:
            log.error(f"Failed to generate script variant: {str(e)}")
            return self._get_emergency_fallback(topic)

    def _clean_and_parse_json(self, text: str) -> Optional[Dict]:
        """Robustly clean and parse JSON from LLM output."""
        try:
            # 1. Extract from Code Blocks
            json_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
            if json_match:
                text = json_match.group(1)
            elif "```" in text:
                 parts = text.split("```")
                 if len(parts) > 1:
                    text = parts[1]
            
            # 2. Extract potential JSON object { ... }
            start = text.find('{')
            end = text.rfind('}')
            if start != -1 and end != -1:
                text = text[start:end+1]
            
            # 3. Replace Control Characters that break JSON
            text = text.replace('\n', ' ').replace('\r', '').replace('\t', ' ')
            
            return json.loads(text)
        except Exception as e:
            log.error(f"JSON Parse Error: {e} | Text preview: {text[:100]}")
            return None

    def _get_emergency_fallback(self, topic: str) -> Dict[str, Any]:
        """Return a valid structure when everything fails."""
        return {
            "script_content": f"Here is a quick fact about {topic}. It is really interesting. You should learn more about it. Follow for more tips daily.",
            "hook": f"You won't believe this about {topic}",
            "scenes": [
                {"id": 1, "visual_desc": "Person talking to camera", "text": f"Here is a quick fact about {topic}."},
                {"id": 2, "visual_desc": "Montage of relevant images", "text": "It is really interesting. You should learn more about it."},
                {"id": 3, "visual_desc": "Call to action text", "text": "Follow for more tips daily."}
            ]
        }

    def _construct_prompt(self, topic: str, niche: str, style: str) -> str:
        return f"""
        Write a viral short-form video script (approx 45 seconds).
        Topic: {topic}
        Niche: {niche}
        Style: {style}
        
        Structure:
        1. Hook (0-3s) - Grab attention immediately.
        2. Content (3-40s) - Deliver value/story.
        3. CTA (40-45s) - Call to action.
        
        Output valid JSON only. Do not use newlines in strings.
        {{
            "script_content": "Full script text...",
            "hook": "The hook used...",
            "scenes": [
                {{"id": 1, "visual_desc": "visual description", "text": "spoken words"}},
                {{"id": 2, "visual_desc": "visual description", "text": "spoken words"}}
            ]
        }}
        """

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        return "topic" in input_data
    
    def validate_output(self, output_data: Dict[str, Any]) -> bool:
        return "script" in output_data
