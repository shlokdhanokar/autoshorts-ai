"""
Visual Planning Agent for AutoShorts AI.
Maps script segments to appropriate visual types and generates prompts.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from core import BaseAgent
from config import log


@dataclass
class VisualScene:
    """Data class for visual scenes."""
    scene_id: int
    duration: float
    visual_type: str  # "stock_video", "stock_image", "ai_image", "ai_video", "text_overlay"
    search_query: Optional[str]
    ai_prompt: Optional[str]
    aspect_ratio: str = "9:16"


class VisualPlanningAgent(BaseAgent):
    """
    Agent responsible for planning visual content for scripts.
    
    Responsibilities:
    - Map script segments to visual types
    - Generate search queries for stock footage
    - Generate prompts for AI image/video generation
    - Plan transitions and pacing
    - Ensure 9:16 aspect ratio compliance
    """
    
    def __init__(self, agent_id: str = "visual_planning_001"):
        """Initialize the Visual Planning Agent."""
        super().__init__(agent_id=agent_id, agent_type="visual_planning")
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute visual planning.
        
        Args:
            input_data: Input data containing:
                - script: Full script text
                - scenes: List of script scenes with timestamps
                - niche: Content niche
                - tone: Content tone
                
        Returns:
            Dictionary with visual storyboard
        """
        script = input_data["script"]
        scenes = input_data["scenes"]
        niche = input_data.get("niche", "general")
        tone = input_data.get("tone", "educational")
        
        log.info(f"Creating visual storyboard for {len(scenes)} scenes")
        
        # Create visual plan for each scene
        visual_scenes = []
        
        for i, scene in enumerate(scenes):
            visual_scene = await self._plan_scene_visuals(
                scene_id=i + 1,
                scene_text=scene["text"],
                visual_cue=scene.get("visual_cue", ""),
                timestamp=scene.get("timestamp", ""),
                niche=niche,
                tone=tone
            )
            visual_scenes.append(visual_scene)
        
        # Plan transitions
        transitions = self._plan_transitions(visual_scenes)
        
        # Store in memory
        storyboard = {
            "storyboard": [self._scene_to_dict(s) for s in visual_scenes],
            "transitions": transitions,
            "total_scenes": len(visual_scenes),
            "aspect_ratio": "9:16"
        }
        
        self.memory.store_long_term(
            f"storyboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            storyboard
        )
        
        return storyboard
    
    async def _plan_scene_visuals(
        self,
        scene_id: int,
        scene_text: str,
        visual_cue: str,
        timestamp: str,
        niche: str,
        tone: str
    ) -> VisualScene:
        """
        Plan visuals for a single scene.
        
        Args:
            scene_id: Scene identifier
            scene_text: Text content of the scene
            visual_cue: Suggested visual cue
            timestamp: Scene timestamp
            niche: Content niche
            tone: Content tone
            
        Returns:
            VisualScene object
        """
        # Parse duration from timestamp (e.g., "0-3s" -> 3 seconds)
        duration = self._parse_duration(timestamp)
        
        # Determine visual type based on content
        visual_type, search_query, ai_prompt = self._determine_visual_strategy(
            scene_text, visual_cue, niche, scene_id
        )
        
        return VisualScene(
            scene_id=scene_id,
            duration=duration,
            visual_type=visual_type,
            search_query=search_query,
            ai_prompt=ai_prompt,
            aspect_ratio="9:16"
        )
    
    def _parse_duration(self, timestamp: str) -> float:
        """Parse duration from timestamp string."""
        try:
            # Format: "0-3s" or "3-10s"
            parts = timestamp.replace('s', '').split('-')
            if len(parts) == 2:
                return float(parts[1]) - float(parts[0])
        except:
            pass
        return 5.0  # Default duration
    
    def _determine_visual_strategy(
        self,
        scene_text: str,
        visual_cue: str,
        niche: str,
        scene_id: int
    ) -> tuple[str, Optional[str], Optional[str]]:
        """
        Determine the best visual strategy for a scene.
        
        Returns:
            Tuple of (visual_type, search_query, ai_prompt)
        """
        text_lower = scene_text.lower()
        cue_lower = visual_cue.lower()
        
        # First scene (hook) - usually face/person
        if scene_id == 1:
            if "face" in cue_lower or "eye contact" in cue_lower:
                return ("stock_video", "person talking to camera confident", None)
        
        # Determine based on keywords
        
        # Abstract concepts -> AI generation
        if any(word in text_lower for word in ["imagine", "future", "dream", "vision", "concept"]):
            ai_prompt = self._generate_ai_prompt(scene_text, niche)
            return ("ai_image", None, ai_prompt)
        
        # Demonstrations or actions -> Stock video
        if any(word in text_lower for word in ["do", "make", "create", "build", "work"]):
            search_query = self._generate_stock_query(scene_text, niche, "video")
            return ("stock_video", search_query, None)
        
        # Lists or steps -> Text overlay
        if any(word in text_lower for word in ["first", "second", "third", "step", "tip"]):
            return ("text_overlay", None, None)
        
        # Nature, places, objects -> Stock image/video
        if any(word in text_lower for word in ["nature", "city", "place", "building", "landscape"]):
            search_query = self._generate_stock_query(scene_text, niche, "video")
            return ("stock_video", search_query, None)
        
        # Default: stock video with general query
        search_query = self._generate_stock_query(scene_text, niche, "video")
        return ("stock_video", search_query, None)
    
    def _generate_stock_query(self, scene_text: str, niche: str, media_type: str) -> str:
        """
        Generate search query for stock footage.
        
        Args:
            scene_text: Scene text
            niche: Content niche
            media_type: "video" or "image"
            
        Returns:
            Search query string
        """
        # Extract key nouns and verbs (simplified)
        # In production, use NLP for better extraction
        
        keywords = []
        
        # Add niche-related keywords
        niche_keywords = {
            "self-improvement": ["motivation", "success", "growth"],
            "finance": ["money", "business", "investment"],
            "technology": ["tech", "innovation", "digital"],
            "health": ["fitness", "wellness", "healthy"],
        }
        
        if niche in niche_keywords:
            keywords.extend(niche_keywords[niche])
        
        # Extract words from scene text (simple approach)
        important_words = [
            word.strip('.,!?') for word in scene_text.split()
            if len(word) > 4 and word.lower() not in ['this', 'that', 'with', 'from', 'have']
        ]
        
        keywords.extend(important_words[:3])  # Take first 3 important words
        
        # Build query
        query = " ".join(keywords[:4])  # Max 4 keywords
        
        # Add quality modifiers for video
        if media_type == "video":
            query += " cinematic professional"
        
        return query.strip() or f"{niche} content"
    
    def _generate_ai_prompt(self, scene_text: str, niche: str) -> str:
        """
        Generate prompt for AI image/video generation.
        
        Args:
            scene_text: Scene text
            niche: Content niche
            
        Returns:
            AI generation prompt
        """
        # Create descriptive prompt based on scene content
        base_prompt = scene_text[:100]  # Use first 100 chars as base
        
        # Add style modifiers
        style_modifiers = {
            "self-improvement": "inspirational, uplifting, bright colors",
            "finance": "professional, modern, sleek",
            "technology": "futuristic, digital, high-tech",
            "health": "vibrant, energetic, natural",
        }
        
        style = style_modifiers.get(niche, "cinematic, professional")
        
        prompt = f"{base_prompt}, {style}, 9:16 aspect ratio, high quality"
        
        return prompt
    
    def _plan_transitions(self, scenes: List[VisualScene]) -> List[Dict[str, str]]:
        """
        Plan transitions between scenes.
        
        Args:
            scenes: List of visual scenes
            
        Returns:
            List of transition specifications
        """
        transitions = []
        
        for i in range(len(scenes) - 1):
            current_scene = scenes[i]
            next_scene = scenes[i + 1]
            
            # Determine transition type
            if current_scene.visual_type == "text_overlay":
                transition_type = "fade"
            elif current_scene.duration < 3:
                transition_type = "cut"  # Quick scenes use cuts
            else:
                transition_type = "dissolve"
            
            transitions.append({
                "from_scene": current_scene.scene_id,
                "to_scene": next_scene.scene_id,
                "type": transition_type,
                "duration": 0.3 if transition_type != "cut" else 0.0
            })
        
        return transitions
    
    def _scene_to_dict(self, scene: VisualScene) -> Dict[str, Any]:
        """Convert VisualScene to dictionary."""
        return {
            "scene_id": scene.scene_id,
            "duration": scene.duration,
            "visual_type": scene.visual_type,
            "search_query": scene.search_query,
            "ai_prompt": scene.ai_prompt,
            "aspect_ratio": scene.aspect_ratio
        }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data."""
        return "script" in input_data and "scenes" in input_data
    
    def validate_output(self, output_data: Dict[str, Any]) -> bool:
        """Validate output data."""
        required_keys = ["storyboard", "transitions", "total_scenes"]
        return all(key in output_data for key in required_keys)
