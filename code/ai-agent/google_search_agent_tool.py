from google.adk.agents import LlmAgent
import os
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context

def google_search_agent(LlmAgent):
    return LlmAgent(
        name= os.environ["agent1_name"],
        model=os.environ["agent1_model"],
        description=(
            os.environ["agent1_description"]
            ),
            sub_agents=[],
                instruction=os.environ["agent1_instruction"],
                tools=[
                    GoogleSearchTool()
                    ],)