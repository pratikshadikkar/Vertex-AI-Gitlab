from google.adk.agents import LlmAgent
import os
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context

def url_context_agent_tool(LlmAgent):
    return LlmAgent(
        name= os.environ["agent2_name"],
        model=os.environ["agent2_model"],
        description=(
            os.environ["agent2_description"]
            ),
            sub_agents=[],
                instruction=os.environ["agent2_instruction"],
                tools=[
                    url_context
                    ],)