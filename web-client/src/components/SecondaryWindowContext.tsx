import React, { createContext, useState, ReactNode } from 'react'

interface SecondaryWindowContextProps {
  isSecondaryWindowOpen: boolean
  toggleSecondaryWindow: () => void
}

export const SecondaryWindowContext = createContext<SecondaryWindowContextProps>({
  isSecondaryWindowOpen: false,
  toggleSecondaryWindow: () => {},
})

interface SecondaryWindowProviderProps {
  children: ReactNode
}

export const SecondaryWindowProvider: React.FC<SecondaryWindowProviderProps> = ({ children }) => {
  const [isSecondaryWindowOpen, setIsSecondaryWindowOpen] = useState(false)

  const toggleSecondaryWindow = () => {
    setIsSecondaryWindowOpen(prev => !prev)
  }

  return (
    <SecondaryWindowContext.Provider value={{ isSecondaryWindowOpen, toggleSecondaryWindow }}>
      {children}
    </SecondaryWindowContext.Provider>
  )
}