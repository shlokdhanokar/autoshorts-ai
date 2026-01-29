"""
Free TTS Provider for AutoShorts AI.
Uses Edge-TTS (Microsoft Edge Text-to-Speech) - 100% FREE!
"""

from typing import Dict, Any, Optional
from pathlib import Path
import asyncio

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

from config import log


class FreeTTSProvider:
    """
    Free TTS provider using Edge-TTS.
    
    100% FREE - No API key needed!
    Uses Microsoft Edge's text-to-speech engine.
    """
    
    # Available voices (high quality, natural sounding)
    VOICES = {
        "male_us": "en-US-GuyNeural",
        "female_us": "en-US-AriaNeural",
        "male_uk": "en-GB-RyanNeural",
        "female_uk": "en-GB-SoniaNeural",
        "male_au": "en-AU-WilliamNeural",
        "female_au": "en-AU-NatashaNeural",
    }
    
    def __init__(self):
        """Initialize the free TTS provider."""
        if not EDGE_TTS_AVAILABLE:
            log.warning("Edge-TTS not installed. Install with: pip install edge-tts")
        
        self.default_voice = self.VOICES["male_us"]
        log.info("Initialized free TTS provider (Edge-TTS)")
    
    async def generate_speech(
        self,
        text: str,
        output_path: Path,
        voice: Optional[str] = None,
        rate: str = "+0%",
        volume: str = "+0%"
    ) -> Path:
        """
        Generate speech from text.
        
        Args:
            text: Text to convert to speech
            output_path: Path to save audio file
            voice: Voice to use (default: male_us)
            rate: Speech rate (e.g., "+10%" for faster, "-10%" for slower)
            volume: Volume (e.g., "+10%" for louder)
            
        Returns:
            Path to generated audio file
        """
        if not EDGE_TTS_AVAILABLE:
            log.error("Edge-TTS not installed")
            output_path.touch()
            return output_path
        
        try:
            # Select voice
            voice_id = self.VOICES.get(voice, self.default_voice) if voice else self.default_voice
            
            log.debug(f"Generating speech with voice: {voice_id}")
            
            # Create TTS communicator
            communicate = edge_tts.Communicate(
                text=text,
                voice=voice_id,
                rate=rate,
                volume=volume
            )
            
            # Generate and save audio
            await communicate.save(str(output_path))
            
            log.info(f"Speech generated: {output_path}")
            return output_path
            
        except Exception as e:
            log.error(f"Speech generation failed: {str(e)}")
            # Create placeholder
            output_path.touch()
            return output_path
    
    def select_voice_for_content(
        self,
        niche: str,
        tone: str,
        target_emotion: str
    ) -> str:
        """
        Select appropriate voice based on content characteristics.
        
        Args:
            niche: Content niche
            tone: Content tone
            target_emotion: Target emotion
            
        Returns:
            Voice identifier
        """
        # Voice selection logic
        if tone == "motivational" or target_emotion in ["excitement", "aspiration"]:
            return "male_us"  # Energetic male voice
        elif tone == "educational" or niche == "finance":
            return "male_uk"  # Clear, authoritative
        elif tone == "storytelling":
            return "female_us"  # Warm, engaging
        elif niche == "health" or niche == "wellness":
            return "female_au"  # Calm, soothing
        else:
            return "male_us"  # Default
    
    async def get_available_voices(self) -> Dict[str, str]:
        """Get list of available voices."""
        if not EDGE_TTS_AVAILABLE:
            return {}
        
        try:
            voices = await edge_tts.list_voices()
            # Filter for English voices
            english_voices = {
                v["ShortName"]: v["FriendlyName"]
                for v in voices
                if v["Locale"].startswith("en-")
            }
            return english_voices
        except Exception as e:
            log.error(f"Failed to list voices: {str(e)}")
            return self.VOICES


# Global instance
_tts_provider = None

def get_tts_provider() -> FreeTTSProvider:
    """Get or create the global TTS provider instance."""
    global _tts_provider
    if _tts_provider is None:
        _tts_provider = FreeTTSProvider()
    return _tts_provider
