# TreeSomeAI

A team of three AI agents (🟠 Claude · 🟢 Codex · 🔵 Gemini/Antigravity) working together
on a Nothing Phone (1): Termux + Ubuntu (proot-distro).

| Tool | Purpose |
|---|---|
| `bin/pedir` | one agent calls another, with usage logging and the "captain's armband" (automatic handover when one runs out of tokens) |
| `bin/saldo` | how much is left on each agent's account, without spending tokens |
| `bin/rever-consumo` | token usage report |
| `policies/` | Antigravity/Gemini permissions per mode (read-only/write) |
| `tests/` | offline regression tests |

Shared memory (outside the repository): `MEMORIA.md` + `temas/`.

> The command names and the tools' messages are in Portuguese (`pedir` = ask, `saldo` = balance,
> `rever-consumo` = review usage).

## What it does

### 📨 `pedir`: one agent calls another
`pedir <codex|gemini|claude|auto> [-t type] [-w] [-n] [-m model] [-c] "request"`
- The single way for one agent to hand work to another. Read-only by default; `-w` allows writing.
- `-t` sets the task type; with `auto`, the chain picks who does it:

| Type (`-t`) | Chain |
|---|---|
| `pesquisa` (research), `documento` (document) | Gemini → Claude → Codex |
| `termux`, `rede` (network), `codigo` (code) | Codex → Claude → Gemini |
| `revisao` (review) | Codex → Gemini → Claude |
| `outro` (other) | Claude → Codex → Gemini |

- **Automatic armband handover:** if an agent hits its limit (or is at ≥90%), the request goes to the next one in the chain and the agent is "benched" (Claude/Codex 5 h, Gemini 12 h). Check with `pedir --estado`.
- `-m` picks the model for that call; `-c` continues the previous conversation without resending context; `-n` disables handover.
- If the connection drops mid-answer, it retries once. Every call is logged to `consumo.csv`.

### 📊 `saldo`: account balance, at 0 tokens
- Claude: reads the `/usage` screen in a hidden tmux session (~15 s).
- Codex: reads the rate limits saved in its last session.
- Gemini: not measured yet.
- Saves to `saldo.json`, which `pedir` uses to hand over the armband **before** the limit is hit.

### 📈 `rever-consumo`: usage report
- Combines agent-to-agent calls with Claude/Codex sessions (last 7 days by default).
- Used to tune the routing chains.

### 🛡️ Under the hood
- Sandbox policies (read-only/write) for Antigravity and Gemini.
- 11 offline automated tests.
- Change history in [`CHANGELOG.md`](CHANGELOG.md) (Portuguese).

## Quick start
```
pedir codex -t revisao "review bin/x:10-40"     # new call, read-only
pedir codex -c "and line 55?"                   # continue the same conversation (no context resent)
pedir claude -m haiku "summarise this log"      # model per call
pedir --estado                                  # who is benched
python3 tests/test-pedir-gemini.py              # offline regression tests (no tokens spent)
```
