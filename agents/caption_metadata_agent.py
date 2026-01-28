"""
Caption and Metadata Agent for AutoShorts AI.
Generates optimized titles, descriptions, and hashtags for social media.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime

from openai import AsyncOpenAI

from core import BaseAgent
from config import log, settings


class CaptionMetadataAgent(BaseAgent):
    """
    Agent responsible for generating captions and metadata.
    
    Responsibilities:
    - Generate SEO-optimized titles
    - Write compelling descriptions
    - Create platform-specific hashtags
    - Generate multiple variants and select best
    """
    
    def __init__(self, agent_id: str = "caption_metadata_001"):
        """Initialize the Caption & Metadata Agent."""
        super().__init__(agent_id=agent_id, agent_type="caption_metadata")
        
        # Initialize LLM client
        self.llm_client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.llm_model
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute caption and metadata generation.
        
        Args:
            input_data: Input data containing:
                - topic: Video topic
                - script: Video script
                - niche: Content niche
                - target_emotion: Target emotion
                - video_id: Video identifier
                
        Returns:
            Dictionary with titles, descriptions, and hashtags for each platform
        """
        topic = input_data["topic"]
        script = input_data.get("script", "")
        niche = input_data.get("niche", "general")
        target_emotion = input_data.get("target_emotion", "curiosity")
        video_id = input_data.get("video_id", f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        log.info(f"Generating metadata for video {video_id}")
        
        # Generate metadata for each platform
        youtube_metadata = await self._generate_youtube_metadata(topic, script, niche, target_emotion)
        instagram_metadata = await self._generate_instagram_metadata(topic, script, niche, target_emotion)
        
        result = {
            "video_id": video_id,
            "youtube": youtube_metadata,
            "instagram": instagram_metadata,
            "generated_at": datetime.now().isoformat()
        }
        
        # Store in memory
        self.memory.store_long_term(
            f"metadata_{video_id}",
            result
        )
        
        return result
    
    async def _generate_youtube_metadata(
        self,
        topic: str,
        script: str,
        niche: str,
        target_emotion: str
    ) -> Dict[str, Any]:
        """Generate metadata optimized for YouTube Shorts."""
        
        # Generate title
        title = await self._generate_title(topic, niche, target_emotion, platform="youtube")
        
        # Generate description
        description = await self._generate_description(topic, script, niche, platform="youtube")
        
        # Generate hashtags
        hashtags = self._generate_hashtags(topic, niche, platform="youtube")
        
        return {
            "title": title,
            "description": description,
            "hashtags": hashtags,
            "tags": self._generate_tags(topic, niche)
        }
    
    async def _generate_instagram_metadata(
        self,
        topic: str,
        script: str,
        niche: str,
        target_emotion: str
    ) -> Dict[str, Any]:
        """Generate metadata optimized for Instagram Reels."""
        
        # Generate caption (title + description combined for Instagram)
        caption = await self._generate_instagram_caption(topic, script, niche, target_emotion)
        
        # Generate hashtags
        hashtags = self._generate_hashtags(topic, niche, platform="instagram")
        
        return {
            "caption": caption,
            "hashtags": hashtags
        }
    
    async def _generate_title(
        self,
        topic: str,
        niche: str,
        target_emotion: str,
        platform: str
    ) -> str:
        """Generate SEO-optimized title."""
        
        prompt = f"""Create a compelling title for a {platform} Short about: "{topic}"

Niche: {niche}
Target emotion: {target_emotion}

Requirements:
- Maximum 60 characters
- Front-load keywords
- Create curiosity gap
- Use power words
- Include relevant emoji (1-2 max)
- Capitalize properly

Generate ONLY the title, nothing else:"""

        try:
            response = await self.llm_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=50
            )
            
            title = response.choices[0].message.content.strip()
            
            # Ensure title is within character limit
            if len(title) > 60:
                title = title[:57] + "..."
            
            return title
            
        except Exception as e:
            log.error(f"Failed to generate title: {str(e)}")
            # Fallback title
            return f"{topic} 🔥"
    
    async def _generate_description(
        self,
        topic: str,
        script: str,
        niche: str,
        platform: str
    ) -> str:
        """Generate compelling description."""
        
        # Get first 2 lines of script as hook
        script_lines = script.split('\n')
        hook = '\n'.join(script_lines[:2]) if len(script_lines) >= 2 else topic
        
        prompt = f"""Create a description for a {platform} Short.

Topic: {topic}
Niche: {niche}
Script hook: {hook}

Requirements:
- First 2 lines are most important (visible without "show more")
- Include call-to-action
- Mention value/benefit
- Use line breaks for readability
- Keep under 200 characters for first 2 lines
- Total max 500 characters

Generate the description:"""

        try:
            response = await self.llm_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=150
            )
            
            description = response.choices[0].message.content.strip()
            
            # Add standard CTA if not present
            if "follow" not in description.lower() and "subscribe" not in description.lower():
                description += "\n\n🔔 Follow for more!"
            
            return description
            
        except Exception as e:
            log.error(f"Failed to generate description: {str(e)}")
            return f"{hook}\n\n🔔 Follow for more {niche} content!"
    
    async def _generate_instagram_caption(
        self,
        topic: str,
        script: str,
        niche: str,
        target_emotion: str
    ) -> str:
        """Generate Instagram-specific caption (title + description combined)."""
        
        script_lines = script.split('\n')
        hook = script_lines[0] if script_lines else topic
        
        prompt = f"""Create an Instagram Reel caption about: "{topic}"

Niche: {niche}
Hook: {hook}

Requirements:
- Start with attention-grabbing first line
- Use emojis strategically (3-5 total)
- Include call-to-action (save, share, follow)
- Keep under 300 characters
- Conversational tone

Generate the caption:"""

        try:
            response = await self.llm_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=100
            )
            
            caption = response.choices[0].message.content.strip()
            return caption
            
        except Exception as e:
            log.error(f"Failed to generate Instagram caption: {str(e)}")
            return f"{hook} 🔥\n\nDouble tap if you agree! 💯\n\n👉 Follow for more {niche} content"
    
    def _generate_hashtags(self, topic: str, niche: str, platform: str) -> List[str]:
        """Generate platform-optimized hashtags."""
        
        # Base hashtags by niche
        niche_hashtags = {
            "self-improvement": ["selfimprovement", "personalgrowth", "mindset", "motivation", "productivity"],
            "finance": ["finance", "money", "investing", "wealth", "financialfreedom"],
            "technology": ["tech", "technology", "ai", "innovation", "digital"],
            "health": ["health", "fitness", "wellness", "healthy", "workout"],
        }
        
        base_tags = niche_hashtags.get(niche, ["viral", "trending", "fyp"])
        
        # Add topic-specific tags (extract keywords)
        topic_words = [w.lower() for w in topic.split() if len(w) > 4]
        topic_tags = ["".join(w.split()) for w in topic_words[:2]]  # Remove spaces for hashtags
        
        # Platform-specific tags
        platform_tags = {
            "youtube": ["shorts", "youtubeshorts", "short"],
            "instagram": ["reels", "reelsinstagram", "instareels", "explore"]
        }
        
        # Combine all tags
        all_tags = base_tags + topic_tags + platform_tags.get(platform, [])
        
        # Remove duplicates and limit
        unique_tags = list(dict.fromkeys(all_tags))
        
        # Format with #
        hashtags = [f"#{tag}" for tag in unique_tags[:10]]  # Max 10 hashtags
        
        return hashtags
    
    def _generate_tags(self, topic: str, niche: str) -> List[str]:
        """Generate YouTube tags (keywords without #)."""
        
        # Extract keywords from topic
        keywords = [w.lower() for w in topic.split()]
        
        # Add niche
        keywords.append(niche)
        
        # Add common tags
        keywords.extend(["shorts", "short video", "viral"])
        
        return keywords[:15]  # YouTube allows up to 500 characters total
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data."""
        return "topic" in input_data
    
    def validate_output(self, output_data: Dict[str, Any]) -> bool:
        """Validate output data."""
        required_keys = ["youtube", "instagram"]
        return all(key in output_data for key in required_keys)
