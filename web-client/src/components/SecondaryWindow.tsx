import React from 'react'

interface SecondaryWindowProps {
  conversation: Conversation | null;
}

const SecondaryWindow: React.FC<SecondaryWindowProps> = ({ conversation }) => {
  return (
    <div className="w-full h-[93vh] bg-base-100 p-4 border-l border-base-300 flex flex-col overflow-hidden">
      <h2 className="text-2xl font-bold mb-4">Secondary Window</h2>
      {conversation ? (
        <div className="space-y-4 flex-grow overflow-y-auto">
          <div className="card bg-base-200 shadow-xl">
            <div className="card-body">
              <h3 className="card-title">Conversation Details</h3>
              <p><strong>Name:</strong> {conversation.conversationName}</p>
              <p><strong>Subject:</strong> {conversation.subject}</p>
              <p><strong>State:</strong> {conversation.conversationState}</p>
              <p><strong>Rewritten Prompt:</strong> {conversation.rewrittenPrompt}</p>
              <p><strong>Meta Prompt One:</strong> {conversation.metaPromptOne}</p>
              <p><strong>Meta Prompt Two:</strong> {conversation.metaPromptTwo}</p>
            </div>
          </div>
        </div>
      ) : (
        <div className="alert alert-warning">
          <svg xmlns="http://www.w3.org/2000/svg" className="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
          <span>No conversation selected</span>
        </div>
      )}
    </div>
  )
}

export default SecondaryWindow