# Agentic AI — OpenAI SDK Learning Journal

A hands-on learning log as I work through the [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) — building agents, understanding orchestration, and tracking cost/usage along the way.

**Stack:** OpenAI Agents SDK · Python (`uv` for env/dependency management)

---

## Progress Log

Newest entries at the top. Each entry is a snapshot of what was learned/built that day — earlier entries are kept as-is so this doubles as a running history of the journey.

### 2026-07-14

**Built a tool-using agent: news reporter** — [`scripts/run_config_3.py`](scripts/run_config_3.py)

- First agent with an actual **function tool**: `search_web`, a `@function_tool`-decorated wrapper around the Tavily search API (`TavilyClient.search(..., search_depth='advanced')`), passed to the agent via `tools=[search_web]`.
- **System prompt** written to force real research over memorized answers: the agent must call `search_web`, refine/re-search on thin results, cross-check claims across sources, flag conflicting or developing stories explicitly, and publish in a fixed Headline / Summary / Details / Sources format.
- **`RunConfig` + `ModelSettings`** used for the first time to control generation behavior (`verbosity`, `reasoning`) per run instead of only per-agent.
- **Bug found and fixed:** `ModelSettings(reasoning='medium')` raised a Pydantic `ValidationError` — unlike `verbosity`, which takes a plain `Literal['low','medium','high']` string, `reasoning` expects a `Reasoning` object/dict with an `effort` key. Fix: `reasoning={"effort": "medium"}`.
- Learned not every model supports every `ModelSettings` field — worth checking the [OpenAI platform docs](https://platform.openai.com/chat/edit?models) per-model before assuming a parameter (e.g. `temperature`, `tool_choice`) is honored.

Example run (U.S.–Iran Strait of Hormuz conflict query):

![Terminal output: news reporter agent's researched report with headline, summary, details, sources, and cost breakdown](assets/news_reporter_run.png)

**Next up:** multi-agent handoffs.

### 2026-07-13

**Built the first agent** — [`scripts/first_agent_1.py`](scripts/first_agent_1.py)

- Created `footsy`, a football-expert `Agent` (friendly/fun persona) running on `gpt-5.4-mini`, invoked via `Runner.run_sync`.
- **`Runner.run_sync` vs `Runner.run`:** both take identical parameters — `run` is `async` (use inside an existing event loop / `async def main()`), `run_sync` is a synchronous wrapper around it (`run_until_complete` under the hood) for plain scripts. Documented directly in the script as a learning note.
- Made the script interactive — takes the user's football question via `input()` instead of a hardcoded prompt.
- **Usage tracking:** pulled `result.context_wrapper.usage` to report input/output/total token counts per run.
- **Cost analysis per run:** calculated actual dollar cost from token usage —
  - input cost = `(input_tokens / 1_000_000) * $0.75`
  - output cost = `(output_tokens / 1_000_000) * $4.50`
  - plus a **total cost** line (input + output combined)
  - Formatting iterated from raw floats (unreadable scientific notation like `2.475e-05`) → 4 decimal places (rounded tiny input costs to `$0.0000`, hiding real signal) → **10 decimal places**, settled on for enough precision to see true per-run cost at this token scale.

Example run (`"Has England ever won the world cup?"`):

![Terminal output: agent answer, token usage, and per-run cost breakdown](assets/first_agent_1_run.png)

**Structured outputs with Pydantic:** gave the agent an `output_type` instead of free-text —

```python
class llm_output(BaseModel):
    description: str
    fun_facts: str
```

Passed as `Agent(..., output_type=llm_output)`. `result.final_output` now comes back as a parsed `llm_output` instance rather than a raw string, so downstream code gets guaranteed fields instead of parsing prose. Added `pydantic` as an explicit dependency for this.

Example run (`"How many goals has Messi scored in Fifa World Cups?"`):

![Terminal output: structured output with description/fun_facts fields, token usage, and cost breakdown](assets/first_agent_1_structured_output.png)

**Reusable boilerplate** — [`scripts/structured_outputs.py`](scripts/structured_outputs.py)

Pulled the Pydantic structured-output pattern (imports, `load_dotenv`, `BaseModel` output class, `Agent` definition) out into its own template file, so every new experiment starts from the same skeleton instead of copy-pasting from the last script.

**New skill: `new-agent-script`** — scaffolds `scripts/<name>.py` from that boilerplate on request (e.g. "create a new script for X"). It re-reads `structured_outputs.py` fresh each time rather than caching a copy of the pattern, so if the boilerplate evolves later, new scaffolds automatically pick up the change.

**Built a real agent from the boilerplate: ticket triage classifier** — [`scripts/structured_outputs.py`](scripts/structured_outputs.py)

Turned the template into a working `customer_ticket_classifier` agent:

```python
class classify_tickets(BaseModel):
    ticket_title: str
    ticket_description: str
    classification_result: Literal["high", "medium", "low"]
```

- Used `typing.Literal` to constrain `classification_result` to an enum-like set of exact strings, instead of a free-text field the model could drift on.
- **Prompt design:** the initial instructions only gave criteria/examples for 'high' and 'low', never mentioned that the agent needed to *populate* `ticket_title`/`ticket_description` from the raw input, and had stray whitespace baked into the string from backslash line-continuations. Rewritten with explicit per-tier criteria (including 'medium'), a tie-breaking rule ("err toward the higher priority"), and implicit string concatenation (parenthesized adjacent string literals) instead of `\`-continuations to avoid leaking indentation into the prompt text.
- Made it interactive via `input()`, reusing the same usage-tracking + cost-analysis block from `first_agent_1.py`.
- **Dependency note:** `uv add`-ing `typing` pulled in the standalone PyPI `typing` backport package (`typing>=3.10.0.0`) even though this project requires Python ≥3.11, where `typing` is already stdlib. Harmless but unnecessary — left in as-is for now rather than removed.

Example run (`"I have noticed unauthorised activity on my card on your website"`):

![Terminal output: ticket classification with title/description/priority fields, token usage, and cost breakdown](assets/ticket_classifier_run.png)

**Next up:** tool calling / function tools, multi-agent handoffs.
