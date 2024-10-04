import { useState, useEffect, useCallback, useContext } from 'react'
import ChatWindow from '../components/ChatWindow'
import ConversationList from '../components/ConversationList'
import SecondaryWindow from '../components/SecondaryWindow'
import { SecondaryWindowContext } from '../components/SecondaryWindowContext'
import { SelectedConversationContext } from '../components/SelectedConversationContext'
import { MetaAgentsContext, MetaAgent } from '../components/MetaAgentsContext'

// Define types for conversations and messages
interface Conversation {
  conversationId: number;
  conversationName: string;
  conversationState: string;
  subject: string;
  plan: string;
  rewrittenPrompt: string;
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
  const { selectedConversation, setSelectedConversation } = useContext(SelectedConversationContext)
  const { setMetaAgents } = useContext(MetaAgentsContext)
  const [ws, setWs] = useState<WebSocket | null>(null)

  // Consume context
  const { isSecondaryWindowOpen } = useContext(SecondaryWindowContext)

  // Function to set up WebSocket connection
  const setupWebSocket = useCallback(() => {
    console.log("Home: Setting up WebSocket connection...")
    const socket = new WebSocket("ws://localhost:8080/server/ws")
    setWs(socket)

    socket.onopen = () => {
      console.log("Home: WebSocket connected successfully")
      const message = JSON.stringify({ type: 'get_latest_conversation' })
      console.log("Home: Sending message to server:", message)
      socket.send(message)
    }

    socket.onclose = (event) => {
      console.log("Home: WebSocket disconnected", event)
      setTimeout(setupWebSocket, 5000)  // Attempt to reconnect after 5 seconds
    }

    socket.onerror = (error) => {
      console.error("Home: WebSocket error:", error)
    }

    socket.onmessage = (event) => {
      console.log("Home: Received message from server:", event.data);
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'latest_conversation' || data.type === 'conversation_updated') {
          console.log("Home: Updating selected conversation", data.data);
          setSelectedConversation(prevConversation => ({
            ...prevConversation,
            ...data.data,
          }));
        } else if (data.type === 'agent_blueprints') {
          console.log("Home: Received agent_blueprints data", data.agent_blueprints);
          if (Array.isArray(data.agent_blueprints)) {
            setMetaAgents(prevAgents => {
              const updatedAgents = [...prevAgents];
              data.agent_blueprints.forEach((incomingAgent: any) => {
                const blueprintId = incomingAgent.blueprint_id; // Use blueprint_id
                if (!blueprintId) {
                  console.warn('Incoming agent_blueprint is missing blueprint_id:', incomingAgent);
                  return;
                }

                const existingAgentIndex = updatedAgents.findIndex(agent => agent.id === blueprintId);
                if (existingAgentIndex !== -1) {
                  // Merge existing agent with incoming agent data
                  updatedAgents[existingAgentIndex] = {
                    ...updatedAgents[existingAgentIndex],
                    ...incomingAgent,
                  };
                  console.log(`Home: Updated agent with blueprint_id ${blueprintId}`, updatedAgents[existingAgentIndex]);
                } else {
                  // Add new agent using blueprint_id as id
                  const newAgent: MetaAgent = {
                    id: blueprintId, // Assign blueprint_id to id
                    name: incomingAgent.name,
                    personality: incomingAgent.personality,
                    temperament: incomingAgent.temperament,
                    temperature: incomingAgent.temperature,
                    role: incomingAgent.role,
                    url: incomingAgent.url || null,
                    system_prompt: incomingAgent.system_prompt,
                  };
                  updatedAgents.push(newAgent);
                  console.log("Home: Added new agent", newAgent);
                }
              });
              return updatedAgents;
            });
          } else {
            console.warn('Invalid "agent_blueprints" data format:', data.agent_blueprints);
          }
        } else {
          console.log("Home: Unhandled message type:", data.type);
        }
      } catch (error) {
        console.error("Home: Error parsing message:", error);
      }
    }

    return () => {
      console.log("Home: Cleaning up WebSocket connection")
      socket.close()
    }
  }, [setSelectedConversation, setMetaAgents])

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
    setMetaAgents([]) // Clear MetaAgents when a new conversation is created
    // No need to send anything to the server here, as it's already done in ConversationList
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
  }, [ws, selectedConversation, setSelectedConversation]);

  // Effect to clear MetaAgents when the selected conversation changes
  useEffect(() => {
    if (!selectedConversation) {
      setMetaAgents([]);
    }
  }, [selectedConversation, setMetaAgents]);

  return (
    <div className="flex flex-1 overflow-hidden">
      <ConversationList
        onNewConversation={handleNewConversation}
        ws={ws}
      />
      <div className="flex-1 flex overflow-hidden">
        <div className="flex-1 flex flex-col">
          <ChatWindow
            conversation={selectedConversation}
            onConversationChange={handleConversationChange}
            ws={ws}
          />
        </div>
        {isSecondaryWindowOpen && (
          <div className="w-1/3 border-l border-base-300 overflow-y-auto">
            <SecondaryWindow conversation={selectedConversation} />
          </div>
        )}
      </div>
    </div>
  )
}