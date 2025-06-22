import React, { useState, useRef, useEffect } from 'react';
import VoiceInput from './VoiceInput';
import VideoPlayer from './VideoPlayer';
import ChatInterface from './ChatInterface';
import './TalkingAgent.css';

const TalkingAgent = () => {
  const [messages, setMessages] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentVideoUrl, setCurrentVideoUrl] = useState(null);
  const [sessionId] = useState(() => {
    let id = localStorage.getItem('talkingAgentSessionId');
    if (!id) {
      id = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
      localStorage.setItem('talkingAgentSessionId', id);
    }
    return id;
  });

  const addMessage = (text, type) => {
    setMessages(prev => [...prev, {
      id: Date.now(),
      text,
      type,
      timestamp: new Date().toLocaleTimeString()
    }]);
  };

  const callBackendAPI = async (transcript, sessionId) => {
    const response = await fetch('http://localhost:8000/api/process-voice/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        transcript: transcript,
        session_id: sessionId
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  };

  const handleVoiceInput = async (transcript) => {
    if (!transcript.trim()) return;

    addMessage(transcript, 'user');
    setIsProcessing(true);

    try {
      const response = await callBackendAPI(transcript, sessionId);
      
      addMessage(response.agent_response, 'agent');
      
      if (response.video_generation_success && response.video_url) {
        setCurrentVideoUrl(response.video_url);
      } else if (response.video_error) {
        console.warn('Video generation failed:', response.video_error);
        // Still show the text response even if video fails
      }
      
    } catch (error) {
      console.error('Error processing voice input:', error);
      addMessage('Sorry, I encountered an error. Please try again.', 'agent');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="talking-agent">
      <div className="talking-agent__container">
        <div className="talking-agent__video-section">
          <VideoPlayer 
            videoUrl={currentVideoUrl} 
            isProcessing={isProcessing}
          />
        </div>
        
        <div className="talking-agent__chat-section">
          <ChatInterface messages={messages} isProcessing={isProcessing} />
          <VoiceInput 
            onVoiceInput={handleVoiceInput}
            disabled={isProcessing}
          />
        </div>
      </div>
    </div>
  );
};

export default TalkingAgent;