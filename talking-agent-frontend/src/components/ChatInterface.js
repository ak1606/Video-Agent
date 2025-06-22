import React, { useRef, useEffect } from 'react';
import { User, Bot, Loader } from 'lucide-react';
import './ChatInterface.css';

const ChatInterface = ({ messages, isProcessing }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="chat-interface">
      <div className="chat-interface__header">
        <h3>Conversation</h3>
      </div>
      
      <div className="chat-interface__messages">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`chat-message ${message.type === 'user' ? 'user' : 'agent'}`}
          >
            <div className="chat-message__avatar">
              {message.type === 'user' ? <User size={20} /> : <Bot size={20} />}
            </div>
            <div className="chat-message__content">
              <div className="chat-message__text">{message.text}</div>
              <div className="chat-message__timestamp">{message.timestamp}</div>
            </div>
          </div>
        ))}
        
        {isProcessing && (
          <div className="chat-message agent">
            <div className="chat-message__avatar">
              <Bot size={20} />
            </div>
            <div className="chat-message__content">
              <div className="chat-message__text">
                <Loader className="spinner" size={16} />
                Processing...
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default ChatInterface;