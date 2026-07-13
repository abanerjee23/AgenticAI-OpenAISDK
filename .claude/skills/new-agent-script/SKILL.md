---
name: new-agent-script
description: Use when the user wants to start a new OpenAI Agents SDK script or experiment (e.g. "create a new script for X", "scaffold an agent for Y", "start a new agent file"). Generates a new file in scripts/ pre-filled with this project's standard boilerplate (imports, load_dotenv, Pydantic output model, Agent definition) instead of retyping it each time.
version: 0.1.0
---

# New Agent Script

Scaffolds a new script under `scripts/` using the project's standard agent boilerplate, so it doesn't have to be retyped for every new experiment.

## Source of truth

`scripts/structured_outputs.py` is the canonical boilerplate — **read it fresh every time this skill runs**, don't rely on the snapshot below. If it's been edited since (new default model, extra imports, a usage/cost-analysis block folded in), the newly scaffolded script should match the *current* file, not this description.

As of writing, the pattern is:

```python
from agents import Agent, Runner
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv(override=True)

class <OutputModelName>(BaseModel):
    <fields>

<agent_var_name> = Agent(name="<agent_name>",
                       instructions="<system prompt>",
                       model="gpt-5.4-mini",
                       output_type=<OutputModelName>)
```

## Steps

1. If the user hasn't already said, ask what the new script is for: a filename, the agent's purpose/persona, and what structured output fields (if any) it should return.
2. Read `scripts/structured_outputs.py` to get the current boilerplate shape.
3. Create `scripts/<name>.py` filling in the boilerplate with real values:
   - A descriptive `BaseModel` name and real fields (not `set_your_name` / `pass` placeholders)
   - A real agent variable name, `name=`, and a proper `instructions=` system prompt matching the requested persona
   - Keep `model="gpt-5.4-mini"` unless told otherwise
4. Don't bolt on the interactive `input()` prompt, usage tracking, or cost-analysis block from `first_agent_1.py` — those aren't part of the core boilerplate. Only add them if explicitly asked.
5. Report the new file path — don't dump the whole file back into the chat unless asked.
