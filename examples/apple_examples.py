from dria_agent import ToolCallingAgent
from dria_agent.tools import APPLE_TOOLS

# Create an inference engine with the available tool(s).
agent = ToolCallingAgent(tools=APPLE_TOOLS, backend="ollama")

query = "Show me how can I get to Barbaros bulvarı"
agent.run(query, print_results=True)

# --- Example 2: Create calendar event ---
query = "Add new event to my calendar for tomorrow at 3PM to meetup with Batu? His mail is batuhan@firstbatch.xyz. We gonna talk about tiny-agents. My mail is omer@firstbatch.xyz. We said we'll meet around Dün moda"
agent.run(query, print_results=True)

# --- Example 3: Open up a file ---
query = "Find the file dota2.pdf."
agent.run(query, print_results=True)

# --- Example 4: Find the contact, and send an SMS ---
contact_name = "John Doe"
message = "Have you heard about tiny agents?"
query = f"Find {contact_name} and send an SMS saying {message}"
agent.run(query, print_results=True, num_tools=3)
