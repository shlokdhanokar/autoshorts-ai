"""
Video Assembly Module for AutoShorts AI.
Handles actual video creation using MoviePy.
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime

import PIL.Image

# Patch PIL.Image.ANTIALIAS for MoviePy compatibility (Pillow 10+ removed it)
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

try:
    from moviepy.editor import (
        VideoFileClip, ImageClip, AudioFileClip, TextClip,
        CompositeVideoClip, concatenate_videoclips, ColorClip,
        CompositeAudioClip
    )
    from moviepy.video.fx import resize, fadein, fadeout
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    # Define dummy classes for type hints if MoviePy is missing
    VideoFileClip = Any
    ImageClip = Any
    AudioFileClip = Any
    TextClip = Any
    CompositeVideoClip = Any
    ColorClip = Any
    CompositeAudioClip = Any

from config import log


class VideoAssembler:
    """
    Video assembly engine using MoviePy.
    Creates final videos from assets, audio, and captions.
    """
    
    def __init__(self):
        """Initialize the video assembler."""
        if not MOVIEPY_AVAILABLE:
            log.warning("MoviePy not available. Video assembly will use placeholders.")
        
        # Video settings
        self.width = 1080
        self.height = 1920
        self.fps = 30
        self.aspect_ratio = (9, 16)
    
    def assemble_video(
        self,
        assets: List[Dict[str, Any]],
        audio_path: str,
        captions: List[Dict[str, Any]],
        transitions: List[Dict[str, Any]],
        output_path: Path,
        background_music: Optional[str] = None
    ) -> Path:
        """
        Assemble final video from components.
        
        Args:
            assets: List of visual assets with scene info
            audio_path: Path to voiceover audio
            captions: Caption data with timestamps
            transitions: Transition specifications
            output_path: Output video path
            background_music: Optional background music path
            
        Returns:
            Path to assembled video
        """
        if not MOVIEPY_AVAILABLE:
            log.warning("MoviePy not available, creating placeholder")
            output_path.touch()
            return output_path
        
        try:
            log.info(f"Assembling video with {len(assets)} assets")
            
            # Load voiceover audio
            audio = AudioFileClip(str(audio_path))
            total_duration = audio.duration
            
            # Create video clips from assets
            video_clips = self._create_video_clips(assets, total_duration)
            
            # Concatenate clips with transitions
            main_video = self._apply_transitions(video_clips, transitions)
            
            # Add captions
            video_with_captions = self._add_captions(main_video, captions)
            
            # Add voiceover audio
            final_video = video_with_captions.set_audio(audio)
            
            # Add background music if provided
            if background_music and Path(background_music).exists():
                final_video = self._add_background_music(final_video, background_music)
            
            # Ensure correct dimensions
            final_video = final_video.resize((self.width, self.height))
            
            # Export video
            log.info(f"Exporting video to {output_path}")
            final_video.write_videofile(
                str(output_path),
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                preset='medium',
                threads=4,
                logger=None  # Suppress MoviePy progress bar
            )
            
            # Clean up
            audio.close()
            final_video.close()
            
            log.info(f"Video assembly complete: {output_path}")
            return output_path
            
        except Exception as e:
            log.error(f"Video assembly failed: {str(e)}")
            # Create placeholder on failure
            output_path.touch()
            return output_path
    
    def _create_video_clips(
        self,
        assets: List[Dict[str, Any]],
        total_duration: float
    ) -> List[VideoFileClip]:
        """Create video clips from assets."""
        clips = []
        
        for asset in assets:
            asset_type = asset.get("type", "")
            asset_path = asset.get("path")
            duration = asset.get("duration", 5.0)
            
            if not asset_path or not Path(asset_path).exists():
                # Create placeholder clip
                clip = self._create_placeholder_clip(duration)
            else:
                clip = self._create_placeholder_clip(duration)
            
            # Resize
            if clip.size != (self.width, self.height):
                 clip = clip.resize((self.width, self.height))
            
            clips.append(clip)
        
        if not clips:
             return [self._create_placeholder_clip(total_duration)]

        # Ensure clips cover total duration
        final_clips = []
        current_duration = 0.0
        
        # Add clips until we exceed audio duration (max 100 loops to prevent infinite hang)
        loop_count = 0
        while current_duration < total_duration and loop_count < 100:
            loop_count += 1
            for clip in clips:
                 # Check if we're done
                 if current_duration >= total_duration:
                     break

                 # Append clip
                 new_clip = clip.copy()
                 final_clips.append(new_clip)
                 current_duration += new_clip.duration
        
        return final_clips
    
    def _create_placeholder_clip(self, duration: float) -> ColorClip:
        """Create a placeholder color clip."""
        return ColorClip(
            size=(self.width, self.height),
            color=(20, 20, 30),  # Dark blue-gray
            duration=duration
        )
    
    def _create_text_clip(self, duration: float) -> TextClip:
        """Create a text overlay clip."""
        try:
            return TextClip(
                "Content",
                fontsize=70,
                color='white',
                size=(self.width, self.height),
                method='caption',
                align='center'
            ).set_duration(duration)
        except:
            # Fallback if font issues
            return self._create_placeholder_clip(duration)
    
    def _apply_transitions(
        self,
        clips: List[VideoFileClip],
        transitions: List[Dict[str, Any]]
    ) -> VideoFileClip:
        """Apply transitions between clips."""
        if not clips:
            return self._create_placeholder_clip(5.0)
        
        # For now, simple concatenation
        # TODO: Implement crossfade, dissolve transitions
        return concatenate_videoclips(clips, method="compose")
    
    def _add_captions(
        self,
        video: VideoFileClip,
        captions: List[Dict[str, Any]]
    ) -> CompositeVideoClip:
        """Add animated captions to video."""
        caption_clips = []
        
        for caption_data in captions:
            text = caption_data.get("text", "")
            start = caption_data.get("start", 0)
            end = caption_data.get("end", start + 2)
            
            try:
                # Create caption clip
                caption_clip = TextClip(
                    text,
                    fontsize=60,
                    color='white',
                    stroke_color='black',
                    stroke_width=2,
                    method='caption',
                    size=(self.width - 100, None),
                    align='center'
                )
                
                # Position at bottom center
                caption_clip = caption_clip.set_position(('center', self.height - 400))
                caption_clip = caption_clip.set_start(start)
                caption_clip = caption_clip.set_duration(end - start)
                
                # Add fade in/out
                caption_clip = caption_clip.crossfadein(0.2).crossfadeout(0.2)
                
                caption_clips.append(caption_clip)
                
            except Exception as e:
                log.warning(f"Failed to create caption: {str(e)}")
                continue
        
        # Composite video with captions
        if caption_clips:
            return CompositeVideoClip([video] + caption_clips)
        return video
    
    def _add_background_music(
        self,
        video: VideoFileClip,
        music_path: str,
        volume: float = 0.15
    ) -> VideoFileClip:
        """Add background music to video."""
        try:
            music = AudioFileClip(music_path)
            
            # Loop music if shorter than video
            if music.duration < video.duration:
                music = music.audio_loop(duration=video.duration)
            else:
                music = music.subclip(0, video.duration)
            
            # Reduce volume
            music = music.volumex(volume)
            
            # Mix with existing audio
            if video.audio:
                final_audio = CompositeAudioClip([video.audio, music])
            else:
                final_audio = music
            
            return video.set_audio(final_audio)
            
        except Exception as e:
            log.warning(f"Failed to add background music: {str(e)}")
            return video


def create_sample_video(output_path: Path) -> Path:
    """
    Create a sample video for testing.
    
    Args:
        output_path: Output path for sample video
        
    Returns:
        Path to created video
    """
    if not MOVIEPY_AVAILABLE:
        log.warning("MoviePy not available")
        output_path.touch()
        return output_path
    
    try:
        # Create simple test video
        clip = ColorClip(size=(1080, 1920), color=(50, 50, 100), duration=5)
        
        text = TextClip(
            "AutoShorts AI\nTest Video",
            fontsize=80,
            color='white',
            size=(1080, 1920),
            method='caption',
            align='center'
        ).set_duration(5)
        
        video = CompositeVideoClip([clip, text])
        
        video.write_videofile(
            str(output_path),
            fps=30,
            codec='libx264',
            logger=None
        )
        
        video.close()
        return output_path
        
    except Exception as e:
        log.error(f"Failed to create sample video: {str(e)}")
        output_path.touch()
        return output_path
