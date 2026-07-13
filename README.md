# Agentic AI — OpenAI SDK Learning Journal

A hands-on learning log as I work through the [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) — building agents, understanding orchestration, and tracking cost/usage along the way.

**Stack:** OpenAI Agents SDK · Python (`uv` for env/dependency management)

---

## Progress Log

Newest entries at the top. Each entry is a snapshot of what was learned/built that day — earlier entries are kept as-is so this doubles as a running history of the journey.

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

**Next up:** tool calling / function tools, multi-agent handoffs.
