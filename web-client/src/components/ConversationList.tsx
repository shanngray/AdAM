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

  useEffect(() => {
    if (!ws) return

    const handleMessage = (event: MessageEvent) => {
      const data = JSON.parse(event.data)
      if (data.type === 'conversations') {
        setConversations(data.conversations)
      } else if (data.type === 'new_conversation') {
        const newConversation: Conversation = {
          conversationId: data.data.conversationId,
          conversationName: data.data.conversationName || 'New Conversation',
          conversationState: 'first_message',
          subject: '',
          rewrittenPrompt: '',
          metaPromptOne: '',
          metaPromptTwo: '',
        }
        setConversations(prevConversations => [...prevConversations, newConversation])
        onNewConversation(newConversation)
      }
    }

    ws.addEventListener('message', handleMessage)

    return () => {
      ws.removeEventListener('message', handleMessage)
    }
  }, [ws, onNewConversation])

  const handleNewConversation = () => {
    if (!ws) return;

    const placeholderConversation = {
      conversationId: Date.now(), // Temporary ID until server assigns one
      conversationName: 'New Conversation',
      conversationState: 'new',
      subject: '',
      rewrittenPrompt: '',
      metaPromptOne: '',
      metaPromptTwo: '',
    };

    ws.send(JSON.stringify({
      type: 'create_conversation',
      ...placeholderConversation
    }));
  }

  return (
    <div className="w-64 bg-base-100 p-4">
      <h2 className="text-xl font-bold mb-4">Conversations</h2>
      {conversations.length === 0 ? (
        <p>No conversations yet. Start a new one!</p>
      ) : (
        <ul className="menu bg-base-200 w-56 rounded-box">
          {conversations.map((conversation, index) => (
            <li key={conversation?.conversationId ?? `conversation-${index}`}>
              <a
                className={selectedConversation?.conversationId === conversation?.conversationId ? 'active' : ''}
                onClick={() => {
                  console.log("Selecting conversation:", conversation)
                  onSelectConversation(conversation)
                }}
              >
                {conversation?.conversationName || 'Unnamed Conversation'}
              </a>
            </li>
          ))}
        </ul>
      )}
      <div className="mt-4">
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