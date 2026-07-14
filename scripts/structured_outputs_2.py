from agents import Agent, Runner, RunConfig, ModelSettings
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Literal

load_dotenv(override=True)

""" Structured output schema for the ticket classifier agent. """
class classify_tickets(BaseModel):
    ticket_title:str
    ticket_description:str
    classification_result: Literal["high","medium","low"]

""" Agent is defined here. No API calls to the LLM take place here. """
customer_ticket_classifier = Agent(name="customer_ticket_classifier",
                       instructions=(
                           "You are a support ticket triage agent. Given a customer's raw message, "
                           "extract a concise ticket_title, restate the issue as ticket_description, "
                           "and set classification_result to one of 'high', 'medium', or 'low'.\n\n"
                           "Priority guidelines:\n"
                           "- 'high': account security or money at risk (fraud, unauthorized transactions, "
                           "account lockout, data breach).\n"
                           "- 'medium': something is broken or blocking the customer, but no security/financial "
                           "risk (billing discrepancy, feature not working, delayed order).\n"
                           "- 'low': general questions with no urgency (product/catalogue questions, how-to "
                           "questions, feedback).\n\n"
                           "If a ticket could fit multiple levels, err toward the higher priority."
                       ),
                       model="gpt-5.4-mini",
                       output_type=classify_tickets)

user_query = input("What's your query? Please be as descriptive as possible. Type here >> ")
result = Runner.run_sync(customer_ticket_classifier,user_query)
usage = result.context_wrapper.usage
print("\n")
print(result.final_output)
print("\n")
print("------Cost Analysis per Run------")
print("\n")
input_cost = (usage.input_tokens/1000000)*0.75
output_cost = (usage.output_tokens/1000000)*4.5
total_cost = input_cost + output_cost
print(f"Cost of input tokens is ${input_cost:.10f}")
print(f"Cost of output tokens is ${output_cost:.10f}")
print(f"Total cost is ${total_cost:.10f}")
