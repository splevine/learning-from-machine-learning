#!/usr/bin/env python3
"""
All-in-One Episode Updater
Simple script to update all episodes from YouTube, Podcast RSS, and Substack
"""

import os
import sys

def main():
    print("🎙️ Learning from Machine Learning - Episode Updater")
    print("=" * 55)
    print()
    
    # Check if config exists
    if not os.path.exists('config.py'):
        print("❌ Configuration file not found!")
        print("Please copy config_simple.py to config.py and fill in your values:")
        print("  cp config_simple.py config.py")
        print("  # Edit config.py with your actual URLs")
        return
    
    print("🔄 This will update your Jekyll site with new episodes from:")
    print("   • YouTube RSS feed")
    print("   • Podcast RSS feed")  
    print("   • Substack RSS feed")
    print()
    
    # Import and run the no-API updater
    try:
        from update_episodes_no_api import EpisodeUpdater
        
        print("🚀 Starting episode update...")
        updater = EpisodeUpdater()
        updater.run()
        
        print()
        print("✅ Episode update complete!")
        print("🌐 Your Jekyll site now has all the latest episodes")
        print("📝 Check the _posts directory for new files")
        
    except ImportError as e:
        print(f"❌ Error importing dependencies: {e}")
        print("Please install requirements: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error during update: {e}")

if __name__ == "__main__":
    main() 