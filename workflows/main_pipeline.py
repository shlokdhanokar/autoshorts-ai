"""
Main Pipeline for AutoShorts AI.
Orchestrates the end-to-end video creation workflow.
"""

from typing import Dict, Any, Optional
from datetime import datetime

from core import AgentOrchestrator
from agents import (
    TrendResearchAgent,
    ScriptwritingAgent,
    VisualPlanningAgent,
    MediaGenerationAgent,
    VoiceoverAgent,
    VideoEditingAgent,
    CaptionMetadataAgent,
    PublishingAgent
)
from config import log, settings


class AutoShortsWorkflow:
    """
    Main workflow for automated short-form video creation.
    
    Orchestrates all agents to create videos from trending topics.
    """
    
    def __init__(self):
        """Initialize the workflow."""
        self.orchestrator = AgentOrchestrator()
        
        # Initialize all agents
        self.trend_agent = TrendResearchAgent()
        self.script_agent = ScriptwritingAgent()
        self.visual_agent = VisualPlanningAgent()
        self.media_agent = MediaGenerationAgent()
        self.voiceover_agent = VoiceoverAgent()
        self.editing_agent = VideoEditingAgent()
        self.caption_agent = CaptionMetadataAgent()
        self.publishing_agent = PublishingAgent()
        
        # Register agents with orchestrator
        self.orchestrator.register_agent(self.trend_agent)
        self.orchestrator.register_agent(self.script_agent)
        self.orchestrator.register_agent(self.visual_agent)
        self.orchestrator.register_agent(self.media_agent)
        self.orchestrator.register_agent(self.voiceover_agent)
        self.orchestrator.register_agent(self.editing_agent)
        self.orchestrator.register_agent(self.caption_agent)
        self.orchestrator.register_agent(self.publishing_agent)
        
        log.info("AutoShorts workflow initialized with all agents")
    
    async def create_video(
        self,
        niche: Optional[str] = None,
        topic: Optional[str] = None,
        auto_publish: bool = False
    ) -> Dict[str, Any]:
        """
        Create a complete short-form video from start to finish.
        
        Args:
            niche: Optional niche to focus on
            topic: Optional specific topic (if None, will research trending topics)
            auto_publish: Whether to automatically publish the video
            
        Returns:
            Dictionary with video creation results
        """
        video_id = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        log.info(f"Starting video creation workflow: {video_id}")
        log.info(f"Niche: {niche or 'auto-detect'}, Topic: {topic or 'auto-research'}")
        
        try:
            # Step 1: Trend Research (if topic not provided)
            if not topic:
                log.info("Step 1/8: Researching trending topics...")
                trend_result = await self.trend_agent.run({
                    "niche": niche or settings.default_niche,
                    "platforms": ["youtube", "instagram", "google_trends"],
                    "limit": 1
                })
                
                if not trend_result["topics"]:
                    raise ValueError("No trending topics found")
                
                selected_topic = trend_result["topics"][0]
                topic = selected_topic["topic"]
                niche = selected_topic["niche"]
                hook = selected_topic["hook"]
                target_emotion = selected_topic["target_emotion"]
            else:
                hook = ""
                target_emotion = "curiosity"
                niche = niche or settings.default_niche
            
            log.info(f"Selected topic: {topic}")
            
            # Step 2: Script Generation
            log.info("Step 2/8: Generating script...")
            script_result = await self.script_agent.run({
                "topic": topic,
                "niche": niche,
                "hook": hook,
                "target_emotion": target_emotion,
                "duration": 45,
                "tone": "educational"
            })
            
            script = script_result["script"]
            scenes = script_result["scenes"]
            
            # Step 3: Visual Planning
            log.info("Step 3/8: Planning visuals...")
            visual_result = await self.visual_agent.run({
                "script": script,
                "scenes": scenes,
                "niche": niche,
                "tone": "educational"
            })
            
            storyboard = visual_result["storyboard"]
            transitions = visual_result["transitions"]
            
            # Step 4: Media Generation
            log.info("Step 4/8: Generating media assets...")
            media_result = await self.media_agent.run({
                "storyboard": storyboard,
                "video_id": video_id
            })
            
            assets = media_result["assets"]
            
            # Step 5: Voiceover Generation
            log.info("Step 5/8: Generating voiceover...")
            voiceover_result = await self.voiceover_agent.run({
                "script": script,
                "niche": niche,
                "target_emotion": target_emotion,
                "video_id": video_id,
                "tone": "educational"
            })
            
            audio_path = voiceover_result["audio_path"]
            transcript = voiceover_result["transcript"]
            
            # Step 6: Video Editing
            log.info("Step 6/8: Assembling video...")
            editing_result = await self.editing_agent.run({
                "assets": assets,
                "audio_path": audio_path,
                "transcript": transcript,
                "storyboard": storyboard,
                "video_id": video_id,
                "transitions": transitions
            })
            
            video_path = editing_result["video_path"]
            
            # Step 7: Caption & Metadata Generation
            log.info("Step 7/8: Generating captions and metadata...")
            metadata_result = await self.caption_agent.run({
                "topic": topic,
                "script": script,
                "niche": niche,
                "target_emotion": target_emotion,
                "video_id": video_id
            })
            
            metadata = {
                "youtube": metadata_result["youtube"],
                "instagram": metadata_result["instagram"]
            }
            
            # Step 8: Publishing (if enabled)
            publishing_result = None
            if auto_publish or settings.auto_publish:
                log.info("Step 8/8: Publishing video...")
                publishing_result = await self.publishing_agent.run({
                    "video_path": video_path,
                    "metadata": metadata,
                    "platforms": ["youtube", "instagram"],
                    "video_id": video_id
                })
            else:
                log.info("Step 8/8: Skipping publishing (auto-publish disabled)")
            
            # Compile final result
            result = {
                "video_id": video_id,
                "status": "completed",
                "topic": topic,
                "niche": niche,
                "video_path": video_path,
                "metadata": metadata,
                "publishing": publishing_result,
                "created_at": datetime.now().isoformat()
            }
            
            log.info(f"Video creation completed successfully: {video_id}")
            return result
            
        except Exception as e:
            log.error(f"Video creation failed: {str(e)}")
            return {
                "video_id": video_id,
                "status": "failed",
                "error": str(e),
                "created_at": datetime.now().isoformat()
            }
    
    async def create_batch(
        self,
        count: int = 5,
        niche: Optional[str] = None,
        auto_publish: bool = False
    ) -> Dict[str, Any]:
        """
        Create multiple videos in batch.
        
        Args:
            count: Number of videos to create
            niche: Optional niche filter
            auto_publish: Whether to auto-publish videos
            
        Returns:
            Batch creation results
        """
        log.info(f"Starting batch creation: {count} videos")
        
        results = []
        
        for i in range(count):
            log.info(f"Creating video {i+1}/{count}")
            
            result = await self.create_video(
                niche=niche,
                topic=None,  # Auto-research each time
                auto_publish=auto_publish
            )
            
            results.append(result)
        
        successful = len([r for r in results if r["status"] == "completed"])
        
        return {
            "total_videos": count,
            "successful": successful,
            "failed": count - successful,
            "results": results
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status."""
        return self.orchestrator.get_system_health()
