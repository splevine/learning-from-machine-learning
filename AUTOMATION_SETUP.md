# Automated Episode Update System

This system automatically pulls episode information from your YouTube channel, podcast RSS feed, and Substack to create Jekyll posts for your website.

## 🎯 What It Does

- **Fetches episodes** from YouTube, podcast RSS, and Substack
- **Matches episodes** across different platforms
- **Creates Jekyll posts** with embedded YouTube videos, Apple Podcast players, and links
- **Runs automatically** on a daily schedule
- **Avoids duplicates** by checking existing posts

## 🚀 Quick Setup

### 1. Get Your API Keys and URLs

You'll need to gather the following information:

#### YouTube API Key
1. Go to [Google Developers Console](https://console.developers.google.com/)
2. Create a new project or select existing one
3. Enable "YouTube Data API v3"
4. Create credentials (API Key)
5. Copy the API key

#### YouTube Channel ID
1. Go to [YouTube Studio](https://studio.youtube.com/)
2. Settings → Channel → Advanced settings
3. Copy your Channel ID
4. Or use this tool: [YouTube Channel ID Finder](https://commentpicker.com/youtube-channel-id.php)

#### Podcast RSS Feed URL
- This is provided by your podcast hosting service (Anchor, Libsyn, Spotify, etc.)
- Usually looks like: `https://anchor.fm/s/[id]/podcast/rss`

#### Substack RSS Feed URL
- Format: `https://your-newsletter.substack.com/feed`
- Replace `your-newsletter` with your actual Substack subdomain

### 2. Test Locally First

Before setting up automation, test the system locally:

1. **Install Python dependencies:**
   ```bash
   pip install requests feedparser python-dateutil pyyaml
   ```

2. **Create configuration file:**
   ```bash
   cp scripts/config_example.py scripts/config.py
   ```

3. **Edit `scripts/config.py` with your actual values:**
   ```python
   YOUTUBE_API_KEY = "your_actual_api_key"
   YOUTUBE_CHANNEL_ID = "your_channel_id"
   PODCAST_RSS_URL = "https://your-podcast-feed.com/rss"
   SUBSTACK_RSS_URL = "https://your-substack.substack.com/feed"
   ```

4. **Run the test script:**
   ```bash
   cd scripts
   python test_update.py
   ```

This will show you what episodes would be created without actually creating them.

### 3. Set Up GitHub Actions (Automated)

Once local testing works, set up automation:

1. **Add GitHub Secrets:**
   Go to your repository → Settings → Secrets and variables → Actions

   Add these secrets:
   - `YOUTUBE_API_KEY`: Your YouTube API key
   - `YOUTUBE_CHANNEL_ID`: Your YouTube channel ID
   - `PODCAST_RSS_URL`: Your podcast RSS feed URL
   - `SUBSTACK_RSS_URL`: Your Substack RSS feed URL

2. **Enable GitHub Actions:**
   - The workflow file `.github/workflows/update-episodes.yml` is already created
   - It will run daily at 6 AM UTC
   - You can also trigger it manually from the Actions tab

3. **Enable GitHub Pages:**
   - Repository Settings → Pages
   - Source: Deploy from a branch
   - Branch: main (or master)

## 🔧 How It Works

### Episode Matching
The system matches episodes across platforms using:
- Episode numbers (e.g., "Episode 1", "Ep. 2", "#3")
- Guest names (extracted from titles like "Episode 1 | John Doe")
- Title similarity

### Post Generation
Each episode post includes:
- **YouTube embed** with full video
- **Episode description** from YouTube and/or podcast
- **Apple Podcasts embed** (if found in RSS)
- **Apple Podcasts badge**
- **Substack link** (if episode found there)
- **Proper Jekyll front matter** with categories and metadata

### Duplicate Prevention
- Checks existing posts for YouTube video IDs
- Only creates posts for new episodes
- Won't overwrite existing content

## 📝 Customization

### Modify Post Template
Edit the `create_jekyll_post` method in `scripts/update_episodes.py` to:
- Change post layout or styling
- Add additional metadata
- Modify content structure
- Add custom sections

### Adjust Matching Logic
Edit the `extract_episode_number` and `extract_guest_name` methods to:
- Handle different title formats
- Add custom episode numbering patterns
- Improve guest name extraction

### Change Schedule
Edit `.github/workflows/update-episodes.yml`:
```yaml
schedule:
  - cron: '0 6 * * *'  # Daily at 6 AM UTC
```

Common cron patterns:
- `0 6 * * *` - Daily at 6 AM UTC
- `0 6 * * 1` - Weekly on Mondays at 6 AM UTC
- `0 */6 * * *` - Every 6 hours

## 🐛 Troubleshooting

### Common Issues

**"No new YouTube videos found"**
- Check YouTube API key and permissions
- Verify Channel ID is correct
- Ensure channel has public videos

**"Error fetching RSS feed"**
- Verify RSS URLs are accessible
- Check if feeds require authentication
- Test URLs in browser

**"Posts not appearing on site"**
- Check GitHub Pages is enabled
- Verify Jekyll build succeeded in Actions tab
- Posts may take a few minutes to appear

**"Duplicate episodes being created"**
- Check if YouTube video IDs are being extracted correctly
- Verify existing posts have proper front matter

### Debug Mode
Add debug output by modifying the script:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Monitoring

### Check GitHub Actions
- Go to your repository → Actions tab
- View workflow runs and logs
- Check for errors or failures

### Manual Trigger
You can manually run the workflow:
1. Go to Actions tab
2. Select "Update Episodes" workflow
3. Click "Run workflow"

## 🔒 Security Notes

- **Never commit API keys** to your repository
- Use GitHub Secrets for all sensitive information
- YouTube API keys should be restricted to your domain
- Monitor API usage to avoid quota limits

## 📈 Future Enhancements

Potential improvements you could add:
- **Guest bio extraction** from episode descriptions
- **Transcript integration** from YouTube captions
- **Social media posting** when new episodes are published
- **Email notifications** for new episodes
- **Analytics integration** for episode performance

## 🆘 Support

If you encounter issues:

1. **Check the logs** in GitHub Actions
2. **Test locally** using the test script
3. **Verify all credentials** are correct
4. **Check API quotas** aren't exceeded

The system is designed to be robust and handle errors gracefully, but monitoring the first few runs is recommended. 