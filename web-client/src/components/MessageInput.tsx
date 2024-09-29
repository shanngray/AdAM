import React, { useState, useCallback } from 'react';

// Define the structure of a Conversation object
interface Conversation {
  conversationId: number;
  conversationName: string;
  conversationState: string;
  subject: string;
  rewrittenPrompt: string;
}

// Define the props that the MessageInput component expects
interface MessageInputProps {
  conversation: Conversation | null;
  onSendMessage: (message: string) => void;
}

const MessageInput: React.FC<MessageInputProps> = ({ conversation, onSendMessage }) => {
  // Use state to manage the current message input
  const [message, setMessage] = useState('');

  // Define a callback function to handle form submission
  const handleSubmit = useCallback((e: React.FormEvent) => {
    // Prevent the default form submission behavior
    e.preventDefault();
    
    // Check if the message is not empty (after trimming whitespace)
    if (!message.trim()) {
      return; // If empty, do nothing
    }

    // Call the onSendMessage prop function with the trimmed message
    onSendMessage(message.trim());
    console.log('Message sent:', message.trim()); // Log the sent message

    // Clear the input field after sending
    setMessage('');
  }, [message, onSendMessage]);

  return (
    <form onSubmit={handleSubmit} className="flex p-4">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        className="input input-bordered flex-1"
        placeholder={conversation ? "Type your message..." : "Select a conversation to start chatting"}
        disabled={!conversation} // Disable input if no conversation is selected
      />
      <button type="submit" className="btn btn-primary ml-2" disabled={!conversation}>
        Send
      </button>
    </form>
  );
};

export default MessageInput;