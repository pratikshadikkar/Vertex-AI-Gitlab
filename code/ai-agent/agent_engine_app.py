# agent_engine_app.py
import os
import vertexai
from vertexai.agent_engines import AdkApp, App
from root_agnet import create_root_agent
 
def create_app():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION")
 
    if not project_id or not location:
        raise ValueError(
                "The GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION "
                "environment variables were not set in the Agent Engine runtime."
        )
 
    vertexai.init(project=project_id, location=location)
    root_agent = create_root_agent()
    return App(agent=root_agent)
 
app = AdkApp(app_callable=create_app, enable_tracing=True)