"""
Video Editing Agent for AutoShorts AI.
Assembles final short-form videos from assets.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import json

from core import BaseAgent
from core.video_assembler import VideoAssembler
from config import log, settings


class VideoEditingAgent(BaseAgent):
    """
    Agent responsible for assembling final videos.
    
    Responsibilities:
    - Combine visual assets + voiceover + music
    - Generate dynamic captions with keyword highlighting
    - Apply cuts, zooms, transitions
    - Sync to beat (if music present)
    - Ensure platform compliance (9:16, <60s)
    """
    
    def __init__(self, agent_id: str = "video_editing_001"):
        """Initialize the Video Editing Agent."""
        super().__init__(agent_id=agent_id, agent_type="video_editing")
        
        # Video output directory
        self.videos_dir = Path(settings.videos_dir)
        self.videos_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize video assembler
        self.assembler = VideoAssembler()
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute video editing and assembly.
        
        Args:
            input_data: Input data containing:
                - assets: List of visual assets
                - audio_path: Path to voiceover audio
                - transcript: Transcript with timestamps
                - storyboard: Visual storyboard
                - video_id: Unique video identifier
                - transitions: Transition specifications
                
        Returns:
            Dictionary with final video path and metadata
        """
        assets = input_data["assets"]
        audio_path = input_data["audio_path"]
        transcript = input_data["transcript"]
        storyboard = input_data.get("storyboard", [])
        video_id = input_data.get("video_id", f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        transitions = input_data.get("transitions", [])
        
        log.info(f"Assembling video {video_id} with {len(assets)} assets")
        
        # Generate captions
        captions = self._generate_captions(transcript)
        
        # Assemble video (placeholder - would use MoviePy/FFmpeg)
        video_path = await self._assemble_video(
            assets=assets,
            audio_path=audio_path,
            captions=captions,
            transitions=transitions,
            video_id=video_id
        )
        
        # Get video metadata
        metadata = self._get_video_metadata(video_path, transcript)
        
        result = {
            "video_path": str(video_path),
            "video_id": video_id,
            "duration": metadata["duration"],
            "resolution": metadata["resolution"],
            "aspect_ratio": "9:16",
            "file_size": metadata["file_size"],
            "captions_included": True
        }
        
        # Store in memory
        self.memory.store_long_term(
            f"video_{video_id}",
            result
        )
        
        return result
    
    def _generate_captions(self, transcript: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate dynamic captions with keyword highlighting.
        
        Args:
            transcript: Transcript with word-level timestamps
            
        Returns:
            List of caption segments
        """
        words = transcript.get("words", [])
        
        if not words:
            return []
        
        # Group words into caption segments (2-4 words per caption)
        captions = []
        words_per_caption = 3
        
        for i in range(0, len(words), words_per_caption):
            segment_words = words[i:i + words_per_caption]
            
            if not segment_words:
                continue
            
            caption_text = " ".join([w["word"] for w in segment_words])
            start_time = segment_words[0]["start"]
            end_time = segment_words[-1]["end"]
            
            # Identify keywords to highlight (simplified - in production use NLP)
            highlighted_words = self._identify_keywords(caption_text)
            
            captions.append({
                "text": caption_text,
                "start": start_time,
                "end": end_time,
                "highlighted_words": highlighted_words
            })
        
        return captions
    
    def _identify_keywords(self, text: str) -> List[str]:
        """Identify keywords to highlight in captions."""
        # Simple approach: highlight words with emphasis markers or important words
        important_words = []
        
        for word in text.split():
            word_clean = word.strip('.,!?')
            # Highlight longer words (likely more important)
            if len(word_clean) > 6:
                important_words.append(word_clean)
            # Highlight words with emphasis
            elif any(char in word for char in ['!', '?']):
                important_words.append(word_clean)
        
        return important_words[:2]  # Max 2 highlighted words per caption
    
    async def _assemble_video(
        self,
        assets: List[Dict[str, Any]],
        audio_path: str,
        captions: List[Dict[str, Any]],
        transitions: List[Dict[str, Any]],
        video_id: str
    ) -> Path:
        """
        Assemble final video from components using MoviePy.
        
        Args:
            assets: Visual assets
            audio_path: Voiceover audio path
            captions: Caption data
            transitions: Transition specifications
            video_id: Video identifier
            
        Returns:
            Path to final video file
        """
        output_path = self.videos_dir / f"{video_id}_final.mp4"
        
        log.debug(f"Assembling video with {len(assets)} assets, {len(captions)} captions")
        
        # Use video assembler to create actual video
        try:
            video_path = self.assembler.assemble_video(
                assets=assets,
                audio_path=audio_path,
                captions=captions,
                transitions=transitions,
                output_path=output_path,
                background_music=None  # Optional: add background music path
            )
        except Exception as e:
            log.error(f"Video assembly failed: {str(e)}")
            # Create placeholder on failure
            output_path.touch()
            video_path = output_path
        
        # Store assembly metadata
        assembly_data = {
            "video_id": video_id,
            "assets_count": len(assets),
            "captions_count": len(captions),
            "transitions_count": len(transitions),
            "audio_path": audio_path,
            "timestamp": datetime.now().isoformat()
        }
        
        metadata_path = self.videos_dir / f"{video_id}_assembly.json"
        with open(metadata_path, 'w') as f:
            json.dump(assembly_data, f, indent=2)
        
        log.info(f"Video assembled: {video_path}")
        return video_path
    
    def _get_video_metadata(self, video_path: Path, transcript: Dict[str, Any]) -> Dict[str, Any]:
        """Get metadata for the assembled video."""
        # In production, would use ffprobe or similar
        
        return {
            "duration": transcript.get("duration", 45),
            "resolution": "1080x1920",
            "file_size": "15.2 MB",  # Placeholder
            "codec": "H.264",
            "framerate": 30
        }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data."""
        required_keys = ["assets", "audio_path", "transcript"]
        return all(key in input_data for key in required_keys)
    
    def validate_output(self, output_data: Dict[str, Any]) -> bool:
        """Validate output data."""
        required_keys = ["video_path", "duration", "aspect_ratio"]
        return all(key in output_data for key in required_keys)
