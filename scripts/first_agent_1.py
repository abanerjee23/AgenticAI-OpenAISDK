from agents import Agent, Runner
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv(override=True)

""" Using Pydantic to produce structured outputs"""
class llm_output(BaseModel):
    description:str
    fun_facts:str


""" Agent is defined here. No API calls to the LLM takes place here."""
footsy = Agent(name='footsy',
               instructions="You are football expert. Answer user queries in a friendly and fun way.",
               model="gpt-5.4-mini",
               output_type=llm_output)

user_query = input("Enter your trickiest question on football: ")
print("\n")

result = Runner.run_sync(footsy, input=user_query)
"""
Runner.run_sync vs Runner.run endpoints?

Answer to the above query is - if your main.py is a plain if __name__ == "__main__": script, use Runner.run_sync. If you're inside async def main() (recommended once you add tools/handoffs with concurrent calls), use await Runner.run(...).

"""
usage = result.context_wrapper.usage
print(result.final_output)
print(f"Total input tokens - {usage.input_tokens}")
print(f"Total output tokens - {usage.output_tokens}")
print(f"Total tokens overall - {usage.total_tokens}")
print("\n")

print("------Cost Analysis per Run------")
print("\n")
input_cost = (usage.input_tokens/1000000)*0.75
output_cost = (usage.output_tokens/1000000)*4.5
total_cost = input_cost + output_cost
print(f"Cost of input tokens is ${input_cost:.10f}")
print(f"Cost of output tokens is ${output_cost:.10f}")
print(f"Total cost is ${total_cost:.10f}")
