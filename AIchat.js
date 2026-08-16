import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const AIChat = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { sender: 'ai', text: "Assalamu Alaikum! I'm Murad's AI Assistant. How can I help you today?" }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: 'user', text: input };
    setMessages([...messages, userMessage]);
    setInput('');
    setIsTyping(true);

    try {
      const response = await axios.post(`${API_URL}/ai/chat`, { message: input });
      const aiMessage = { sender: 'ai', text: response.data.response };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      // Fallback AI response
      const fallbackResponse = getFallbackResponse(input);
      const aiMessage = { sender: 'ai', text: fallbackResponse };
      setMessages(prev => [...prev, aiMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const getFallbackResponse = (message) => {
    const msg = message.toLowerCase();
    if (msg.includes('salam') || msg.includes('hello')) {
      return "Wa Alaikum Assalam! How can I help you with your studies?";
    }
    if (msg.includes('study')) {
      return "Study tips: Break sessions into 25-minute blocks, review regularly, and stay consistent!";
    }
    if (msg.includes('motivat')) {
      return "You have the power to achieve greatness. Keep pushing forward!";
    }
    return "That's interesting! Could you please be more specific about your question?";
  };

  return (
    <div className="ai-chat-widget">
      {isOpen && (
        <div className="ai-chat-window">
          <div className="ai-chat-header">
            <h6>Murad's AI Assistant</h6>
            <button onClick={() => setIsOpen(false)}>×</button>
          </div>
          <div className="ai-chat-messages">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.sender}-message`}>
                {msg.text}
              </div>
            ))}
            {isTyping && (
              <div className="message ai-message typing">
                Typing...
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <div className="ai-chat-input">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Ask me anything..."
            />
            <button onClick={sendMessage}>Send</button>
          </div>
        </div>
      )}
      <button className="ai-chat-button" onClick={() => setIsOpen(!isOpen)}>
        🤖
      </button>
    </div>
  );
};

export default AIChat;
