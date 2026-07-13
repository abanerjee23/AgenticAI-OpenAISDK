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

```
Total input tokens  - 33
Total output tokens - 54
Total tokens overall - 87

------Cost Analysis per Run------

Cost of input tokens is  $0.0000247500
Cost of output tokens is $0.0002430000
Total cost is             $0.0002677500
```

**Next up:** tool calling / function tools, multi-agent handoffs.
