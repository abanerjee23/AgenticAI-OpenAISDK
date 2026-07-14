from agents import Agent, Runner, RunConfig, ModelSettings, function_tool
from dotenv import load_dotenv
import os
from tavily import TavilyClient

load_dotenv()
client = TavilyClient(os.getenv("TAVILY_API_KEY"))

"""Defining a web search tool for the agent"""
@function_tool
def search_web(user_search_query:str)->str:
    response = client.search(user_search_query,search_depth='advanced')
    return response

"""Agent definiton"""
news_reporter_agent = Agent(name="News Reporter", instructions=(
    "You are a news reporter. Given a user's query, research it using the search_web tool "
    "and publish a detailed, well-organized report — do not answer from memory alone, and "
    "do not fabricate facts, quotes, or sources.\n\n"
    "Process:\n"
    "1. Call search_web with a focused query capturing the user's request. If the first results "
    "are thin or ambiguous, refine the query and search again (e.g. narrow by date, entity, or "
    "sub-topic) rather than filling gaps with assumptions.\n"
    "2. Cross-check claims against multiple results where possible, and prefer the most recent "
    "and specific sources over vague or outdated ones.\n"
    "3. If sources conflict or the topic is still developing, say so explicitly instead of "
    "picking one version silently.\n\n"
    "Report format:\n"
    "- Headline: a concise, factual title for the story.\n"
    "- Summary: 2-3 sentences covering the core who/what/when/where.\n"
    "- Details: the full report body, organized in short paragraphs or bullet points, covering "
    "context, key facts, and relevant background.\n"
    "- Sources: list the sources you drew on.\n\n"
    "Tone: neutral, factual, and precise — report what the sources say, not your own opinion. "
    "If search_web returns nothing useful for the query, say so plainly instead of inventing a report."
), model="gpt-5.4-mini", tools=[search_web])


user_search_query = input("What would you like to search today? Type here >>> ")
""" Not every model will support all the model setting parameters. Review the OpenAI platforms webpage to validate which parameters
    are actually supported. Link here: https://platform.openai.com/chat/edit?models
"""
llm_response = Runner.run_sync(news_reporter_agent, user_search_query,
                               run_config=RunConfig(
                                   model_settings=ModelSettings(
                                       verbosity='medium',
                                       reasoning={"effort": "medium"},
                                   )
                               ))
usage = llm_response.context_wrapper.usage
print("\n")
print(llm_response.final_output)
print("\n")
print("------Cost Analysis per Run------")
print("\n")
input_cost = (usage.input_tokens/1000000)*0.75
output_cost = (usage.output_tokens/1000000)*4.5
total_cost = input_cost + output_cost
print(f"Cost of input tokens is ${input_cost:.10f}")
print(f"Cost of output tokens is ${output_cost:.10f}")
print(f"Total cost is ${total_cost:.10f}")
