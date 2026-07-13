from agents import Agent, Runner
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv(override=True)

class set_your_name(BaseModel):
    pass

set_agent_name = Agent(name="set_name",
                       instructions="System prompt goes here",
                       model="gpt-5.4-mini",
                       output_type=set_your_name)
