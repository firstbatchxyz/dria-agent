from dria_agent.agent import ToolCallingAgent
from dria_agent.tools import APPLE_TOOLS

# Create an inference engine with the available tool(s).
agent = ToolCallingAgent(tools=APPLE_TOOLS, backend="ollama")

"""
# --- Example 1: Simple tool usage ---
query = "Show me how can I get to Barbaros bulvarı"
execution = agent.run(query, print_results=True)
"""

"""
# --- Example 2: Create calendar event ---
query = "Add new event to my calendar for tomorrow at 3PM to meetup with Batu? His mail is batuhan@firstbatch.xyz. We gonna talk about tiny-agents. My mail is omer@firstbatch.xyz. We said we'll meet around Dün moda"
execution = agent.run(query, print_results=True)
"""


query = "Find the file dota2.pdf."
execution = agent.run(query, print_results=True)
