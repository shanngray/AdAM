import React from 'react'

interface Message {
  id: number
  sender_name: string
  message: string
  type: string
  timestamp: string
}

interface MessageListProps {
  messages: Message[]
}

const MessageList: React.FC<MessageListProps> = ({ messages }) => {
  return (
    <div className="space-y-4 p-4">
      {messages?.map((message) => (
        <div
          key={message?.id}
          className={`chat ${message?.sender_name === 'User' ? 'chat-end' : 'chat-start'}`}
        >
          <div className="chat-header">
            {message?.sender_name}
            <time className="text-xs opacity-50 ml-1">
              {message?.timestamp && new Date(message.timestamp).toLocaleTimeString()}
            </time>
          </div>
          <div className="chat-bubble">{message?.message}</div>
        </div>
      ))}
    </div>
  )
}

export default MessageList