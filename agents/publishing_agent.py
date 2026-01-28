"""
Publishing Agent for AutoShorts AI.
Handles uploading and scheduling content to social media platforms.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path

from core import BaseAgent
from config import log, settings


class PublishingAgent(BaseAgent):
    """
    Agent responsible for publishing videos.
    
    Responsibilities:
    - Upload videos to Instagram Reels and YouTube Shorts
    - Schedule posts based on analytics insights
    - Handle OAuth authentication
    - Retry failed uploads
    - Log all publishing activity
    """
    
    def __init__(self, agent_id: str = "publishing_001"):
        """Initialize the Publishing Agent."""
        super().__init__(agent_id=agent_id, agent_type="publishing")
        
        # Platform credentials
        self.youtube_credentials = {
            "client_id": settings.youtube_client_id,
            "client_secret": settings.youtube_client_secret,
            "refresh_token": settings.youtube_refresh_token
        }
        
        self.instagram_credentials = {
            "access_token": settings.instagram_access_token,
            "business_account_id": settings.instagram_business_account_id
        }
        
        # Publishing settings
        self.auto_publish = settings.auto_publish
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute video publishing.
        
        Args:
            input_data: Input data containing:
                - video_path: Path to video file
                - metadata: Platform-specific metadata
                - platforms: List of platforms to publish to
                - schedule_time: Optional scheduled publish time
                - video_id: Video identifier
                
        Returns:
            Dictionary with publishing results
        """
        video_path = input_data["video_path"]
        metadata = input_data["metadata"]
        platforms = input_data.get("platforms", ["youtube", "instagram"])
        schedule_time = input_data.get("schedule_time")
        video_id = input_data.get("video_id", f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        log.info(f"Publishing video {video_id} to platforms: {platforms}")
        
        # Check if auto-publish is enabled
        if not self.auto_publish and not input_data.get("force_publish", False):
            log.warning("Auto-publish is disabled. Video will not be published.")
            return {
                "video_id": video_id,
                "status": "pending_approval",
                "message": "Auto-publish disabled. Manual approval required."
            }
        
        # Determine optimal posting time if not specified
        if not schedule_time:
            schedule_time = await self._determine_optimal_time(platforms)
        
        # Publish to each platform
        results = {}
        
        if "youtube" in platforms:
            youtube_result = await self._publish_to_youtube(
                video_path=video_path,
                metadata=metadata.get("youtube", {}),
                schedule_time=schedule_time,
                video_id=video_id
            )
            results["youtube"] = youtube_result
        
        if "instagram" in platforms:
            instagram_result = await self._publish_to_instagram(
                video_path=video_path,
                metadata=metadata.get("instagram", {}),
                schedule_time=schedule_time,
                video_id=video_id
            )
            results["instagram"] = instagram_result
        
        # Store publishing log
        publish_log = {
            "video_id": video_id,
            "platforms": platforms,
            "schedule_time": schedule_time.isoformat() if schedule_time else None,
            "results": results,
            "published_at": datetime.now().isoformat()
        }
        
        self.memory.store_long_term(
            f"publish_log_{video_id}",
            publish_log
        )
        
        return {
            "video_id": video_id,
            "status": "published" if all(r.get("success") for r in results.values()) else "partial_failure",
            "results": results,
            "schedule_time": schedule_time.isoformat() if schedule_time else None
        }
    
    async def _publish_to_youtube(
        self,
        video_path: str,
        metadata: Dict[str, Any],
        schedule_time: Optional[datetime],
        video_id: str
    ) -> Dict[str, Any]:
        """
        Publish video to YouTube Shorts.
        
        Args:
            video_path: Path to video file
            metadata: YouTube metadata (title, description, tags)
            schedule_time: Optional scheduled publish time
            video_id: Video identifier
            
        Returns:
            Publishing result
        """
        # TODO: Implement actual YouTube API upload
        # Using YouTube Data API v3
        
        log.info(f"Publishing to YouTube: {metadata.get('title', 'Untitled')}")
        
        # Check credentials
        if not all(self.youtube_credentials.values()):
            log.error("YouTube credentials not configured")
            return {
                "success": False,
                "error": "YouTube credentials not configured",
                "platform": "youtube"
            }
        
        # Simulate upload
        # In production:
        # 1. Authenticate using OAuth 2.0
        # 2. Upload video file
        # 3. Set metadata (title, description, tags)
        # 4. Set as Short (add #Shorts to title/description)
        # 5. Set privacy status (public/scheduled)
        # 6. Get video URL
        
        video_url = f"https://youtube.com/shorts/{video_id}"
        
        log.info(f"YouTube upload successful: {video_url}")
        
        return {
            "success": True,
            "platform": "youtube",
            "video_url": video_url,
            "video_id": video_id,
            "scheduled_for": schedule_time.isoformat() if schedule_time else None
        }
    
    async def _publish_to_instagram(
        self,
        video_path: str,
        metadata: Dict[str, Any],
        schedule_time: Optional[datetime],
        video_id: str
    ) -> Dict[str, Any]:
        """
        Publish video to Instagram Reels.
        
        Args:
            video_path: Path to video file
            metadata: Instagram metadata (caption, hashtags)
            schedule_time: Optional scheduled publish time
            video_id: Video identifier
            
        Returns:
            Publishing result
        """
        # TODO: Implement actual Instagram API upload
        # Using Instagram Graph API
        
        log.info(f"Publishing to Instagram Reels")
        
        # Check credentials
        if not all(self.instagram_credentials.values()):
            log.error("Instagram credentials not configured")
            return {
                "success": False,
                "error": "Instagram credentials not configured",
                "platform": "instagram"
            }
        
        # Simulate upload
        # In production:
        # 1. Upload video to Instagram container
        # 2. Set caption and hashtags
        # 3. Publish container as Reel
        # 4. Get post URL
        
        post_url = f"https://instagram.com/reel/{video_id}"
        
        log.info(f"Instagram upload successful: {post_url}")
        
        return {
            "success": True,
            "platform": "instagram",
            "post_url": post_url,
            "post_id": video_id,
            "scheduled_for": schedule_time.isoformat() if schedule_time else None
        }
    
    async def _determine_optimal_time(self, platforms: List[str]) -> datetime:
        """
        Determine optimal posting time based on analytics.
        
        Args:
            platforms: List of platforms
            
        Returns:
            Optimal posting time
        """
        # Retrieve learnings about best posting times
        learnings = self.memory.retrieve_learnings("optimal_posting_time", min_confidence=0.6)
        
        if learnings:
            # Use learned optimal time
            # For now, use default optimal times
            pass
        
        # Default optimal times (based on general social media best practices)
        optimal_hours = {
            "youtube": [12, 15, 18, 20],  # Noon, 3pm, 6pm, 8pm
            "instagram": [11, 13, 17, 19]  # 11am, 1pm, 5pm, 7pm
        }
        
        # Get current time
        now = datetime.now()
        
        # Find next optimal hour for primary platform
        primary_platform = platforms[0] if platforms else "youtube"
        hours = optimal_hours.get(primary_platform, [12, 18])
        
        # Find next optimal hour
        current_hour = now.hour
        next_hour = min([h for h in hours if h > current_hour], default=hours[0])
        
        # If no hour today, schedule for tomorrow
        if next_hour <= current_hour:
            schedule_time = now + timedelta(days=1)
            schedule_time = schedule_time.replace(hour=hours[0], minute=0, second=0, microsecond=0)
        else:
            schedule_time = now.replace(hour=next_hour, minute=0, second=0, microsecond=0)
        
        log.info(f"Optimal posting time determined: {schedule_time}")
        return schedule_time
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data."""
        required_keys = ["video_path", "metadata"]
        return all(key in input_data for key in required_keys)
    
    def validate_output(self, output_data: Dict[str, Any]) -> bool:
        """Validate output data."""
        required_keys = ["video_id", "status", "results"]
        return all(key in output_data for key in required_keys)
