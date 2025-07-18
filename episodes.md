---
layout: page
title: All Episodes
permalink: /episodes/
description: Browse all episodes of Learning from Machine Learning podcast featuring industry experts sharing their insights on ML, data science, and career advice.
---

## Browse All {{ site.posts.size }} Episodes

Explore conversations with industry experts and practitioners sharing their experiences, insights, and advice on succeeding in Machine Learning and Data Science.

<div class="episodes-grid">
{% assign episode_posts = site.posts | where: "categories", "machine learning updates" %}
{% for post in episode_posts %}
  <article class="episode-card" style="border: 1px solid #e1e4e8; border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem; background: #f8f9fa;">
    
    {% if post.youtubeID %}
    <div class="episode-video" style="margin-bottom: 1rem;">
      <iframe width="100%" height="200" src="https://www.youtube.com/embed/{{ post.youtubeID }}" 
              title="YouTube video player" frameborder="0" 
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
              allowfullscreen style="border-radius: 6px;"></iframe>
    </div>
    {% endif %}
    
    <header class="episode-header">
      <h3 style="margin-bottom: 0.5rem;">
        <a href="{{ post.url | relative_url }}" style="text-decoration: none; color: #0366d6;">
          {{ post.title | escape }}
        </a>
      </h3>
      
      <div class="episode-meta" style="color: #586069; font-size: 0.9rem; margin-bottom: 1rem;">
        <time datetime="{{ post.date | date_to_xmlschema }}">
          {{ post.date | date: site.minima.date_format | default: "%B %-d, %Y" }}
        </time>
        {% if post.episode_number %}
          • Episode #{{ post.episode_number }}
        {% endif %}
        {% if post.guest %}
          • Guest: {{ post.guest }}
        {% endif %}
        {% if post.duration %}
          • {{ post.duration }}
        {% endif %}
      </div>
    </header>
    
    {% if post.excerpt %}
    <div class="episode-excerpt" style="margin-bottom: 1rem;">
      {{ post.excerpt | strip_html | truncatewords: 50 }}
    </div>
    {% endif %}
    
    <div class="episode-actions">
      <a href="{{ post.url | relative_url }}" class="read-more" 
         style="display: inline-block; padding: 0.5rem 1rem; background: #0366d6; color: white; text-decoration: none; border-radius: 4px; font-size: 0.9rem;">
        Read Full Episode →
      </a>
      {% if post.youtubeID %}
      <a href="https://www.youtube.com/watch?v={{ post.youtubeID }}" target="_blank"
         style="display: inline-block; padding: 0.5rem 1rem; background: #ff0000; color: white; text-decoration: none; border-radius: 4px; font-size: 0.9rem; margin-left: 0.5rem;">
        📺 Watch
      </a>
      {% endif %}
    </div>
    
  </article>
{% endfor %}
</div>

---

### Subscribe to stay updated:

- **[🎧 Apple Podcasts](https://podcasts.apple.com/us/podcast/learning-from-machine-learning/id1663925230)**
- **[📺 YouTube Channel](https://www.youtube.com/channel/UCGwSWuvSRzop4ZVG2z9NmnQ?sub_confirmation=1)**
- **[🎙️ RSS Feed](https://media.rss.com/learning-from-machine-learning/feed.xml)**
- **[📝 Substack](https://mindfulmachines.substack.com)** 