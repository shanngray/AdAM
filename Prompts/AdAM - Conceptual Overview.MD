# AdAM - Conceptual Overview

To conceptualize how these components fit together in your project, let's break down the process flow and discuss how each component interacts with the others:

## Components
1. Web Client:
   - This is the user interface where the interaction begins.
   - The user enters a prompt here.
   - The Web Client sends the prompt to the FastAPI Server.

2. FastAPI Server:
   - Acts as the central coordinator between all components.
   - Receives the prompt from the Web Client.
   - Sends the prompt to two places:
     a) The LLM Workflow for processing
     b) The Database for recording

3. LLM Workflow:
   - Receives the prompt from the FastAPI Server.
   - Processes the prompt and generates a response.
   - Streams the response back to the FastAPI Server in real-time.

4. Database:
   - Receives and stores the initial prompt from the FastAPI Server.
   - Later receives and stores the complete LLM response from the FastAPI Server.

This architecture allows for real-time interaction while also maintaining a record of all interactions. 

## Start up Process

1. Load the database with all the relevant data
2. Start the FastAPI Server
3. Start the Web Client
4. Send list of Conversation Names and IDs to Web Client

## Interaction Process

1. User selects Conversation Name or Creates a New Conversation
   - Response is sent to FastAPI Server
   - If Conversation Name is new, a new Conversation ID is created
   - If Conversation Name is existing, the Conversation History is loaded
2. User enters prompt in Web Client
3. Web Client sends prompt to FastAPI Server
3. FastAPI Server sends prompt to LLM Workflow and Database
4. LLM Workflow processes prompt and starts streaming response
5. FastAPI Server receives streamed response and sends it to Web Client in real-time
6. Once response is complete, FastAPI Server sends full response to Database
7. Process repeats for next user prompt

