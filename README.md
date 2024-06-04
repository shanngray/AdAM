#Ad.A.M - Adaptive Agent Multiplex

![AdAM Node Map](./AdAM%20Node%20Map.png)

This still needs a lot of work but here is the basic gist of the project...

1) To start the prompt gets re-written using prompt engineering. This prompt then get sent back to the human for them to tweak or agree with (this step is to emulate "active listening" where the agent rephrases the request and the human can let them know if they are on the right track. 2) The feedback then gets analysed to determine whether to proceed (feedback is simple affirmation) or if the human says pretty much anything else it will go back for review and to rewrite the prompt again.
3) Next the subject matter gets pulled out of the prompt and added into the state as a separate variable
4) The subject matter variable is used to make an ad hoc "expert" who will write the new system prompts (might need to add an extra node here to "write" the system prompt of the first expert if this approach doesn't work).
5) Then our expert writes the system prompts for our team of meta agents. This may require a separate LLM call for each system prompt and is where I want to spend most of the time iterating and improving. Might even have different team configurations run as inner graphs and the expert decides which one to use (this diagram only shows one simple three-agent team).
6) The system prompts then get inserted into the meta agents and they are fed the re-engineered prompt from the first step.
7) Once they are happy the response gets fed back to the human.



