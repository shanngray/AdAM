import React, { useState, useEffect } from 'react'

interface Conversation {
  conversationId: number;
  conversationName: string;
  conversationState: string;
  subject: string;
  rewrittenPrompt: string;
  metaPromptOne: string;
  metaPromptTwo: string;
}

interface ConversationListProps {
  selectedConversation: Conversation | null
  onSelectConversation: (conversation: Conversation) => void
  onNewConversation: (conversation: Conversation) => void
  ws: WebSocket | null
}

const ConversationList: React.FC<ConversationListProps> = ({
  selectedConversation,
  onSelectConversation,
  onNewConversation,
  ws
}) => {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [newConversationName, setNewConversationName] = useState('')

  useEffect(() => {
    if (ws) {
      const handleMessage = (event: MessageEvent) => {
        const message = JSON.parse(event.data);
        if (message.type === 'conversations') {
          console.log('Received conversations:', message.data);
          setConversations(message.data);
        } else if (message.type === 'new_conversation') {
          console.log('Received new conversation:', message.data);
          setConversations(prevConversations => [...prevConversations, message.data]);
          onNewConversation(message.data);
        }
      };

      ws.addEventListener('message', handleMessage)

      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'get_conversations' }))
      }

      return () => {
        ws.removeEventListener('message', handleMessage)
      };
    }
  }, [ws, onNewConversation])

  useEffect(() => {
    if (selectedConversation) {
      setConversations(prevConversations => 
        prevConversations.map(conv => 
          conv.conversationId === selectedConversation.conversationId ? selectedConversation : conv
        )
      );
    }
  }, [selectedConversation]);

  const handleNewConversation = () => {
    if (!newConversationName.trim() || !ws) return

    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'create_conversation',
        name: newConversationName
      }))
      setNewConversationName('')
    } else {
      console.error('WebSocket is not open');
    }
  }

  return (
    <div className="w-64 bg-base-100 p-4">
      <h2 className="text-xl font-bold mb-4">Conversations</h2>
      {conversations.length === 0 ? (
        <p>No conversations yet. Start a new one!</p>
      ) : (
        <ul className="menu bg-base-200 w-56 rounded-box">
          {conversations.map((conversation, index) => (
            <li key={conversation.conversationId || `conversation-${index}`}>
              <a
                className={selectedConversation?.conversationId === conversation.conversationId ? 'active' : ''}
                onClick={() => {
                  console.log("Selecting conversation:", conversation)
                  onSelectConversation(conversation)
                }}
              >
                {conversation.conversationName || 'Unnamed Conversation'}
              </a>
            </li>
          ))}
        </ul>
      )}
      <div className="mt-4">
        <input
          type="text"
          value={newConversationName}
          onChange={(e) => setNewConversationName(e.target.value)}
          className="input input-bordered w-full"
          placeholder="New conversation name"
        />
        <button
          className="btn btn-primary mt-2 w-full"
          onClick={handleNewConversation}
        >
          New Conversation
        </button>
      </div>
    </div>
  )
}

export default ConversationList