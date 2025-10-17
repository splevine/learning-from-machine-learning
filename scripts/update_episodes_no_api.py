#!/usr/bin/env python3

import os
import re
import requests
import feedparser
import yaml
from datetime import datetime
from dateutil import parser as date_parser
import json

class EpisodeUpdater:
    def __init__(self):
        self.youtube_channel_id = os.getenv('YOUTUBE_CHANNEL_ID')
        self.podcast_rss_url = os.getenv('PODCAST_RSS_URL')
        self.substack_rss_url = os.getenv('SUBSTACK_RSS_URL')
        
        # Load existing episodes to avoid duplicates
        self.existing_episodes = self.load_existing_episodes()
    
    def load_existing_episodes(self):
        """Load existing episode posts to avoid duplicates"""
        existing = set()
        # Handle both running from scripts/ directory and from root
        script_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.dirname(script_dir)
        posts_dir = os.path.join(repo_root, '_posts')
        if os.path.exists(posts_dir):
            for filename in os.listdir(posts_dir):
                if filename.endswith('.markdown'):
                    filepath = os.path.join(posts_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Extract YouTube ID from existing posts
                            youtube_match = re.search(r'youtubeID:\s*([a-zA-Z0-9_-]+)', content)
                            if youtube_match:
                                video_id = youtube_match.group(1)
                                existing.add(video_id)
                                print(f"Found existing episode with YouTube ID: {video_id} in {filename}")
                    except Exception as e:
                        print(f"Error reading {filename}: {e}")
        
        print(f"Total existing episodes found: {len(existing)}")
        return existing
    
    def fetch_youtube_videos_rss(self):
        """Fetch videos from YouTube channel using RSS feed (no API key needed)"""
        if not self.youtube_channel_id:
            print("YouTube Channel ID not found")
            return []
        
        try:
            # YouTube RSS feed URL
            rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={self.youtube_channel_id}"
            print(f"Fetching YouTube RSS: {rss_url}")
            
            feed = feedparser.parse(rss_url)
            
            if not feed.entries:
                print("No videos found in YouTube RSS feed")
                return []
            
            videos = []
            for entry in feed.entries:
                # Extract video ID from link
                video_id = entry.link.split('v=')[-1] if 'v=' in entry.link else None
                
                if not video_id:
                    continue
                    
                if video_id in self.existing_episodes:
                    print(f"Skipping existing episode: {entry.title} (ID: {video_id})")
                    continue
                
                print(f"Found new episode: {entry.title} (ID: {video_id})")
                videos.append({
                    'id': video_id,
                    'title': entry.title,
                    'description': getattr(entry, 'summary', ''),
                    'published_at': entry.published,
                    'link': entry.link,
                    'thumbnail': ''  # Not available in RSS
                })
            
            return videos
        except Exception as e:
            print(f"Error fetching YouTube RSS feed: {e}")
            return []
    
    def fetch_rss_feed(self, url, source_name):
        """Fetch and parse RSS feed"""
        try:
            feed = feedparser.parse(url)
            episodes = []
            
            for entry in feed.entries:
                episodes.append({
                    'title': entry.title,
                    'description': getattr(entry, 'description', ''),
                    'summary': getattr(entry, 'summary', ''),
                    'link': entry.link,
                    'published': getattr(entry, 'published', ''),
                    'source': source_name
                })
            
            return episodes
        except Exception as e:
            print(f"Error fetching {source_name} RSS feed: {e}")
            return []
    
    def extract_episode_number(self, title):
        """Extract episode number from title"""
        # Look for patterns like "Episode 1", "Ep. 2", "#3", etc.
        patterns = [
            r'episode\s*(\d+)',
            r'ep\.?\s*(\d+)',
            r'#(\d+)',
            r'\|\s*(\d+)\s*\|'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, title, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return None
    
    def extract_guest_name(self, title):
        """Extract guest name from title"""
        # Look for pattern "Episode X | Guest Name"
        match = re.search(r'\|\s*([^|]+?)(?:\s*\||$)', title)
        if match:
            guest = match.group(1).strip()
            # Remove common prefixes
            guest = re.sub(r'^(with\s+|ft\.?\s+|featuring\s+)', '', guest, flags=re.IGNORECASE)
            return guest
        return None
    
    def match_episodes_across_sources(self, youtube_videos, podcast_episodes, substack_episodes):
        """Match episodes across different sources"""
        matched_episodes = []
        
        for video in youtube_videos:
            episode_num = self.extract_episode_number(video['title'])
            guest_name = self.extract_guest_name(video['title'])
            
            episode_data = {
                'youtube': video,
                'episode_number': episode_num,
                'guest_name': guest_name,
                'podcast': None,
                'substack': None
            }
            
            # Try to match with podcast episodes
            for podcast_ep in podcast_episodes:
                if (episode_num and self.extract_episode_number(podcast_ep['title']) == episode_num) or \
                   (guest_name and guest_name.lower() in podcast_ep['title'].lower()):
                    episode_data['podcast'] = podcast_ep
                    break
            
            # Try to match with substack episodes
            for substack_ep in substack_episodes:
                if (episode_num and self.extract_episode_number(substack_ep['title']) == episode_num) or \
                   (guest_name and guest_name.lower() in substack_ep['title'].lower()):
                    episode_data['substack'] = substack_ep
                    break
            
            matched_episodes.append(episode_data)
        
        return matched_episodes
    
    def create_jekyll_post(self, episode_data):
        """Create a Jekyll post for an episode"""
        youtube = episode_data['youtube']
        podcast = episode_data.get('podcast')
        substack = episode_data.get('substack')
        
        # Parse date
        try:
            pub_date = date_parser.parse(youtube['published_at'])
        except:
            pub_date = datetime.now()
        
        # Create filename
        date_str = pub_date.strftime('%Y-%m-%d')
        title_slug = re.sub(r'[^\w\s-]', '', youtube['title']).strip().lower()
        title_slug = re.sub(r'[-\s]+', '-', title_slug)
        filename = f"{date_str}-{title_slug}.markdown"
        
        # Extract Apple Podcast episode ID if available
        apple_podcast_id = ""
        if podcast and 'link' in podcast:
            apple_match = re.search(r'i=(\d+)', podcast['link'])
            if apple_match:
                apple_podcast_id = apple_match.group(1)
        
        # Create front matter
        front_matter = {
            'layout': 'post',
            'title': youtube['title'],
            'date': pub_date.strftime('%Y-%m-%d %H:%M:%S %z') or pub_date.strftime('%Y-%m-%d %H:%M:%S -0500'),
            'categories': 'machine learning updates',
            'youtubeID': youtube['id']
        }
        
        # Add Substack URL if available
        if substack and substack.get('link'):
            front_matter['substack_url'] = substack['link']
        
        # Create post content
        content_parts = []
        
        # Episode description from YouTube
        description = youtube.get('description', '')
        if description:
            # Get first few paragraphs, clean up
            paragraphs = description.split('\n\n')[:3]  # First 3 paragraphs
            for para in paragraphs:
                para = para.strip()
                if para and not para.startswith('http') and not para.startswith('---'):
                    content_parts.append(para)
                    content_parts.append("")
        
        # Add podcast description if available and different
        if podcast and podcast.get('description'):
            podcast_desc = podcast['description'].strip()
            if podcast_desc and podcast_desc not in youtube.get('description', ''):
                content_parts.append(podcast_desc)
                content_parts.append("")
        
        # Write the file
        full_content = "---\n" + yaml.dump(front_matter, default_flow_style=False) + "---\n"
        full_content += "\n".join(content_parts)
        
        # Create posts in the main _posts directory
        # Handle both running from scripts/ directory and from root
        script_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.dirname(script_dir)
        posts_dir = os.path.join(repo_root, '_posts')
        filepath = os.path.join(posts_dir, filename)
        os.makedirs(posts_dir, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        print(f"Created post: {filename}")
    
    def run(self):
        """Main execution function"""
        print("Starting episode update process (No API key version)...")
        
        # Fetch data from all sources
        print("Fetching YouTube videos via RSS...")
        youtube_videos = self.fetch_youtube_videos_rss()
        print(f"Found {len(youtube_videos)} new YouTube videos")
        
        print("Fetching podcast RSS feed...")
        podcast_episodes = []
        if self.podcast_rss_url:
            podcast_episodes = self.fetch_rss_feed(self.podcast_rss_url, 'podcast')
        print(f"Found {len(podcast_episodes)} podcast episodes")
        
        print("Fetching Substack RSS feed...")
        substack_episodes = []
        if self.substack_rss_url:
            substack_episodes = self.fetch_rss_feed(self.substack_rss_url, 'substack')
        print(f"Found {len(substack_episodes)} Substack episodes")
        
        # Match episodes across sources
        print("Matching episodes across sources...")
        matched_episodes = self.match_episodes_across_sources(youtube_videos, podcast_episodes, substack_episodes)
        
        # Create Jekyll posts
        print("Creating Jekyll posts...")
        for episode_data in matched_episodes:
            self.create_jekyll_post(episode_data)
        
        print(f"Episode update complete! Created {len(matched_episodes)} new posts.")

if __name__ == "__main__":
    updater = EpisodeUpdater()
    updater.run() 