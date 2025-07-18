#!/usr/bin/env python3
"""
Test script for RSS-only episode updating (No YouTube API Key Required)
Run this locally to test the episode update process
"""

import os
import sys

# Add the scripts directory to the Python path
sys.path.append(os.path.dirname(__file__))

# Try to import configuration
try:
    import config
    
    # Set environment variables from config (no YouTube API key needed)
    os.environ['YOUTUBE_CHANNEL_ID'] = config.YOUTUBE_CHANNEL_ID
    os.environ['PODCAST_RSS_URL'] = config.PODCAST_RSS_URL
    os.environ['SUBSTACK_RSS_URL'] = config.SUBSTACK_RSS_URL
    
    print("✅ Configuration loaded successfully")
    
except ImportError:
    print("❌ Configuration file not found!")
    print("Please copy scripts/config_simple.py to scripts/config.py and fill in your values")
    sys.exit(1)

# Import and run the updater (RSS version)
from update_episodes_no_api import EpisodeUpdater

def test_connections():
    """Test connections to all services"""
    print("\n🔍 Testing connections...")
    
    updater = EpisodeUpdater()
    
    # Test YouTube RSS
    print("Testing YouTube RSS...")
    youtube_videos = updater.fetch_youtube_videos_rss()
    print(f"  Found {len(youtube_videos)} YouTube videos")
    
    # Test Podcast RSS
    print("Testing Podcast RSS feed...")
    podcast_episodes = updater.fetch_rss_feed(updater.podcast_rss_url, 'podcast') if updater.podcast_rss_url else []
    print(f"  Found {len(podcast_episodes)} podcast episodes")
    
    # Test Substack RSS
    print("Testing Substack RSS feed...")
    substack_episodes = updater.fetch_rss_feed(updater.substack_rss_url, 'substack') if updater.substack_rss_url else []
    print(f"  Found {len(substack_episodes)} Substack episodes")
    
    return youtube_videos, podcast_episodes, substack_episodes

def preview_episodes(youtube_videos, podcast_episodes, substack_episodes):
    """Preview what episodes would be created"""
    print("\n📋 Preview of episodes that would be created:")
    
    updater = EpisodeUpdater()
    matched_episodes = updater.match_episodes_across_sources(youtube_videos, podcast_episodes, substack_episodes)
    
    for i, episode_data in enumerate(matched_episodes, 1):
        youtube = episode_data['youtube']
        print(f"\n{i}. {youtube['title']}")
        print(f"   YouTube ID: {youtube['id']}")
        print(f"   Published: {youtube['published_at']}")
        print(f"   Podcast Match: {'✅' if episode_data['podcast'] else '❌'}")
        print(f"   Substack Match: {'✅' if episode_data['substack'] else '❌'}")
    
    return matched_episodes

def main():
    print("🎙️  Episode Update Test Script (RSS-Only Version)")
    print("=" * 50)
    
    # Test connections
    youtube_videos, podcast_episodes, substack_episodes = test_connections()
    
    if not youtube_videos:
        print("\n⚠️  No new YouTube videos found. This could mean:")
        print("   - All episodes are already imported")
        print("   - YouTube RSS is not accessible")
        print("   - Channel ID is incorrect")
        return
    
    # Preview episodes
    matched_episodes = preview_episodes(youtube_videos, podcast_episodes, substack_episodes)
    
    # Ask if user wants to proceed
    print(f"\n📝 Ready to create {len(matched_episodes)} new episode posts")
    response = input("Do you want to proceed? (y/N): ").strip().lower()
    
    if response == 'y':
        print("\n🚀 Creating episode posts...")
        updater = EpisodeUpdater()
        updater.run()
        print("✅ Done! Check the _posts directory for new files.")
    else:
        print("👋 Cancelled. No posts were created.")

if __name__ == "__main__":
    main() 