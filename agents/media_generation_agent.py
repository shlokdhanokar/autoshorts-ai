"""
Media Generation Agent for AutoShorts AI.
Generates and fetches visual assets for video production.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import asyncio
import aiohttp

from core import BaseAgent
from config import log, settings


class MediaGenerationAgent(BaseAgent):
    """
    Agent responsible for generating all visual assets.
    
    Responsibilities:
    - Fetch stock footage from Pexels/Pixabay
    - Generate AI images using Stability AI or DALL-E
    - Generate AI videos (future: Runway ML)
    - Store assets with scene alignment metadata
    """
    
    def __init__(self, agent_id: str = "media_generation_001"):
        """Initialize the Media Generation Agent."""
        super().__init__(agent_id=agent_id, agent_type="media_generation")
        
        # API keys
        self.pexels_api_key = settings.pexels_api_key
        self.pixabay_api_key = settings.pixabay_api_key
        self.stability_api_key = settings.stability_api_key
        
        # Asset storage directory
        self.assets_dir = Path(settings.assets_dir)
        self.assets_dir.mkdir(parents=True, exist_ok=True)
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute media generation.
        
        Args:
            input_data: Input data containing:
                - storyboard: Visual storyboard with scenes
                - video_id: Unique identifier for this video
                
        Returns:
            Dictionary with generated asset paths
        """
        storyboard = input_data["storyboard"]
        video_id = input_data.get("video_id", f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        log.info(f"Generating media assets for {len(storyboard)} scenes")
        
        # Create video-specific asset directory
        video_assets_dir = self.assets_dir / video_id
        video_assets_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate assets for each scene
        assets = []
        
        for scene in storyboard:
            asset = await self._generate_scene_asset(scene, video_assets_dir)
            if asset:
                assets.append(asset)
        
        result = {
            "video_id": video_id,
            "assets": assets,
            "total_assets": len(assets),
            "assets_directory": str(video_assets_dir)
        }
        
        # Store in memory
        self.memory.store_long_term(
            f"assets_{video_id}",
            result
        )
        
        return result
    
    async def _generate_scene_asset(
        self,
        scene: Dict[str, Any],
        output_dir: Path
    ) -> Optional[Dict[str, Any]]:
        """
        Generate or fetch asset for a single scene.
        
        Args:
            scene: Scene specification
            output_dir: Output directory for assets
            
        Returns:
            Asset metadata or None if failed
        """
        scene_id = scene["scene_id"]
        visual_type = scene["visual_type"]
        
        log.debug(f"Generating asset for scene {scene_id} ({visual_type})")
        
        try:
            if visual_type == "stock_video":
                return await self._fetch_stock_video(scene, output_dir)
            
            elif visual_type == "stock_image":
                return await self._fetch_stock_image(scene, output_dir)
            
            elif visual_type == "ai_image":
                return await self._generate_ai_image(scene, output_dir)
            
            elif visual_type == "ai_video":
                return await self._generate_ai_video(scene, output_dir)
            
            elif visual_type == "text_overlay":
                # Text overlays don't need asset generation
                return {
                    "scene_id": scene_id,
                    "type": "text_overlay",
                    "path": None
                }
            
            else:
                log.warning(f"Unknown visual type: {visual_type}")
                return None
                
        except Exception as e:
            log.error(f"Failed to generate asset for scene {scene_id}: {str(e)}")
            return None
    
    async def _fetch_stock_video(
        self,
        scene: Dict[str, Any],
        output_dir: Path
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch stock video from Pexels.
        
        Args:
            scene: Scene specification
            output_dir: Output directory
            
        Returns:
            Asset metadata
        """
        search_query = scene.get("search_query", "abstract background")
        scene_id = scene["scene_id"]
        
        if not self.pexels_api_key:
            log.warning("Pexels API key not configured, using placeholder")
            return self._create_placeholder_asset(scene_id, "video", output_dir)
        
        # TODO: Implement actual Pexels API call
        # For now, return mock data
        log.debug(f"Fetching stock video: {search_query}")
        
        # Simulate API call
        await asyncio.sleep(0.1)
        
        # In production, download actual video
        asset_path = output_dir / f"scene_{scene_id}_stock.mp4"
        
        return {
            "scene_id": scene_id,
            "type": "stock_video",
            "path": str(asset_path),
            "source": "pexels",
            "query": search_query,
            "duration": scene.get("duration", 5.0)
        }
    
    async def _fetch_stock_image(
        self,
        scene: Dict[str, Any],
        output_dir: Path
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch stock image from Pexels.
        
        Args:
            scene: Scene specification
            output_dir: Output directory
            
        Returns:
            Asset metadata
        """
        search_query = scene.get("search_query", "abstract background")
        scene_id = scene["scene_id"]
        
        if not self.pexels_api_key:
            log.warning("Pexels API key not configured, using placeholder")
            return self._create_placeholder_asset(scene_id, "image", output_dir)
        
        # TODO: Implement actual Pexels API call
        log.debug(f"Fetching stock image: {search_query}")
        
        await asyncio.sleep(0.1)
        
        asset_path = output_dir / f"scene_{scene_id}_stock.jpg"
        
        return {
            "scene_id": scene_id,
            "type": "stock_image",
            "path": str(asset_path),
            "source": "pexels",
            "query": search_query
        }
    
    async def _generate_ai_image(
        self,
        scene: Dict[str, Any],
        output_dir: Path
    ) -> Optional[Dict[str, Any]]:
        """
        Generate AI image using DALL-E or Stability AI.
        
        Args:
            scene: Scene specification
            output_dir: Output directory
            
        Returns:
            Asset metadata
        """
        ai_prompt = scene.get("ai_prompt", "abstract artistic background")
        scene_id = scene["scene_id"]
        
        # TODO: Implement actual AI image generation
        # Using OpenAI DALL-E or Stability AI
        log.debug(f"Generating AI image: {ai_prompt}")
        
        await asyncio.sleep(0.1)
        
        asset_path = output_dir / f"scene_{scene_id}_ai.png"
        
        return {
            "scene_id": scene_id,
            "type": "ai_image",
            "path": str(asset_path),
            "source": "ai_generated",
            "prompt": ai_prompt
        }
    
    async def _generate_ai_video(
        self,
        scene: Dict[str, Any],
        output_dir: Path
    ) -> Optional[Dict[str, Any]]:
        """
        Generate AI video using Runway ML or similar.
        
        Args:
            scene: Scene specification
            output_dir: Output directory
            
        Returns:
            Asset metadata
        """
        ai_prompt = scene.get("ai_prompt", "abstract motion background")
        scene_id = scene["scene_id"]
        
        # TODO: Implement AI video generation
        # This is expensive and may not be needed for MVP
        log.debug(f"AI video generation not yet implemented: {ai_prompt}")
        
        # Fallback to stock video
        return await self._fetch_stock_video(scene, output_dir)
    
    def _create_placeholder_asset(
        self,
        scene_id: int,
        asset_type: str,
        output_dir: Path
    ) -> Dict[str, Any]:
        """Create placeholder asset metadata when APIs are not available."""
        extension = "mp4" if asset_type == "video" else "jpg"
        asset_path = output_dir / f"scene_{scene_id}_placeholder.{extension}"
        
        return {
            "scene_id": scene_id,
            "type": f"placeholder_{asset_type}",
            "path": str(asset_path),
            "source": "placeholder"
        }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data."""
        return "storyboard" in input_data
    
    def validate_output(self, output_data: Dict[str, Any]) -> bool:
        """Validate output data."""
        required_keys = ["video_id", "assets", "total_assets"]
        return all(key in output_data for key in required_keys)
