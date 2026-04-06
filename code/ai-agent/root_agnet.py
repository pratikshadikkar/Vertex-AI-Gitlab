from google.adk.agents import LlmAgent
import os
from google.adk.tools import agent_tool
from google_search_agent_tool import google_search_agent
from url_context_agent_tool import url_context_agent_tool

def main():
        root_agent = LlmAgent(
            name= os.environ["main_agent_name"],
            model=os.environ["main_agent_model"],
            description=(
                os.environ["main_agent_description"]
                ),
                sub_agents=[],
                instruction=os.environ["main_agent_instruction"],
                tools=[
                    agent_tool.AgentTool(agent=google_search_agent),
                    agent_tool.AgentTool(agent=url_context_agent_tool)
                    ],
                    )

if __name__ == "__main__":

    main()

