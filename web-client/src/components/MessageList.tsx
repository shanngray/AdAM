import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface Message {
  id: number;
  sender_name: string;
  message: string;
  type: string;
  timestamp: string;
}

interface MessageListProps {
  messages: Message[];
}

const MessageList: React.FC<MessageListProps> = ({ messages }) => {
  return (
    <div className="flex flex-col space-y-4">
      {messages?.map((message) => (
        <div
          key={message.id}
          className={`chat ${message.sender_name === 'User' ? 'chat-end' : 'chat-start'}`}
        >
          <div className="chat-header">
            {message.sender_name}
            <time className="text-xs opacity-50 ml-1">
              {message.timestamp && new Date(message.timestamp).toLocaleTimeString()}
            </time>
          </div>
          <div className="chat-bubble">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {message.message}
            </ReactMarkdown>
          </div>
        </div>
      ))}
    </div>
  );
};

export default MessageList;