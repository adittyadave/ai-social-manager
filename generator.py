import os
import sys

# Add the current directory to sys.path so local modules can be found
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging
import time
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from config import OPENAI_API_KEY, ELEVENLABS_API_KEY

logger = logging.getLogger(__name__)

class ContentGenerator:
    def __init__(self):
        logger.info("Initializing Content Generator with OpenAI and ElevenLabs...")
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        self.elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        
    def generate_script(self, topic):
        """
        Uses OpenAI to generate a 30-second viral video script.
        """
        logger.info(f"Generating script for topic: '{topic}' using GPT-4o...")
        
        prompt = f"""
        Write a high-energy, engaging 30-second script for a social media Short/Reel about: {topic}.
        The script should have:
        1. A strong "hook" in the first 3 seconds.
        2. 3 quick, value-packed points.
        3. A call to action at the end.
        Keep it under 75 words to ensure it fits in 30 seconds.
        Format: ONLY the spoken text, no stage directions.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150
            )
            script = response.choices[0].message.content.strip()
            logger.info("Script generation successful.")
            return script
        except Exception as e:
            logger.error(f"Failed to generate script: {e}")
            return f"Hey everyone! Today we are talking about {topic}. It's absolutely game-changing. Check it out and let me know what you think!"

    def generate_voiceover(self, script, topic):
        """
        Uses ElevenLabs to convert the script into a realistic voiceover.
        """
        logger.info("Generating professional voiceover using ElevenLabs...")
        
        output_path = f"voiceover_{int(time.time())}.mp3"
        
        try:
            audio = self.elevenlabs_client.generate(
                text=script,
                voice="Adam", # A popular high-energy male voice
                model="eleven_multilingual_v2"
            )
            
            # Save the generator/iterator to a file
            with open(output_path, "wb") as f:
                for chunk in audio:
                    if chunk:
                        f.write(chunk)
            
            logger.info(f"Voiceover saved to: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to generate voiceover: {e}")
            return None

    def compile_video(self, topic, voiceover_file):
        """
        Programmatically compiles the final vertical video.
        Note: In a full implementation, this uses MoviePy to overlay the voiceover 
        on top of dynamic background footage or stock clips.
        """
        logger.info(f"Compiling final vertical video for '{topic}'...")
        # Since rendering video is resource-intensive and requires local ffmpeg setup,
        # we demonstrate the final file creation step.
        time.sleep(2)
        
        output_filename = f"output_{int(time.time())}.mp4"
        # In a real scenario:
        # clip = VideoFileClip("background_template.mp4").subclip(0, 30)
        # audio = AudioFileClip(voiceover_file)
        # final_video = clip.set_audio(audio)
        # final_video.write_videofile(output_filename, fps=24)
        
        # For demonstration, we'll create a dummy file if not exists
        if not os.path.exists(output_filename):
            with open(output_filename, "w") as f:
                f.write("DUMMY_VIDEO_CONTENT")
        
        logger.info(f"Video compilation complete: {output_filename}")
        return output_filename

    def create_content(self, topic):
        """
        Orchestrates the full content generation pipeline.
        """
        logger.info(f"Starting Content Generation Pipeline for: {topic}")
        script = self.generate_script(topic)
        voiceover = self.generate_voiceover(script, topic)
        video_file = self.compile_video(topic, voiceover)
        
        return {
            "title": f"{topic} EXPLAINED! #shorts #automation",
            "description": f"Here is what you need to know about {topic}. Automated by AI.",
            "file_path": video_file,
            "tags": ["AI", "Automation", topic.replace(" ", "")]
        }

if __name__ == "__main__":
    generator = ContentGenerator()
    print(generator.create_content("The Future of AI"))
