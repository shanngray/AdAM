import { useState, useEffect, useCallback } from 'react'
import ChatWindow from '../components/ChatWindow'
import ConversationList from '../components/ConversationList'
import SecondaryWindow from '../components/SecondaryWindow'

// Define types for conversations and messages
interface Conversation {
  conversationId: number;
  conversationName: string;
  conversationState: string;
  subject: string;
  rewrittenPrompt: string;
  metaPromptOne: string;
  metaPromptTwo: string;
}

interface Message {
  id: number;
  content: string;
  sender: string;
  conversation_id: string;
  sender_name: string;
  type: string;
}

export default function Home() {
  // State management for the main components
  const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null)
  const [isSecondaryWindowOpen, setIsSecondaryWindowOpen] = useState(false)
  const [ws, setWs] = useState<WebSocket | null>(null)

  // Function to set up WebSocket connection
  const setupWebSocket = useCallback(() => {
    console.log("Home: Setting up WebSocket connection...")
    const socket = new WebSocket("ws://localhost:8080/server/ws")
    setWs(socket)

    socket.onopen = () => {
      console.log("Home: WebSocket connected successfully")
      // Request the latest conversation when the connection is established
      const message = JSON.stringify({ type: 'get_latest_conversation' })
      console.log("Home: Sending message to server:", message)
      socket.send(message)
    }

    socket.onclose = (event) => {
      console.log("Home: WebSocket disconnected", event)
      // Attempt to reconnect after a delay
      setTimeout(setupWebSocket, 5000)
    }

    socket.onerror = (error) => {
      console.error("Home: WebSocket error:", error)
    }

    socket.onmessage = (event) => {
      console.log("Home: Received message from server:", event.data)
      try {
        const data = JSON.parse(event.data)
        if (data.type === 'latest_conversation' || data.type === 'conversation_updated') {
          console.log("Home: Updating selected conversation", data.data)
          setSelectedConversation(prevConversation => ({
            ...prevConversation,
            ...data.data,
          }))
        } else {
          // TODO: work out why this keeps firing
          //console.log("Home: Unhandled message type:", data.type)
        }
      } catch (error) {
        console.error("Home: Error parsing message:", error)
      }
    }

    return () => {
      console.log("Home: Cleaning up WebSocket connection")
      socket.close()
    }
  }, [])

  // Set up WebSocket connection on component mount
  useEffect(() => {
    const cleanup = setupWebSocket()
    return cleanup
  }, [setupWebSocket])

  // Handler for selecting a conversation
  const handleSelectConversation = (conversation: Conversation) => {
    console.log("Home: Conversation selected", conversation)
    setSelectedConversation(conversation)
  }

  // Handler for creating a new conversation
  const handleNewConversation = (newConversation: Conversation) => {
    console.log("Home: New conversation created", newConversation)
    setSelectedConversation(newConversation)
  }

  // Handler for updating the selected conversation
  const handleConversationChange = (conversation: Conversation) => {
    console.log("Home: Conversation updated", conversation)
    setSelectedConversation(conversation);
  };

  // Effect to handle WebSocket messages related to conversation updates
  useEffect(() => {
    if (!ws) return;

    const handleWebSocketMessage = (event: MessageEvent) => {
      // console.log("Home: Received WebSocket message:", event.data);
      try {
        const data = JSON.parse(event.data);

        if (data.type === 'conversation_updated') {
          if (selectedConversation && selectedConversation.conversationId === data.conversation_id) {
            console.log("Home: Updating selected conversation", data.updated_fields)
            setSelectedConversation({
              ...selectedConversation,
              ...data.updated_fields,
            });
          }
        } else if (data.type === 'latest_conversation') {
          console.log("Home: Setting latest conversation", data.data);
          setSelectedConversation(data.data);
        } else {
          console.log("Home: Unhandled WebSocket message type:", data.type);
        }
      } catch (error) {
        console.error("Home: Error parsing WebSocket message:", error);
      }
    };

    ws.addEventListener('message', handleWebSocketMessage);

    return () => {
      ws.removeEventListener('message', handleWebSocketMessage);
    };
  }, [ws, selectedConversation]);

  return (
    <div className="flex h-[calc(100vh-4rem)]">
      <ConversationList
        selectedConversation={selectedConversation}
        onSelectConversation={handleSelectConversation}
        onNewConversation={handleNewConversation}
        ws={ws}
      />
      <div className="flex-1 flex flex-col">
        <ChatWindow
          conversation={selectedConversation}
          onConversationChange={handleConversationChange}
          onToggleSecondaryWindow={() => setIsSecondaryWindowOpen(!isSecondaryWindowOpen)}
          ws={ws}
        />
        {isSecondaryWindowOpen && <SecondaryWindow conversation={selectedConversation} />}
      </div>
    </div>
  )
}