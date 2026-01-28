"""
Example usage of AutoShorts AI system.
Demonstrates how to use the workflow programmatically.
"""

import asyncio
from workflows.main_pipeline import AutoShortsWorkflow
from config import log


async def example_single_video():
    """Example: Create a single video."""
    print("\n=== Example 1: Single Video Creation ===\n")
    
    workflow = AutoShortsWorkflow()
    
    # Create a video on a specific topic
    result = await workflow.create_video(
        niche="self-improvement",
        topic="5 Morning Habits That Changed My Life",
        auto_publish=False  # Don't publish, just create
    )
    
    print(f"Status: {result['status']}")
    if result['status'] == 'completed':
        print(f"Video created: {result['video_path']}")
        print(f"YouTube title: {result['metadata']['youtube']['title']}")


async def example_auto_research():
    """Example: Let the system research trending topics automatically."""
    print("\n=== Example 2: Auto-Research Trending Topics ===\n")
    
    workflow = AutoShortsWorkflow()
    
    # Don't specify topic - let it research automatically
    result = await workflow.create_video(
        niche="finance",
        topic=None,  # Auto-research
        auto_publish=False
    )
    
    print(f"Auto-selected topic: {result.get('topic', 'N/A')}")
    print(f"Status: {result['status']}")


async def example_batch_creation():
    """Example: Create multiple videos in batch."""
    print("\n=== Example 3: Batch Video Creation ===\n")
    
    workflow = AutoShortsWorkflow()
    
    # Create 3 videos
    result = await workflow.create_batch(
        count=3,
        niche="technology",
        auto_publish=False
    )
    
    print(f"Total: {result['total_videos']}")
    print(f"Successful: {result['successful']}")
    print(f"Failed: {result['failed']}")


async def example_with_publishing():
    """Example: Create and publish a video."""
    print("\n=== Example 4: Create and Publish ===\n")
    
    workflow = AutoShortsWorkflow()
    
    # This will publish to YouTube and Instagram if credentials are configured
    result = await workflow.create_video(
        niche="self-improvement",
        auto_publish=True  # Enable publishing
    )
    
    if result.get('publishing'):
        print(f"Publishing status: {result['publishing']['status']}")
        if result['publishing'].get('results'):
            for platform, platform_result in result['publishing']['results'].items():
                if platform_result.get('success'):
                    print(f"{platform}: {platform_result.get('video_url', 'Published')}")


async def main():
    """Run all examples."""
    print("="*60)
    print("AutoShorts AI - Usage Examples")
    print("="*60)
    
    # Run examples
    await example_single_video()
    await example_auto_research()
    await example_batch_creation()
    
    # Uncomment to test publishing (requires API credentials)
    # await example_with_publishing()
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
