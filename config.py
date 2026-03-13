import os
import logging

# Configure basic logging for the system
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# API Keys and Secrets
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "your_youtube_api_key_here")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "your_token_here")
INSTAGRAM_BUSINESS_ID = os.getenv("INSTAGRAM_BUSINESS_ID", "your_id_here")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_key_here")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "your_elevenlabs_key_here")

# Scheduling Settings
POSTS_PER_DAY = int(os.getenv("POSTS_PER_DAY", "2"))
TIMEZONE = os.getenv("TIMEZONE", "UTC")

# Content Settings
MAX_VIDEO_DURATION_SECONDS = 30
TARGET_PLATFORMS = ["youtube_shorts", "instagram_reels"]
