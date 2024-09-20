import React from 'react'

interface SecondaryWindowProps {
  conversation: Conversation | null;
}

const SecondaryWindow: React.FC<SecondaryWindowProps> = ({ conversation }) => {
  return (
    <div className="w-1/3 bg-base-100 p-4 border-l border-base-300">
      <h2 className="text-xl font-bold mb-4">Secondary Window</h2>
      {conversation ? (
        <div>
          <p>Conversation: {conversation.conversationName}</p>
          <p>Subject: {conversation.subject}</p>
          <p>State: {conversation.conversationState}</p>
          {/* Add more conversation details as needed */}
        </div>
      ) : (
        <p>No conversation selected</p>
      )}
    </div>
  )
}

export default SecondaryWindow