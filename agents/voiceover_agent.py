"""
Voiceover Agent for AutoShorts AI.
Generates natural voiceovers for video scripts.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import asyncio

from openai import AsyncOpenAI

from core import BaseAgent
from config import log, settings


class VoiceoverAgent(BaseAgent):
    """
    Agent responsible for creating voiceovers.
    
    Responsibilities:
    - Convert script to natural speech using TTS
    - Select voice based on niche and emotion
    - Control pacing, emphasis, and energy
    - Generate timestamp-aligned transcript
    """
    
    def __init__(self, agent_id: str = "voiceover_001"):
        """Initialize the Voiceover Agent."""
        super().__init__(agent_id=agent_id, agent_type="voiceover")
        
        # Initialize TTS client
        self.tts_provider = settings.tts_provider
        
        if self.tts_provider == "openai":
            self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
        elif self.tts_provider == "elevenlabs":
            # TODO: Initialize ElevenLabs client
            self.elevenlabs_api_key = settings.elevenlabs_api_key
        
        # Audio storage directory
        self.audio_dir = Path(settings.data_dir) / "audio"
        self.audio_dir.mkdir(parents=True, exist_ok=True)
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute voiceover generation.
        
        Args:
            input_data: Input data containing:
                - script: Full script text
                - niche: Content niche
                - target_emotion: Target emotion
                - video_id: Unique video identifier
                - tone: Script tone
                
        Returns:
            Dictionary with voiceover audio path and transcript
        """
        script = input_data["script"]
        niche = input_data.get("niche", "general")
        target_emotion = input_data.get("target_emotion", "neutral")
        video_id = input_data.get("video_id", f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        tone = input_data.get("tone", "educational")
        
        log.info(f"Generating voiceover for video {video_id}")
        
        # Select appropriate voice
        voice_id = self._select_voice(niche, target_emotion, tone)
        
        # Generate voiceover
        audio_path = await self._generate_voiceover(
            script=script,
            voice_id=voice_id,
            video_id=video_id
        )
        
        # Generate timestamp-aligned transcript
        transcript = await self._generate_transcript(script, audio_path)
        
        result = {
            "audio_path": str(audio_path),
            "voice_id": voice_id,
            "transcript": transcript,
            "duration": transcript.get("duration", 0),
            "video_id": video_id
        }
        
        # Store in memory
        self.memory.store_long_term(
            f"voiceover_{video_id}",
            result
        )
        
        return result
    
    def _select_voice(self, niche: str, target_emotion: str, tone: str) -> str:
        """
        Select appropriate voice based on content characteristics.
        
        Args:
            niche: Content niche
            target_emotion: Target emotion
            tone: Content tone
            
        Returns:
            Voice identifier
        """
        # Voice selection logic for OpenAI TTS
        if self.tts_provider == "openai":
            # OpenAI voices: alloy, echo, fable, onyx, nova, shimmer
            
            voice_map = {
                "educational": "onyx",  # Clear, authoritative
                "motivational": "nova",  # Energetic, inspiring
                "entertaining": "shimmer",  # Warm, engaging
                "storytelling": "fable",  # Narrative, expressive
            }
            
            voice = voice_map.get(tone, "alloy")
            
            # Adjust based on emotion
            if target_emotion in ["excitement", "aspiration"]:
                voice = "nova"
            elif target_emotion in ["calm", "trust"]:
                voice = "onyx"
            
            log.debug(f"Selected voice: {voice} for tone={tone}, emotion={target_emotion}")
            return voice
        
        # For ElevenLabs, use configured voice ID or default
        elif self.tts_provider == "elevenlabs":
            return settings.elevenlabs_voice_id or "default_voice"
        
        return "default"
    
    async def _generate_voiceover(
        self,
        script: str,
        voice_id: str,
        video_id: str
    ) -> Path:
        """
        Generate voiceover audio file.
        
        Args:
            script: Script text
            voice_id: Voice identifier
            video_id: Video identifier
            
        Returns:
            Path to generated audio file
        """
        audio_path = self.audio_dir / f"{video_id}_voiceover.mp3"
        
        if self.tts_provider == "openai":
            return await self._generate_openai_tts(script, voice_id, audio_path)
        elif self.tts_provider == "elevenlabs":
            return await self._generate_elevenlabs_tts(script, voice_id, audio_path)
        else:
            log.error(f"Unknown TTS provider: {self.tts_provider}")
            # Create placeholder
            audio_path.touch()
            return audio_path
    
    async def _generate_openai_tts(
        self,
        script: str,
        voice: str,
        output_path: Path
    ) -> Path:
        """Generate voiceover using OpenAI TTS."""
        try:
            log.debug(f"Generating OpenAI TTS with voice: {voice}")
            
            response = await self.openai_client.audio.speech.create(
                model="tts-1-hd",  # High quality model
                voice=voice,
                input=script,
                speed=1.0  # Normal speed
            )
            
            # Save audio file
            response.stream_to_file(str(output_path))
            
            log.info(f"Voiceover generated: {output_path}")
            return output_path
            
        except Exception as e:
            log.error(f"Failed to generate OpenAI TTS: {str(e)}")
            # Create placeholder
            output_path.touch()
            return output_path
    
    async def _generate_elevenlabs_tts(
        self,
        script: str,
        voice_id: str,
        output_path: Path
    ) -> Path:
        """Generate voiceover using ElevenLabs."""
        # TODO: Implement ElevenLabs TTS
        log.warning("ElevenLabs TTS not yet implemented, creating placeholder")
        output_path.touch()
        return output_path
    
    async def _generate_transcript(
        self,
        script: str,
        audio_path: Path
    ) -> Dict[str, Any]:
        """
        Generate timestamp-aligned transcript.
        
        Args:
            script: Original script
            audio_path: Path to audio file
            
        Returns:
            Transcript with word-level timestamps
        """
        # TODO: Use Whisper or similar for precise timing
        # For now, estimate timing based on word count
        
        words = script.split()
        words_per_second = 2.5  # Average speaking rate
        total_duration = len(words) / words_per_second
        
        # Create simple word-level timestamps
        word_timestamps = []
        current_time = 0.0
        time_per_word = total_duration / len(words)
        
        for word in words:
            word_timestamps.append({
                "word": word,
                "start": round(current_time, 2),
                "end": round(current_time + time_per_word, 2)
            })
            current_time += time_per_word
        
        return {
            "text": script,
            "duration": round(total_duration, 2),
            "words": word_timestamps
        }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data."""
        return "script" in input_data
    
    def validate_output(self, output_data: Dict[str, Any]) -> bool:
        """Validate output data."""
        required_keys = ["audio_path", "transcript", "duration"]
        return all(key in output_data for key in required_keys)
