"""
Analytics & Learning Agent for AutoShorts AI.
Tracks performance metrics and feeds insights back to other agents.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import json

from core import BaseAgent
from config import log, settings


class AnalyticsLearningAgent(BaseAgent):
    """
    Agent responsible for tracking performance and learning.
    
    Responsibilities:
    - Track performance metrics (views, watch time, engagement, retention)
    - Identify patterns in successful content
    - Update system memory with insights
    - Generate weekly performance reports
    - Feed optimization rules back to other agents
    """
    
    def __init__(self, agent_id: str = "analytics_001"):
        """Initialize the Analytics & Learning Agent."""
        super().__init__(agent_id=agent_id, agent_type="analytics_learning")
        
        # YouTube API credentials
        self.youtube_credentials = {
            "client_id": settings.youtube_client_id,
            "client_secret": settings.youtube_client_secret,
            "refresh_token": settings.youtube_refresh_token
        }
        
        # Instagram API credentials
        self.instagram_credentials = {
            "access_token": settings.instagram_access_token,
            "business_account_id": settings.instagram_business_account_id
        }
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute analytics tracking and learning.
        
        Args:
            input_data: Input data containing:
                - video_ids: List of video IDs to analyze
                - platforms: Platforms to track (youtube, instagram)
                - days: Number of days to analyze (default: 7)
                
        Returns:
            Dictionary with analytics results and insights
        """
        video_ids = input_data.get("video_ids", [])
        platforms = input_data.get("platforms", ["youtube", "instagram"])
        days = input_data.get("days", 7)
        
        log.info(f"Analyzing {len(video_ids)} videos across {len(platforms)} platforms")
        
        # Fetch metrics from platforms
        all_metrics = []
        
        if "youtube" in platforms:
            youtube_metrics = await self._fetch_youtube_metrics(video_ids, days)
            all_metrics.extend(youtube_metrics)
        
        if "instagram" in platforms:
            instagram_metrics = await self._fetch_instagram_metrics(video_ids, days)
            all_metrics.extend(instagram_metrics)
        
        # Analyze patterns
        insights = self._analyze_patterns(all_metrics)
        
        # Update agent learnings
        await self._update_learnings(insights)
        
        # Generate report
        report = self._generate_report(all_metrics, insights)
        
        # Store in memory
        self.memory.store_long_term(
            f"analytics_report_{datetime.now().strftime('%Y%m%d')}",
            report
        )
        
        return report
    
    async def _fetch_youtube_metrics(
        self,
        video_ids: List[str],
        days: int
    ) -> List[Dict[str, Any]]:
        """
        Fetch metrics from YouTube Analytics API.
        
        Args:
            video_ids: List of video IDs
            days: Number of days to analyze
            
        Returns:
            List of video metrics
        """
        # TODO: Implement actual YouTube Analytics API call
        log.debug(f"Fetching YouTube metrics for {len(video_ids)} videos")
        
        # Mock data for now
        metrics = []
        for video_id in video_ids:
            metrics.append({
                "video_id": video_id,
                "platform": "youtube",
                "views": 15000,
                "watch_time_hours": 250,
                "avg_view_duration": 35,
                "likes": 850,
                "comments": 120,
                "shares": 45,
                "retention_rate": 0.65,
                "click_through_rate": 0.08,
                "fetched_at": datetime.now().isoformat()
            })
        
        return metrics
    
    async def _fetch_instagram_metrics(
        self,
        video_ids: List[str],
        days: int
    ) -> List[Dict[str, Any]]:
        """
        Fetch metrics from Instagram Insights API.
        
        Args:
            video_ids: List of video IDs
            days: Number of days to analyze
            
        Returns:
            List of video metrics
        """
        # TODO: Implement actual Instagram Insights API call
        log.debug(f"Fetching Instagram metrics for {len(video_ids)} videos")
        
        # Mock data
        metrics = []
        for video_id in video_ids:
            metrics.append({
                "video_id": video_id,
                "platform": "instagram",
                "plays": 12000,
                "reach": 18000,
                "likes": 720,
                "comments": 85,
                "shares": 60,
                "saves": 150,
                "retention_rate": 0.58,
                "fetched_at": datetime.now().isoformat()
            })
        
        return metrics
    
    def _analyze_patterns(self, metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze patterns in video performance.
        
        Args:
            metrics: List of video metrics
            
        Returns:
            Dictionary of insights
        """
        if not metrics:
            return {}
        
        # Calculate averages
        total_videos = len(metrics)
        
        youtube_videos = [m for m in metrics if m["platform"] == "youtube"]
        instagram_videos = [m for m in metrics if m["platform"] == "instagram"]
        
        insights = {
            "total_videos_analyzed": total_videos,
            "platforms": {
                "youtube": {
                    "count": len(youtube_videos),
                    "avg_views": sum(m.get("views", 0) for m in youtube_videos) / len(youtube_videos) if youtube_videos else 0,
                    "avg_retention": sum(m.get("retention_rate", 0) for m in youtube_videos) / len(youtube_videos) if youtube_videos else 0,
                    "avg_engagement": sum(m.get("likes", 0) + m.get("comments", 0) for m in youtube_videos) / len(youtube_videos) if youtube_videos else 0
                },
                "instagram": {
                    "count": len(instagram_videos),
                    "avg_plays": sum(m.get("plays", 0) for m in instagram_videos) / len(instagram_videos) if instagram_videos else 0,
                    "avg_retention": sum(m.get("retention_rate", 0) for m in instagram_videos) / len(instagram_videos) if instagram_videos else 0,
                    "avg_engagement": sum(m.get("likes", 0) + m.get("comments", 0) + m.get("saves", 0) for m in instagram_videos) / len(instagram_videos) if instagram_videos else 0
                }
            },
            "top_performers": self._identify_top_performers(metrics),
            "recommendations": self._generate_recommendations(metrics)
        }
        
        return insights
    
    def _identify_top_performers(self, metrics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify top performing videos."""
        # Sort by engagement (views/plays + likes + comments)
        scored_metrics = []
        
        for m in metrics:
            if m["platform"] == "youtube":
                score = m.get("views", 0) + (m.get("likes", 0) * 10) + (m.get("comments", 0) * 20)
            else:  # instagram
                score = m.get("plays", 0) + (m.get("likes", 0) * 10) + (m.get("saves", 0) * 30)
            
            scored_metrics.append({
                "video_id": m["video_id"],
                "platform": m["platform"],
                "score": score,
                "retention_rate": m.get("retention_rate", 0)
            })
        
        # Sort and return top 5
        scored_metrics.sort(key=lambda x: x["score"], reverse=True)
        return scored_metrics[:5]
    
    def _generate_recommendations(self, metrics: List[Dict[str, Any]]) -> List[str]:
        """Generate actionable recommendations based on metrics."""
        recommendations = []
        
        # Calculate average retention
        avg_retention = sum(m.get("retention_rate", 0) for m in metrics) / len(metrics) if metrics else 0
        
        if avg_retention < 0.5:
            recommendations.append("Retention is below 50%. Consider stronger hooks and faster pacing.")
        elif avg_retention > 0.7:
            recommendations.append("Excellent retention! Continue with current content style.")
        
        # Check engagement
        youtube_videos = [m for m in metrics if m["platform"] == "youtube"]
        if youtube_videos:
            avg_ctr = sum(m.get("click_through_rate", 0) for m in youtube_videos) / len(youtube_videos)
            if avg_ctr < 0.05:
                recommendations.append("Low CTR on YouTube. Improve thumbnails and titles.")
        
        # Platform-specific
        instagram_videos = [m for m in metrics if m["platform"] == "instagram"]
        if instagram_videos:
            avg_saves = sum(m.get("saves", 0) for m in instagram_videos) / len(instagram_videos)
            if avg_saves > 100:
                recommendations.append("High save rate on Instagram. Content is valuable - create more educational content.")
        
        return recommendations
    
    async def _update_learnings(self, insights: Dict[str, Any]) -> None:
        """
        Update agent learnings based on insights.
        
        Args:
            insights: Analytics insights
        """
        # Store successful patterns
        top_performers = insights.get("top_performers", [])
        
        for performer in top_performers:
            if performer["retention_rate"] > 0.6:
                self.memory.store_learning(
                    "high_retention_video",
                    f"Video {performer['video_id']} achieved {performer['retention_rate']:.2%} retention",
                    confidence=min(performer["retention_rate"], 1.0)
                )
        
        # Store optimal posting times (would be calculated from actual data)
        # For now, store general best practices
        recommendations = insights.get("recommendations", [])
        for rec in recommendations:
            self.memory.store_learning(
                "optimization_recommendation",
                rec,
                confidence=0.7
            )
    
    def _generate_report(
        self,
        metrics: List[Dict[str, Any]],
        insights: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive analytics report."""
        return {
            "report_date": datetime.now().isoformat(),
            "period_days": 7,
            "summary": {
                "total_videos": insights.get("total_videos_analyzed", 0),
                "platforms": insights.get("platforms", {}),
                "top_performers": insights.get("top_performers", []),
                "recommendations": insights.get("recommendations", [])
            },
            "raw_metrics": metrics,
            "insights": insights
        }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data."""
        # Can work with empty video_ids (will analyze all recent videos)
        return True
    
    def validate_output(self, output_data: Dict[str, Any]) -> bool:
        """Validate output data."""
        required_keys = ["report_date", "summary"]
        return all(key in output_data for key in required_keys)
