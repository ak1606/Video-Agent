import requests
import json
import time
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class DIDService:
    def __init__(self):
        if not settings.DID_API_KEY:
            raise ValueError("DID_API_KEY not found in environment variables")
        
        self.api_key = settings.DID_API_KEY
        self.base_url = settings.DID_BASE_URL
        
        # Use Basic auth (method that worked)
        self.headers = {
            'Authorization': f'Basic {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Use direct image URLs that end with proper extensions
        self.default_avatar = "https://raw.githubusercontent.com/Asit0011/DID/main/avatar.jpg"
        
        # Backup avatars with proper extensions
        self.backup_avatars = [
            "https://thispersondoesnotexist.com/image.jpeg",
            "https://randomuser.me/api/portraits/men/1.jpg",
            "https://randomuser.me/api/portraits/women/1.jpg",
            "https://randomuser.me/api/portraits/men/2.jpg",
            "https://randomuser.me/api/portraits/women/2.jpg",
            "https://randomuser.me/api/portraits/men/3.jpg",
            "https://randomuser.me/api/portraits/women/3.jpg",
            # Static reliable images
            "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&w=400",
            "https://images.pexels.com/photos/614810/pexels-photo-614810.jpeg?auto=compress&cs=tinysrgb&w=400"
        ]
    
    def create_talking_video(self, text, avatar_url=None):
        """
        Create a talking video using D-ID API with proper image URLs
        """
        try:
            # Use default avatar if none provided
            if not avatar_url:
                avatar_url = self.default_avatar
            
            # Try creating video with primary avatar
            result = self._attempt_video_creation(text, avatar_url)
            
            # If any error, try backup avatars
            if not result['success']:
                logger.warning(f"Primary avatar failed ({result.get('error')}), trying backup avatars...")
                
                for i, backup_avatar in enumerate(self.backup_avatars):
                    logger.info(f"Trying backup avatar {i+1}: {backup_avatar}")
                    result = self._attempt_video_creation(text, backup_avatar)
                    
                    if result['success']:
                        logger.info(f"Success with backup avatar {i+1}: {backup_avatar}")
                        break
                    else:
                        logger.warning(f"Backup avatar {i+1} failed: {result.get('error')}")
                        # Continue to next backup
            
            return result
                
        except Exception as e:
            logger.error(f"Error in create_talking_video: {str(e)}")
            return {
                'success': False,
                'video_url': None,
                'error': str(e)
            }
    
    def _attempt_video_creation(self, text, avatar_url):
        """
        Attempt to create video with specific avatar
        """
        try:
            # Prepare the request payload - minimal configuration
            payload = {
                "source_url": avatar_url,
                "script": {
                    "type": "text",
                    "input": text[:150]  # Keep text very short
                }
            }
            
            logger.info(f"Attempting video creation with: {avatar_url}")
            logger.info(f"Text length: {len(text)} chars")
            
            # Create the talk
            response = requests.post(
                f"{self.base_url}/talks",
                headers=self.headers,
                json=payload,
                timeout=20
            )
            
            logger.info(f"D-ID response status: {response.status_code}")
            logger.info(f"D-ID response: {response.text}")
            
            if response.status_code == 201:
                talk_data = response.json()
                talk_id = talk_data.get('id')
                
                if talk_id:
                    logger.info(f"Talk created successfully with ID: {talk_id}")
                    # Poll for video completion
                    video_url = self._wait_for_video_completion(talk_id)
                    if video_url:
                        return {
                            'success': True,
                            'video_url': video_url,
                            'talk_id': talk_id,
                            'error': None
                        }
                    else:
                        return {
                            'success': False,
                            'video_url': None,
                            'error': 'Video generation timed out'
                        }
                else:
                    return {
                        'success': False,
                        'video_url': None,
                        'error': 'No talk ID returned'
                    }
            else:
                error_text = response.text
                logger.error(f"Talk creation failed: {response.status_code} - {error_text}")
                return {
                    'success': False,
                    'video_url': None,
                    'error': f'D-ID API error: {response.status_code} - {error_text}'
                }
                
        except requests.exceptions.Timeout:
            logger.error("D-ID API request timed out")
            return {
                'success': False,
                'video_url': None,
                'error': 'D-ID API request timed out'
            }
        except Exception as e:
            logger.error(f"Error in _attempt_video_creation: {str(e)}")
            return {
                'success': False,
                'video_url': None,
                'error': str(e)
            }
    
    def _wait_for_video_completion(self, talk_id, max_wait=60):
        """
        Poll D-ID API until video is ready
        """
        start_time = time.time()
        poll_count = 0
        
        while time.time() - start_time < max_wait:
            try:
                poll_count += 1
                response = requests.get(
                    f"{self.base_url}/talks/{talk_id}",
                    headers=self.headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    status = data.get('status')
                    
                    logger.info(f"D-ID status check {poll_count}: {status}")
                    
                    if status == 'done':
                        result_url = data.get('result_url')
                        logger.info(f"✅ D-ID video completed: {result_url}")
                        return result_url
                    elif status == 'error':
                        logger.error(f"❌ D-ID video generation failed: {data}")
                        return None
                    elif status in ['created', 'started']:
                        logger.info(f"⏳ Video still processing... (attempt {poll_count})")
                        time.sleep(3)
                        continue
                    else:
                        logger.warning(f"Unknown status: {status}")
                        time.sleep(3)
                        continue
                else:
                    logger.error(f"Error checking D-ID status: {response.status_code}")
                    return None
                    
            except Exception as e:
                logger.error(f"Error polling D-ID status: {str(e)}")
                return None
        
        logger.error(f"❌ D-ID video generation timed out after {max_wait} seconds")
        return None
    
    def get_credits(self):
        """
        Check remaining D-ID credits
        """
        try:
            response = requests.get(
                f"{self.base_url}/credits",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f'Status {response.status_code}: {response.text}'}
                
        except Exception as e:
            logger.error(f"Error checking D-ID credits: {str(e)}")
            return {'error': str(e)}