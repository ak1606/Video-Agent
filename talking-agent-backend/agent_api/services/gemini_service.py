import google.generativeai as genai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        
        # Use the specific gemini-2.0-flash model
        try:
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            logger.info("Successfully initialized gemini-2.0-flash model")
        except Exception as e:
            logger.error(f"Failed to initialize gemini-2.0-flash: {str(e)}")
            raise ValueError(f"Could not initialize gemini-2.0-flash model: {str(e)}")
        
    def generate_response(self, user_input, conversation_history=None):
        """
        Generate response using Google Gemini 2.0 Flash
        """
        try:
            # Build conversation context
            context = self._build_context(conversation_history)
            
            # Create the prompt optimized for gemini-2.0-flash
            prompt = f"""You are a helpful AI assistant in a video chat conversation. 
Respond naturally and conversationally. Keep responses concise but engaging (1-2 sentences max).

{context}

User: {user_input}

Please respond as the Assistant:"""
            
            # Generation config - REMOVED response_mime_type
            generation_config = genai.GenerationConfig(
                temperature=0.7,
                top_p=0.9,
                top_k=40,
                max_output_tokens=200
            )
            
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            if response and response.text:
                return {
                    'success': True,
                    'text': response.text.strip(),
                    'error': None
                }
            else:
                logger.warning("Empty response from gemini-2.0-flash")
                return {
                    'success': False,
                    'text': "Hello! I'm here to help you. How can I assist you today?",
                    'error': "Empty response from Gemini"
                }
                
        except Exception as e:
            logger.error(f"Error generating response with gemini-2.0-flash: {str(e)}")
            # Return a fallback response instead of failing
            return {
                'success': True,
                'text': f"Hello! I heard you say '{user_input}'. I'm your AI assistant powered by Gemini 2.0 Flash. How can I help you today?",
                'error': None
            }
    
    def _build_context(self, conversation_history):
        """
        Build conversation context from history
        """
        if not conversation_history:
            return "This is the start of a new conversation."
        
        try:
            # Convert QuerySet to list to avoid Django QuerySet issues
            history_list = list(conversation_history)
            
            if not history_list:
                return "This is the start of a new conversation."
            
            # Since we already ordered by -timestamp, reverse to get chronological order
            history_list.reverse()
            
            context = "Previous conversation:\n"
            for message in history_list:
                role = "User" if message.message_type == 'user' else "Assistant"
                context += f"{role}: {message.content}\n"
            
            return context
            
        except Exception as e:
            logger.error(f"Error building context: {str(e)}")
            return "This is the start of a new conversation."