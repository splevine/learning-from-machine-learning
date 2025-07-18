#!/usr/bin/env python3
"""
YouTube Channel ID Finder
This script helps you find your YouTube Channel ID from your channel URL or handle
"""

import re
import requests
import sys

def find_channel_id_from_url(url):
    """Extract channel ID from various YouTube URL formats"""
    
    # Direct channel ID URL
    if '/channel/' in url:
        match = re.search(r'/channel/([a-zA-Z0-9_-]+)', url)
        if match:
            return match.group(1)
    
    # Custom URL format
    if '/c/' in url or '/user/' in url:
        print(f"⚠️  Custom URL detected: {url}")
        print("For custom URLs, you'll need to:")
        print("1. Go to your YouTube channel")
        print("2. View page source (Ctrl+U)")
        print("3. Search for 'channel_id' or 'channelId'")
        print("4. Look for a string like 'UC...' (starts with UC)")
        return None
    
    # Handle @username format
    if '@' in url:
        print(f"⚠️  Handle format detected: {url}")
        print("For @handle URLs, you'll need to:")
        print("1. Go to your YouTube channel")
        print("2. Look in the URL bar for '/channel/UC...' format")
        print("3. Or view page source and search for 'channelId'")
        return None
    
    return None

def test_channel_id(channel_id):
    """Test if a channel ID works by checking the RSS feed"""
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    
    try:
        response = requests.get(rss_url, timeout=10)
        if response.status_code == 200 and '<feed' in response.text:
            return True
        return False
    except:
        return False

def main():
    print("🎥 YouTube Channel ID Finder")
    print("=" * 30)
    
    if len(sys.argv) > 1:
        input_url = sys.argv[1]
    else:
        print("\nHow would you like to find your Channel ID?")
        print("1. Enter your YouTube channel URL")
        print("2. I already know my Channel ID (test it)")
        print("3. Help me find it manually")
        
        choice = input("\nChoose option (1-3): ").strip()
        
        if choice == "1":
            input_url = input("\nEnter your YouTube channel URL: ").strip()
        elif choice == "2":
            channel_id = input("\nEnter your Channel ID to test: ").strip()
            if test_channel_id(channel_id):
                print(f"✅ Channel ID works: {channel_id}")
                print(f"RSS Feed: https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}")
            else:
                print(f"❌ Channel ID doesn't work: {channel_id}")
            return
        elif choice == "3":
            print("\n🔍 How to find your Channel ID manually:")
            print("1. Go to https://studio.youtube.com/")
            print("2. Click Settings (gear icon)")
            print("3. Click Channel → Advanced settings")
            print("4. Your Channel ID is listed there")
            print("\nAlternatively:")
            print("1. Go to your YouTube channel")
            print("2. Right-click → View page source")
            print("3. Search for 'channelId' or 'channel_id'")
            print("4. Look for a string starting with 'UC'")
            return
        else:
            print("Invalid choice")
            return
    
    print(f"\n🔍 Analyzing: {input_url}")
    
    channel_id = find_channel_id_from_url(input_url)
    
    if channel_id:
        print(f"✅ Found Channel ID: {channel_id}")
        
        # Test the channel ID
        print("🧪 Testing channel ID...")
        if test_channel_id(channel_id):
            print("✅ Channel ID works!")
            print(f"\nAdd this to your config.py:")
            print(f'YOUTUBE_CHANNEL_ID = "{channel_id}"')
            print(f"\nRSS Feed URL: https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}")
        else:
            print("❌ Channel ID doesn't seem to work")
    else:
        print("❌ Could not extract Channel ID from URL")
        print("\n📝 Manual steps:")
        print("1. Go to your YouTube channel")
        print("2. Look at the URL - if it contains '/channel/UC...', that's your ID")
        print("3. If not, go to YouTube Studio → Settings → Channel → Advanced")

if __name__ == "__main__":
    main() 