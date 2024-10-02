import React, { useEffect, useState, useCallback, useRef } from 'react'
import MessageList from './MessageList'
import MessageInput from './MessageInput'

// Define types for messages and conversations
interface Message {
  id: number
  sender_name: string
  message: string
  type: string
  timestamp: string
}

interface Conversation {
  conversationId: number;
  conversationName: string;
  conversationState: string;
  subject: string;
  rewrittenPrompt: string;
}

interface ChatWindowProps {
  conversation: Conversation | null
  ws: WebSocket | null
  onConversationChange: (conversation: Conversation) => void
}

const ChatWindow: React.FC<ChatWindowProps> = ({ 
  conversation, 
  ws,
  onConversationChange
}) => {
  const [localConversation, setLocalConversation] = useState<Conversation | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    setLocalConversation(conversation)
    if (conversation?.conversationState === 'new') {
      setMessages([])
    }
  }, [conversation])

  // Set up WebSocket event listener and request conversation history
  useEffect(() => {
    console.log("ChatWindow: Setting up WebSocket listener")

    if (ws && localConversation && ws.readyState === WebSocket.OPEN) {
      const handleMessage = (event: MessageEvent) => {
        const data = JSON.parse(event.data)
        console.log("ChatWindow: Received WebSocket message", data.type)

        switch (data.type) {
          case 'conversation_history':
            setMessages(data.data)
            break
          case 'new_message':
            const newMessage: Message = {
              id: Date.now(),
              sender_name: data.sender_name,
              message: data.message,
              type: data.type,
              timestamp: new Date().toISOString()
            }
            setMessages(prevMessages => [...prevMessages, newMessage])
            break
          case 'new_conversation':
            if (data.data.initialMessage) {
              const initialMessage: Message = {
                id: data.data.initialMessage.id,
                sender_name: data.data.initialMessage.sender_name,
                message: data.data.initialMessage.message,
                type: data.data.initialMessage.type,
                timestamp: new Date().toISOString()
              }
              setMessages([initialMessage])
            }
            break
          case 'conversation_updated':
            if (localConversation && localConversation.conversationId === data.conversation_id) {
              const updatedConversation = {
                ...localConversation,
                ...data.updated_fields,
              };
              console.log("ChatWindow: Updating conversation", updatedConversation)
              setLocalConversation(updatedConversation);
              onConversationChange(updatedConversation);
            }
            break
          default:
            console.log("ChatWindow: Unhandled message type", data.type)
        }
      };

      ws.addEventListener('message', handleMessage)

      // Request conversation history from the server
      // TODO: This only needs to be called when a new conversation is selected
      const getConversationHistory = () => {
        const message = JSON.stringify({
          type: 'get_conversation_history',
          conversation_id: localConversation.conversationId
        })
        console.log("ChatWindow: Requesting conversation history")
        ws.send(message)
      }

      getConversationHistory()

      // Clean up event listener when component unmounts or dependencies change
      return () => {
        ws.removeEventListener('message', handleMessage)
      };
    }
  }, [ws, localConversation, onConversationChange])

  // Handler for sending messages
  const handleMessageSent = useCallback((message: string) => {
    if (!localConversation || !ws) return;

    const newMessage: Message = {
      id: Date.now(),
      sender_name: 'User',
      message: message,
      type: 'text',
      timestamp: new Date().toISOString()
    };

    setMessages(prevMessages => [...prevMessages, newMessage]);

    let messageType: string;
    if (localConversation.conversationState === 'new') {
      messageType = 'create_conversation';
    } else if (localConversation.conversationState === 'meta_agent_input') {
      messageType = 'meta_agent_input';
    } else {
      messageType = localConversation.conversationState;
    }

    ws.send(JSON.stringify({
      type: messageType,
      conversation_id: localConversation.conversationId,
      content: message,
      sender_name: 'User'
    }));
  }, [ws, localConversation]);

  // Scroll to bottom when messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages])

  // Render the chat window
  return (
    <div className="flex flex-col h-[93vh]">
      {/* Scrollable Messages Container */}
      <div className="flex-1 overflow-y-auto">
        <MessageList messages={messages} />
        <div ref={messagesEndRef} />
      </div>
      
      {/* Always render MessageInput */}
      <div className="mt-auto">
        <MessageInput 
          conversation={localConversation}
          onSendMessage={handleMessageSent}
        />
      </div>
    </div>
  )
}

export default ChatWindow