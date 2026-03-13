import logging
import time
import os
import sys

# Add the current directory to sys.path so modules can be found
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pickle
import requests
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from config import INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_BUSINESS_ID

logger = logging.getLogger(__name__)

# The SCOPES for YouTube Data API. 'youtube.upload' is needed for uploading videos.
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

class Publisher:
    def __init__(self):
        logger.info("Initializing Publisher module...")
        self.youtube = self._authenticate_youtube()

    def _authenticate_youtube(self):
        """
        Handles the OAuth2 authentication flow for YouTube.
        Saves/loads credentials using token.pickle.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Refreshing YouTube access token...")
                creds.refresh(Request())
            else:
                logger.info("No valid tokens found. Starting manual OAuth2 flow...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('youtube', 'v3', credentials=creds)

    def publish_to_youtube_shorts(self, video_data):
        """
        Uploads a video to YouTube using the Data API.
        """
        logger.info(f"Uploading '{video_data['title']}' to YouTube Shorts...")
        
        body = {
            'snippet': {
                'title': video_data['title'],
                'description': video_data['description'],
                'tags': video_data['tags'],
                'categoryId': '22' # 'People & Blogs' category
            },
            'status': {
                'privacyStatus': 'unlisted', # Start as unlisted for safety
                'selfDeclaredMadeForKids': False
            }
        }

        # Call the API's videos.insert method to create and upload the video.
        media = MediaFileUpload(video_data['file_path'], chunksize=-1, resumable=True)
        
        request = self.youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                logger.info(f"Upload progress: {int(status.progress() * 100)}%")

        video_id = response.get('id')
        logger.info(f"Successfully published to YouTube Shorts! Video ID: {video_id}")
        return f"https://youtube.com/shorts/{video_id}"

    def publish_to_instagram_reels(self, video_data):
        """
        Uploads a video to Instagram Reels using the Graph API.
        Note: The video must be accessible via a public URL for Instagram to fetch it.
        """

        if INSTAGRAM_BUSINESS_ID == "your_instagram_business_id_here":
            logger.error("Instagram Business ID not configured! Skipping upload.")
            return None

        logger.info(f"Starting Instagram Reels upload for '{video_data['title']}'...")
        
        # 1. Create Media Container
        # IMPORTANT: video_url MUST be a publicly accessible URL (ngrok, S3, etc.)
        # For now, we assume the video_data contains a public URL if available, 
        # or we log that hosting is required.
        video_url = video_data.get('public_url') 
        if not video_url:
            logger.warning("No public video URL found. Instagram requires a public URL to fetch the video file.")
            logger.info("Simulation: If this were production, we would upload the local file to a temp host first.")
            return "https://instagram.com/reels/simulated_upload_pending_host"

        container_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_BUSINESS_ID}/media"
        payload = {
            'media_type': 'REELS',
            'video_url': video_url,
            'caption': f"{video_data['title']}\n\n{video_data['description']}\n{' '.join(['#'+t for t in video_data['tags']])}",
            'access_token': INSTAGRAM_ACCESS_TOKEN
        }

        try:
            response = requests.post(container_url, data=payload).json()
            container_id = response.get('id')
            if not container_id:
                logger.error(f"Failed to create Instagram container: {response}")
                return None

            # 2. Wait for Container Processing
            logger.info(f"Container created (ID: {container_id}). Waiting for processing...")
            status_url = f"https://graph.facebook.com/v19.0/{container_id}"
            params = {'fields': 'status_code', 'access_token': INSTAGRAM_ACCESS_TOKEN}
            
            for _ in range(10): # Poll for up to ~2 minutes
                time.sleep(15)
                status_response = requests.get(status_url, params=params).json()
                status = status_response.get('status_code')
                logger.info(f"Current container status: {status}")
                if status == 'FINISHED':
                    break
                elif status == 'ERROR':
                    logger.error(f"Instagram container processing failed: {status_response}")
                    return None
            else:
                logger.error("Instagram container processing timed out.")
                return None

            # 3. Publish Media
            logger.info("Publishing container to Reels...")
            publish_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_BUSINESS_ID}/media_publish"
            publish_payload = {
                'creation_id': container_id,
                'access_token': INSTAGRAM_ACCESS_TOKEN
            }
            publish_response = requests.post(publish_url, data=publish_payload).json()
            media_id = publish_response.get('id')
            
            if media_id:
                logger.info(f"Successfully published to Instagram Reels! Media ID: {media_id}")
                return f"https://www.instagram.com/reels/{media_id}/"
            else:
                logger.error(f"Failed to publish Instagram media: {publish_response}")
                return None

        except Exception as e:
            logger.error(f"Instagram publishing error: {e}")
            return None

    def distribute_content(self, video_data):
        """
        Publishes the generated video to all configured platforms.
        """
        logger.info("Starting distribution process...")
        results = {}
        
        try:
            yt_url = self.publish_to_youtube_shorts(video_data)
            results['youtube'] = yt_url
        except Exception as e:
            logger.error(f"Failed to publish to YouTube: {e}")

        try:
            ig_url = self.publish_to_instagram_reels(video_data)
            if ig_url:
                results['instagram'] = str(ig_url)
        except Exception as e:
            logger.error(f"Failed to publish to Instagram: {e}")
            
        return results

if __name__ == "__main__":
    # Note: Running this directly requires a 'test.mp4' file to exist.
    pub = Publisher()
    dummy_data = {
        "title": "Test Video", 
        "description": "Test", 
        "file_path": "test.mp4", 
        "tags": ["test"]
    }
    print(pub.distribute_content(dummy_data))
