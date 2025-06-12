from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import uuid
import logging

from .models import Conversation, Message
from .services.gemini_service import GeminiService
from .services.did_service import DIDService

logger = logging.getLogger(__name__)

class ProcessVoiceView(APIView):
    def post(self, request):
        """
        Process voice input and return agent response with video
        """
        try:
            # Get data from request
            transcript = request.data.get('transcript', '').strip()
            session_id = request.data.get('session_id', str(uuid.uuid4()))
            
            if not transcript:
                return Response({
                    'error': 'No transcript provided'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get or create conversation
            conversation, created = Conversation.objects.get_or_create(
                session_id=session_id
            )
            
            # Save user message
            user_message = Message.objects.create(
                conversation=conversation,
                content=transcript,
                message_type='user'
            )
            
            # Get conversation history
            all_messages = Message.objects.filter(conversation=conversation).exclude(id=user_message.id)
            conversation_history = all_messages.order_by('-timestamp')[:5]
            
            # Generate AI response
            try:
                gemini_service = GeminiService()
                ai_response = gemini_service.generate_response(
                    transcript, 
                    conversation_history
                )
                
                if ai_response['success']:
                    response_text = ai_response['text']
                else:
                    response_text = f"Hello! I heard you say '{transcript}'. How can I help you today?"
                    
            except Exception as e:
                logger.error(f"Gemini service failed: {str(e)}")
                response_text = f"Hello! I heard you say '{transcript}'. I'm your AI assistant. How can I help you today?"
            
            # Try D-ID video generation
            video_url = None
            video_error = None
            
            try:
                did_service = DIDService()
                video_result = did_service.create_talking_video(response_text)
                
                if video_result['success']:
                    video_url = video_result['video_url']
                else:
                    video_error = video_result.get('error', 'Video generation failed')
                    
            except Exception as e:
                logger.error(f"D-ID service failed: {str(e)}")
                video_error = f"Video service error: {str(e)}"
            
            # Save agent message
            agent_message = Message.objects.create(
                conversation=conversation,
                content=response_text,
                message_type='agent',
                video_url=video_url
            )
            
            # Return response
            response_data = {
                'session_id': session_id,
                'agent_response': response_text,
                'video_url': video_url,
                'video_generation_success': video_url is not None,
                'timestamp': timezone.now().isoformat()
            }
            
            if video_error:
                response_data['video_error'] = video_error
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error processing voice input: {str(e)}")
            return Response({
                'error': f'Server error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HealthCheckView(APIView):
    def get(self, request):
        """
        Health check endpoint
        """
        return Response({
            'status': 'healthy',
            'timestamp': timezone.now().isoformat()
        })

class CheckCreditsView(APIView):
    def get(self, request):
        """
        Check D-ID credits
        """
        try:
            did_service = DIDService()
            credits = did_service.get_credits()
            
            return Response({
                'credits': credits,
                'timestamp': timezone.now().isoformat()
            })
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)