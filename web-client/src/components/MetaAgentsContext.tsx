import React, { createContext, useState, ReactNode } from 'react';

// Define the structure of a MetaAgent
export interface MetaAgent {
  id: number;
  name: string;
  personality: string;
  temperament: string;
  temperature: number;
  role: string;
  url: string | null;
  system_prompt: string;
}

interface MetaAgentsContextProps {
  metaAgents: MetaAgent[];
  setMetaAgents: (agents: MetaAgent[]) => void;
}

export const MetaAgentsContext = createContext<MetaAgentsContextProps>({
  metaAgents: [],
  setMetaAgents: () => {},
});

interface MetaAgentsProviderProps {
  children: ReactNode;
}

export const MetaAgentsProvider: React.FC<MetaAgentsProviderProps> = ({ children }) => {
  const [metaAgents, setMetaAgents] = useState<MetaAgent[]>([]);

  return (
    <MetaAgentsContext.Provider value={{ metaAgents, setMetaAgents }}>
      {children}
    </MetaAgentsContext.Provider>
  );
};
