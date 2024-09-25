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
  metaPromptOne: string;
  metaPromptTwo: string;
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
  const [messages, setMessages] = useState<Message[]>([])
  const [localConversation, setLocalConversation] = useState(conversation)

  // Use a ref to store the latest conversation state
  const conversationRef = useRef(conversation)

  // Ref to the end of the messages list for auto-scrolling
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Update local state and ref when the conversation prop changes
  useEffect(() => {
    conversationRef.current = conversation
    setLocalConversation(conversation)
    console.log("ChatWindow: Conversation updated from parent", conversation)
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

    if (ws && localConversation) {
      // Create a new message object and add it to local state
      const newMessage = {
        id: Date.now(),
        sender_name: 'User',
        message: message,
        type: 'outer',
        timestamp: new Date().toISOString()
      };
      setMessages(prevMessages => [...prevMessages, newMessage]);

      // Send the message to the server
      console.log("Preparing to send message:", message);
      console.log("Current conversation state:", localConversation.conversationState);
      
      const sendMessage = JSON.stringify({
        type: localConversation.conversationState,
        conversation_id: localConversation.conversationId,
        content: message,
        sender_name: 'User'
      })
      
      console.log("Sending WebSocket message:", sendMessage);
      ws.send(sendMessage);
      
      console.log("Message sent successfully");
    } else {
      console.log("ChatWindow: Unable to send message - WebSocket or conversation not available")
    }
  }, [ws, localConversation]);

  // Scroll to bottom when messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages])

  // Render the chat window
  return (
    <div className="flex flex-col h-[93vh]"> {/* Change to h-full */}
      {/* Scrollable Messages Container */}
      <div className="flex-1 overflow-y-auto">
        <MessageList messages={messages} />
        <div ref={messagesEndRef} />
      </div>
      
      {/* Fixed Message Input */}
      {localConversation ? (
        <div className="mt-auto">
          <MessageInput 
            conversation={localConversation}
            onSendMessage={handleMessageSent}
          />
        </div>
      ) : (
        <p className="p-4 mt-auto">Loading conversation...</p>
      )}
    </div>
  )
}

export default ChatWindow