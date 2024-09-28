import React, { createContext, useState, ReactNode } from 'react'

interface Conversation {
  conversationId: number;
  conversationName: string;
  conversationState: string;
  subject: string;
  rewrittenPrompt: string;
  metaPromptOne: string;
  metaPromptTwo: string;
}

interface SelectedConversationContextProps {
  selectedConversation: Conversation | null;
  setSelectedConversation: (conversation: Conversation | null) => void;
}

export const SelectedConversationContext = createContext<SelectedConversationContextProps>({
  selectedConversation: null,
  setSelectedConversation: () => {},
})

interface SelectedConversationProviderProps {
  children: ReactNode
}

export const SelectedConversationProvider: React.FC<SelectedConversationProviderProps> = ({ children }) => {
  const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null)

  return (
    <SelectedConversationContext.Provider value={{ selectedConversation, setSelectedConversation }}>
      {children}
    </SelectedConversationContext.Provider>
  )
}