"""
AutoShorts AI - Main Entry Point
Automated short-form video creation and publishing system.
"""

import asyncio
import argparse
from pathlib import Path

from workflows.main_pipeline import AutoShortsWorkflow
from config import log, settings


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="AutoShorts AI - Automated Short-Form Video Creation"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate a single video")
    generate_parser.add_argument("--topic", type=str, help="Specific topic (optional)")
    generate_parser.add_argument("--niche", type=str, help="Content niche")
    generate_parser.add_argument("--publish", action="store_true", help="Auto-publish after creation")
    
    # Batch command
    batch_parser = subparsers.add_parser("batch", help="Generate multiple videos")
    batch_parser.add_argument("--count", type=int, default=5, help="Number of videos to create")
    batch_parser.add_argument("--niche", type=str, help="Content niche")
    batch_parser.add_argument("--publish", action="store_true", help="Auto-publish after creation")
    
    # Run command (continuous mode)
    run_parser = subparsers.add_parser("run", help="Run in continuous mode")
    run_parser.add_argument("--frequency", choices=["hourly", "daily", "weekly"], default="daily")
    run_parser.add_argument("--niche", type=str, help="Content niche")
    run_parser.add_argument("--videos-per-run", type=int, default=1, help="Videos to create per run")
    run_parser.add_argument("--publish", action="store_true", help="Auto-publish videos")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="View system status")
    
    args = parser.parse_args()
    
    # Initialize workflow
    workflow = AutoShortsWorkflow()
    
    if args.command == "generate":
        log.info("=== AutoShorts AI - Single Video Generation ===")
        result = await workflow.create_video(
            niche=args.niche,
            topic=args.topic,
            auto_publish=args.publish
        )
        
        print("\n" + "="*50)
        print("VIDEO CREATION RESULT")
        print("="*50)
        print(f"Status: {result['status']}")
        print(f"Video ID: {result['video_id']}")
        if result['status'] == 'completed':
            print(f"Topic: {result['topic']}")
            print(f"Niche: {result['niche']}")
            print(f"Video Path: {result['video_path']}")
            print(f"\nYouTube Title: {result['metadata']['youtube']['title']}")
            print(f"Instagram Caption: {result['metadata']['instagram']['caption'][:100]}...")
            if result.get('publishing'):
                print(f"\nPublishing Status: {result['publishing']['status']}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
        print("="*50)
    
    elif args.command == "batch":
        log.info(f"=== AutoShorts AI - Batch Generation ({args.count} videos) ===")
        result = await workflow.create_batch(
            count=args.count,
            niche=args.niche,
            auto_publish=args.publish
        )
        
        print("\n" + "="*50)
        print("BATCH CREATION RESULT")
        print("="*50)
        print(f"Total Videos: {result['total_videos']}")
        print(f"Successful: {result['successful']}")
        print(f"Failed: {result['failed']}")
        print("="*50)
    
    elif args.command == "run":
        from workflows.continuous_scheduler import ContinuousScheduler
        
        log.info(f"=== AutoShorts AI - Continuous Mode ({args.frequency}) ===")
        print(f"\nRunning in {args.frequency} mode...")
        print(f"Videos per run: {args.videos_per_run}")
        print(f"Auto-publish: {args.publish}")
        print(f"Niche: {args.niche or 'auto-detect'}")
        print("\nPress Ctrl+C to stop\n")
        
        scheduler = ContinuousScheduler()
        await scheduler.start(
            frequency=args.frequency,
            niche=args.niche,
            auto_publish=args.publish,
            videos_per_run=args.videos_per_run
        )
    
    elif args.command == "status":
        status = workflow.get_system_status()
        
        print("\n" + "="*50)
        print("SYSTEM STATUS")
        print("="*50)
        print(f"Total Agents: {status['total_agents']}")
        print(f"Workflow Status: {status['workflow_status']}")
        print(f"\nAgents by Status:")
        for status_type, count in status['agents_by_status'].items():
            print(f"  {status_type.capitalize()}: {count}")
        print("="*50)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Shutting down...")
    except Exception as e:
        log.error(f"Fatal error: {str(e)}")
        raise
