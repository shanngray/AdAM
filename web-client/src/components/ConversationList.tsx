import React, { useState, useEffect, useContext } from 'react';
import { SelectedConversationContext } from './SelectedConversationContext';

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
  onNewConversation: (conversation: Conversation) => void;
  ws: WebSocket | null;
}

const ConversationList: React.FC<ConversationListProps> = ({
  onNewConversation,
  ws,
}) => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const { setSelectedConversation } = useContext(SelectedConversationContext);

  useEffect(() => {
    if (!ws) return;

    const handleMessage = (event: MessageEvent) => {
      let data: any;
      try {
        data = JSON.parse(event.data);
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
        return;
      }

      console.log('Received WebSocket message:', data);

      if (data.type === 'conversations') {
        if (Array.isArray(data.conversations)) {
          setConversations(data.conversations);
        } else {
          console.warn('Invalid "conversations" data format:', data.conversations);
        }
      } else if (data.type === 'new_conversation') {
        if (data.data && typeof data.data.conversationId === 'number') {
          const newConversation: Conversation = {
            conversationId: data.data.conversationId,
            conversationName: data.data.conversationName || 'New Conversation',
            conversationState: 'first_message',
            subject: '',
            rewrittenPrompt: '',
            metaPromptOne: '',
            metaPromptTwo: '',
          };
          setConversations(prevConversations => [...prevConversations, newConversation]);
          onNewConversation(newConversation);
        } else {
          console.warn('Invalid "new_conversation" data format:', data.data);
        }
      } else if (data.type === 'conversation_updated') {
        if (data.conversation_id && typeof data.conversation_id === 'number') {
          setConversations(prevConversations =>
            prevConversations.map(conv =>
              conv.conversationId === data.conversation_id
                ? { ...conv, ...data.updated_fields }
                : conv
            )
          );
        } else {
          console.warn('Invalid "conversation_updated" data format:', data);
        }
      } else {
        console.warn('Unhandled message type:', data.type);
      }
    };

    ws.addEventListener('message', handleMessage);

    return () => {
      ws.removeEventListener('message', handleMessage);
    };
  }, [ws, onNewConversation]);

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

    ws.send(
      JSON.stringify({
        type: 'create_conversation',
        ...placeholderConversation,
      })
    );
  };

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
                className={''} // You can add active classes if needed
                onClick={() => {
                  console.log('Selecting conversation:', conversation);
                  setSelectedConversation(conversation);
                }}
              >
                {conversation?.conversationName || 'Unnamed Conversation'}
              </a>
            </li>
          ))}
        </ul>
      )}

      <div className="mt-4">
        <button className="btn btn-primary mt-2 w-full" onClick={handleNewConversation}>
          New Conversation
        </button>
      </div>
    </div>
  );
};

export default ConversationList;