import React, { useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

const ChatNew = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      const userMessage = { text: inputValue, sender: 'user' };
      setMessages(prev => [...prev, userMessage]);
      
      const loadingMessage = { text: 'Searching and analyzing information...', sender: 'bot', isLoading: true };
      setMessages(prev => [...prev, loadingMessage]);
      
      const currentQuery = inputValue;
      setInputValue('');
      setIsLoading(true);

      try {
        // Prepare conversation history (exclude the current loading message)
        const conversationHistory = messages.map(msg => ({
          text: msg.text,
          sender: msg.sender
        }));

        const response = await axios.post('http://localhost:5001/api/query', { 
          query: currentQuery,
          conversation_history: conversationHistory
        });
        
        // Extract the summary content from the response
        const aiResponse = response.data.summary || response.data || 'No response received';
        
        // Remove loading message and add properly formatted response
        setMessages(prev => {
          const newMessages = prev.slice(0, -1); // Remove loading message
          return [...newMessages, { 
            text: aiResponse, 
            sender: 'bot',
            sources: response.data.sources || []
          }];
        });
        
      } catch (error) {
        console.error('Error fetching AI response:', error);
        setMessages(prev => {
          const newMessages = prev.slice(0, -1); // Remove loading message
          return [...newMessages, { 
            text: 'Sorry, I encountered an error while processing your request. Please make sure the backend server is running and try again.', 
            sender: 'bot' 
          }];
        });
      } finally {
        setIsLoading(false);
      }
    }
  };

  // Enhanced component to render beautifully formatted message content - ChatGPT Style
  const MessageContent = ({ text, sender }) => {
    if (sender === 'user') {
      return <div className="message-text">{text}</div>;
    }

    // Markdown components for ChatGPT-style rendering
    const components = {
      h1: ({ children }) => <h1 className="chatgpt-h1">{children}</h1>,
      h2: ({ children }) => <h2 className="chatgpt-h2">{children}</h2>,
      h3: ({ children }) => <h3 className="chatgpt-h3">{children}</h3>,
      h4: ({ children }) => <h4 className="chatgpt-h4">{children}</h4>,
      p: ({ children }) => <p className="chatgpt-paragraph">{children}</p>,
      ul: ({ children }) => <ul className="chatgpt-ul">{children}</ul>,
      ol: ({ children }) => <ol className="chatgpt-ol">{children}</ol>,
      li: ({ children }) => <li className="chatgpt-li">{children}</li>,
      table: ({ children }) => (
        <div className="chatgpt-table-wrapper">
          <table className="chatgpt-table">{children}</table>
        </div>
      ),
      thead: ({ children }) => <thead className="chatgpt-thead">{children}</thead>,
      tbody: ({ children }) => <tbody className="chatgpt-tbody">{children}</tbody>,
      tr: ({ children }) => <tr className="chatgpt-tr">{children}</tr>,
      th: ({ children }) => <th className="chatgpt-th">{children}</th>,
      td: ({ children }) => <td className="chatgpt-td">{children}</td>,
      blockquote: ({ children }) => <blockquote className="chatgpt-blockquote">{children}</blockquote>,
      strong: ({ children }) => <strong className="chatgpt-strong">{children}</strong>,
      em: ({ children }) => <em className="chatgpt-em">{children}</em>,
      code: ({ node, inline, className, children, ...props }) => {
        const match = /language-(\w+)/.exec(className || '');
        const language = match ? match[1] : '';
        
        return !inline && language ? (
          <div className="chatgpt-code-block">
            <div className="chatgpt-code-header">
              <span className="chatgpt-code-language">{language}</span>
              <button 
                className="chatgpt-copy-button"
                onClick={() => navigator.clipboard.writeText(String(children).replace(/\n$/, ''))}
              >
                Copy code
              </button>
            </div>
            <SyntaxHighlighter
              style={oneDark}
              language={language}
              PreTag="div"
              className="chatgpt-syntax-highlighter"
              {...props}
            >
              {String(children).replace(/\n$/, '')}
            </SyntaxHighlighter>
          </div>
        ) : (
          <code className="chatgpt-inline-code" {...props}>
            {children}
          </code>
        );
      }
    };

    return (
      <div className="message-text chatgpt-content">
        <ReactMarkdown components={components}>
          {text}
        </ReactMarkdown>
      </div>
    );
  };

  const handleSuggestionClick = (suggestion) => {
    setInputValue(suggestion);
  };

  const handleNewChat = () => {
    setMessages([]);
    setInputValue('');
    setIsLoading(false);
  };

  const suggestions = [
    "Explain quantum computing in simple terms",
    "Got any creative ideas for a 10 year old's birthday?",
    "How do I make an HTTP request in Javascript?",
    "Explain options trading in simple terms"
  ];

  return (
    <>
      {/* Sidebar */}
      <div className="sidebar">
        <div className="sidebar-header" onClick={handleNewChat} style={{ cursor: 'pointer' }}>
          + New chat
        </div>
        <div className="sidebar-content">
          <div className="sidebar-section">
            <div className="sidebar-section-title">Today</div>
            <div className="chat-item active">Personal AI Copilot</div>
          </div>
          <div className="sidebar-section">
            <div className="sidebar-section-title">Previous 7 Days</div>
            <div className="chat-item">Content structuring for project</div>
            <div className="chat-item">Course feedback review</div>
            <div className="chat-item">Email to QwikLabs support</div>
            <div className="chat-item">ChromeDriver setup guide</div>
            <div className="chat-item">Google Cloud journey post</div>
            <div className="chat-item">Microsoft and Google apprentice...</div>
            <div className="chat-item">Cloud Spanner Error Fix</div>
            <div className="chat-item">OCI exam notes structure</div>
            <div className="chat-item">Cloud Function deployment issue</div>
            <div className="chat-item">Fix Translation API Errors</div>
            <div className="chat-item">GenAI hackathon project</div>
            <div className="chat-item">Web scraping health score</div>
            <div className="chat-item">Salary of Apple Technical Specialist...</div>
            <div className="chat-item">Understanding node types</div>
            <div className="chat-item">Mini app definition</div>
            <div className="chat-item">Gen AI hackathon guidance</div>
            <div className="chat-item">Vault permission errors</div>
            <div className="chat-item">Global routing troubleshooting</div>
            <div className="chat-item">GCP Dataflow lab guide</div>
            <div className="chat-item">Create virtual machine</div>
            <div className="chat-item">Mock interview script</div>
            <div className="chat-item">Excel and Google Sheets</div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="main-content">
        <div className="chat-container">
          <div className="messages-container">
            {messages.length === 0 ? (
              <div className="empty-state">
                <h1>What can I help with?</h1>
                <div className="suggestions">
                  {suggestions.map((suggestion, index) => (
                    <div 
                      key={index} 
                      className="suggestion"
                      onClick={() => handleSuggestionClick(suggestion)}
                    >
                      {suggestion}
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              messages.map((message, index) => (
                <div key={index} className="message-wrapper">
                  <div className={`message ${message.sender}`}>
                    <div className="message-content">
                      <div className="message-avatar">
                        {message.sender === 'user' ? 'Y' : 'AI'}
                      </div>
                      <MessageContent text={message.text} sender={message.sender} />
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>

          <div className="input-container">
            <div className="input-wrapper">
              <form onSubmit={handleSubmit} className="input-form">
                <textarea
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Message ChatGPT..."
                  rows="1"
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleSubmit(e);
                    }
                  }}
                />
                <button 
                  type="submit" 
                  className="send-button"
                  disabled={!inputValue.trim()}
                >
                  ↑
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ChatNew;
