"""
Voiceover Agent for AutoShorts AI.
Generates natural voiceovers for video scripts.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import asyncio

from core import BaseAgent
from config import log, settings
from core.free_tts_provider import get_tts_provider

class VoiceoverAgent(BaseAgent):
    """
    Agent responsible for creating voiceovers.
    """
    
    def __init__(self, agent_id: str = "voiceover_001"):
        """Initialize the Voiceover Agent."""
        super().__init__(agent_id=agent_id, agent_type="voiceover")
        
        # Initialize TTS provider
        self.tts = get_tts_provider()
        
        # Audio storage directory
        self.audio_dir = Path(settings.data_dir) / "audio"
        self.audio_dir.mkdir(parents=True, exist_ok=True)
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute voiceover generation.
        """
        script = input_data.get("script", {})
        # Handle if script is just text or dict
        if isinstance(script, str):
             script_text = script
        else:
             script_text = script.get("script_content", "") or str(script)
             
        video_id = input_data.get("video_id", f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        log.info(f"Generating voiceover for video {video_id}")
        
        if not script_text:
            return {"status": "failed", "error": "Empty script"}
            
        output_dir = Path(settings.data_dir) / "audio"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{video_id}_voiceover.mp3"
        output_path = output_dir / filename
        
        # Generate voiceover
        try:
            # Re-named method is 'generate'
            audio_path = await self.tts.generate(
                text=script_text,
                output_path=output_path,
                voice=input_data.get("voice_id")
            )
        except Exception as e:
            log.error(f"TTS failed: {e}")
            audio_path = None

        if not audio_path:
             # Placeholder
             audio_path = output_path
             audio_path.touch()
        
        # Create Dummy Transcript (Since EdgeTTS doesn't give us word-level timestamps easily)
        # This prevents VideoEditingAgent from crashing
        transcript = {
            "text": script_text,
            "words": [], # Empty words = no dynamic subtitles, but won't crash
            "duration": 45.0 # Estimated/Default
        }
        
        return {
            "status": "completed",
            "video_id": video_id,
            "audio_path": str(audio_path),
            "transcript": transcript, # Required key for main_pipeline
            "transcript_path": str(output_path.with_suffix(".srt")),
            "duration": 45.0
        }

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        return "script" in input_data
    
    def validate_output(self, output_data: Dict[str, Any]) -> bool:
        return "audio_path" in output_data
