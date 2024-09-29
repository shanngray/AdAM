# Creating Meta Agents

Some of the tasks required in this process are going to be difficult for an LLM to do because they don't have any context 
and trying to learn something like this will be difficult.

## Step 1: Decide how many agents to create
Hard. The optimal number of agents to create is going to be dependent on the task. Further we don't know have any data on
what the optimal number of agents is for a given task.

## Step 2: Decide on the capabilities of the agents
(a) Does the agent need to use a tool?
(b) Does the agent have the ability to remember past messages? => Ideally this would be to contrsuct a memory store rather than verbatim messages.

## Step 3: Creating complimentary agents
Ideally the agents should compliment each other but again this will be difficult for the LLM to do.

## Step 4: Agent Archetypes
One way to solve some of these issues is to create archetypes for agents. These archetypes will have a set of capabilities.
They will also have a set of goals that they are designed to achieve.  The archetype will work as a template that needs
to be completed meaning that each agent is unique.

### Archetype 1: The General Agent
This type of agent is going to be the most common agent. It is going to be a general agent that is designed to be able to do a 
variety of tasks, but it will not have tool use or memory.

### Archetype 2: The Memory Agent
This type of agent is going to be designed to remember messages. It will have a memory store that it can use to recall past messages.

### Archetype 3: The Search Agent
A special type of tool agent that is able to search the internet for information. It is only ever assigned the one tool.

### Archetype 4: The Tool Agent
As task for later on will be to create a set of tools that can be used by the agents. These tools will be a combination of
LangChain base tools and custom tools and a variety of them will be assigned to the agent to perform tasks.

## Agent Personality
Each agent will have a personality. The personality will be a set of traits that the agent will have. This will be a combination of
personality traits and role playing and will be used to create the prompt for the agent.

## Agent Name
Each agent will be given a nickname based off it personality and traits.

## Agent Description
a one sentence description of the agent to help the supervisor decide who goes next.






