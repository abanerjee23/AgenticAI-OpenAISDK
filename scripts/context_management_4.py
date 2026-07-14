from database_context_management_4 import Database
from agents import Agent, Runner, RunContextWrapper, function_tool
from dotenv import load_dotenv
from dataclasses import dataclass

"""Load environment variables"""
load_dotenv(override=True)

"""Create an instance of the class 'Database"""
db=Database()

"""Define the context object or 'bagpack' for the app"""
@dataclass
class AppContext:
    user_name:str
    db:Database

"""Once the context object has been defined, we add context to the 'bagpack'"""
app_state = AppContext(user_name='Alice',db=db)

"""Define the tool that the agent will call"""
@function_tool
def get_order_details(wrapper:RunContextWrapper[AppContext], order_id:str):
    state = wrapper.context
    order = state.db.get_order(order_id)
    return f"Hello {state.user_name}. Your order with {order_id} of {order['pizza']} is \
        currently {order['status']}. Hope you enjoy your pizza!"

"""Define the agent"""
order_status_agent = Agent(
    name="Pizza Assistant",
    instructions="""You are a trusted resource to respond back to a user's \
        query regarding their pizza order. In your response, remember to quote back \
            their order id, what they have specifically ordered, and what's the latest status. You \
                must respond back in a friendly tone. Finally, ensure you do not add any markdown characters or special characters \
                    such as '*', '$', '#', etc. in your response. It must be in plain text.""",
    tools=[get_order_details],
    model="gpt-5.4-mini"
)

"""Execute agent runtime using Runner.run_sync"""
result = Runner.run_sync(order_status_agent, input="Where's my order with order id 123?",
                         context=app_state)

"""Print agent output"""

print(result.final_output)
