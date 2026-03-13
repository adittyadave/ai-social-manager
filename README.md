# AI Social Media Manager

A fully automated, 24/7 social media management system for YouTube Shorts and Instagram Reels.

## Overview
This system is designed to independently manage social media accounts by:
1. **Researching** trending topics and formats across platforms.
2. **Generating** 30-second vertical videos utilizing AI (LLMs, TTS, and programmatic editing).
3. **Publishing** the finalized content to YouTube Shorts and Instagram Reels.

## File Structure

- `main.py`: The central orchestrator running a continuous schedule.
- `config.py`: Centralized configuration and API key setup.
- `researcher.py`: Analyzes social trends to pick relevant topics (concept).
- `generator.py`: Creates the script, audio, and compiles the video (concept).
- `publisher.py`: Uploads to YouTube and Instagram APIs (concept).

## Installation

1. Clone or clone the source files into a directory (`scratch/ai_social_manager`).
2. Install Python >= 3.9
3. Install required libraries:
   \`\`\`bash
   pip install schedule
   \`\`\`
   *(Note: A full implementation would require `openai`, `google-api-python-client`, etc.)*

## Configuration
Set the following environment variables (or modify `config.py`):
- `YOUTUBE_API_KEY`
- `INSTAGRAM_API_KEY`
- `OPENAI_API_KEY`
- `POSTS_PER_DAY` (Default: 2)

## Running the System
To start the 24/7 automated loop, simply run:
\`\`\`bash
python main.py
\`\`\`
The application will immediately perform one cycle and then schedule subsequent cycles based on your configured `POSTS_PER_DAY`.
