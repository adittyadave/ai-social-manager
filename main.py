import os
import sys

# Add the current directory to sys.path so modules can be found
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import time
import logging
import schedule

from config import POSTS_PER_DAY
from researcher import TrendResearcher
from generator import ContentGenerator
from publisher import Publisher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SocialMediaAutomator")

def run_automation_cycle():
    """
    Executes a single end-to-end cycle of the automation system.
    Research -> Generate -> Publish
    """
    logger.info("========================================")
    logger.info("Starting new automation cycle...")
    
    # 1. Research
    researcher = TrendResearcher()
    trending_topic = researcher.fetch_current_trends()
    
    # 2. Generate Content
    generator = ContentGenerator()
    video_data = generator.create_content(trending_topic)
    
    # 3. Publish
    publisher = Publisher()
    results = publisher.distribute_content(video_data)
    
    logger.info("Cycle complete! Published URLs:")
    for platform, url in results.items():
        logger.info(f" - {platform}: {url}")
    logger.info("========================================")

def start_scheduler():
    logger.info(f"Starting 24/7 Scheduler. Target frequency: {POSTS_PER_DAY} posts per day.")
    
    # Calculate intervals based on posts per day
    # Example: 2 posts per day = every 12 hours
    hours_between_posts = max(1, 24 // POSTS_PER_DAY)
    
    schedule.every(hours_between_posts).hours.do(run_automation_cycle)
    
    # Run once immediately on startup for demonstration
    run_automation_cycle()
    
    while True:
        schedule.run_pending()
        time.sleep(60) # Wait one minute before checking schedule again

if __name__ == "__main__":
    try:
        start_scheduler()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped manually.")
