import React, { useState, useRef, useEffect } from 'react';
import { Mic, MicOff, Volume2 } from 'lucide-react';
import './VoiceInput.css';

const VoiceInput = ({ onVoiceInput, disabled }) => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState('');
  const recognitionRef = useRef(null);

  useEffect(() => {
    // Check if Web Speech API is supported
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      setError('Speech recognition not supported in this browser');
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognitionRef.current = new SpeechRecognition();
    
    const recognition = recognitionRef.current;
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
      setIsListening(true);
      setError('');
    };

    recognition.onresult = (event) => {
      let interimTranscript = '';
      let finalTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript;
        } else {
          interimTranscript += transcript;
        }
      }

      setTranscript(finalTranscript || interimTranscript);

      if (finalTranscript) {
        onVoiceInput(finalTranscript);
        setTranscript('');
      }
    };

    recognition.onerror = (event) => {
      setError(`Speech recognition error: ${event.error}`);
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    return () => {
      if (recognition) {
        recognition.stop();
      }
    };
  }, [onVoiceInput]);

  const startListening = () => {
    if (recognitionRef.current && !isListening) {
      recognitionRef.current.start();
    }
  };

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop();
    }
  };

  const toggleListening = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  };

  return (
    <div className="voice-input">
      <div className="voice-input__controls">
        <button
          className={`voice-input__mic-button ${isListening ? 'listening' : ''}`}
          onClick={toggleListening}
          disabled={disabled || !!error}
          title={isListening ? 'Stop recording' : 'Start recording'}
        >
          {isListening ? <MicOff size={24} /> : <Mic size={24} />}
        </button>
        
        {isListening && (
          <div className="voice-input__status">
            <Volume2 size={16} />
            <span>Listening...</span>
          </div>
        )}
      </div>

      {transcript && (
        <div className="voice-input__transcript">
          <p>{transcript}</p>
        </div>
      )}

      {error && (
        <div className="voice-input__error">
          <p>{error}</p>
        </div>
      )}
    </div>
  );
};

export default VoiceInput;