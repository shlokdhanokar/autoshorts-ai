"""
Continuous Scheduling System for AutoShorts AI.
Automates video creation on a schedule using APScheduler.
"""

from typing import Optional
from datetime import datetime
import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from workflows.main_pipeline import AutoShortsWorkflow
from config import log, settings


class ContinuousScheduler:
    """
    Continuous scheduling system for automated video creation.
    
    Supports hourly, daily, and weekly scheduling.
    """
    
    def __init__(self):
        """Initialize the scheduler."""
        self.scheduler = AsyncIOScheduler()
        self.workflow = AutoShortsWorkflow()
        self.is_running = False
        
        log.info("Continuous scheduler initialized")
    
    async def start(
        self,
        frequency: str = "daily",
        niche: Optional[str] = None,
        auto_publish: bool = True,
        videos_per_run: int = 1
    ):
        """
        Start continuous video creation.
        
        Args:
            frequency: "hourly", "daily", or "weekly"
            niche: Optional niche filter
            auto_publish: Whether to auto-publish videos
            videos_per_run: Number of videos to create per run
        """
        log.info(f"Starting continuous mode: {frequency}")
        
        # Define the job
        async def create_videos_job():
            """Job to create videos."""
            log.info(f"Scheduled job triggered: creating {videos_per_run} video(s)")
            
            try:
                if videos_per_run == 1:
                    result = await self.workflow.create_video(
                        niche=niche,
                        topic=None,
                        auto_publish=auto_publish
                    )
                    log.info(f"Video created: {result['video_id']} - Status: {result['status']}")
                else:
                    result = await self.workflow.create_batch(
                        count=videos_per_run,
                        niche=niche,
                        auto_publish=auto_publish
                    )
                    log.info(f"Batch completed: {result['successful']}/{result['total_videos']} successful")
            
            except Exception as e:
                log.error(f"Scheduled job failed: {str(e)}")
        
        # Schedule based on frequency
        if frequency == "hourly":
            # Run every hour at minute 0
            trigger = CronTrigger(minute=0)
            self.scheduler.add_job(
                create_videos_job,
                trigger=trigger,
                id="hourly_video_creation",
                replace_existing=True
            )
            log.info("Scheduled: Hourly video creation (every hour at :00)")
        
        elif frequency == "daily":
            # Run daily at optimal times (12pm, 6pm)
            self.scheduler.add_job(
                create_videos_job,
                trigger=CronTrigger(hour=12, minute=0),
                id="daily_video_creation_noon",
                replace_existing=True
            )
            self.scheduler.add_job(
                create_videos_job,
                trigger=CronTrigger(hour=18, minute=0),
                id="daily_video_creation_evening",
                replace_existing=True
            )
            log.info("Scheduled: Daily video creation (12:00 PM and 6:00 PM)")
        
        elif frequency == "weekly":
            # Run weekly on Monday at 10am
            self.scheduler.add_job(
                create_videos_job,
                trigger=CronTrigger(day_of_week='mon', hour=10, minute=0),
                id="weekly_video_creation",
                replace_existing=True
            )
            log.info("Scheduled: Weekly video creation (Mondays at 10:00 AM)")
        
        else:
            raise ValueError(f"Invalid frequency: {frequency}. Use 'hourly', 'daily', or 'weekly'")
        
        # Start the scheduler
        self.scheduler.start()
        self.is_running = True
        
        log.info("Continuous scheduler started successfully")
        
        # Keep running
        try:
            while self.is_running:
                await asyncio.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            log.info("Scheduler interrupted by user")
            self.stop()
    
    def stop(self):
        """Stop the scheduler."""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            log.info("Continuous scheduler stopped")
    
    def get_jobs(self):
        """Get list of scheduled jobs."""
        return self.scheduler.get_jobs()


async def run_continuous(
    frequency: str = "daily",
    niche: Optional[str] = None,
    auto_publish: bool = True,
    videos_per_run: int = 1
):
    """
    Run continuous video creation.
    
    Args:
        frequency: "hourly", "daily", or "weekly"
        niche: Optional niche filter
        auto_publish: Whether to auto-publish
        videos_per_run: Videos to create per run
    """
    scheduler = ContinuousScheduler()
    
    try:
        await scheduler.start(
            frequency=frequency,
            niche=niche,
            auto_publish=auto_publish,
            videos_per_run=videos_per_run
        )
    except KeyboardInterrupt:
        scheduler.stop()
        log.info("Continuous mode stopped by user")


if __name__ == "__main__":
    # Example usage
    asyncio.run(run_continuous(
        frequency="daily",
        niche="self-improvement",
        auto_publish=False,
        videos_per_run=2
    ))
