# Memory Layer for LLM Chats (Cognee Hackathon Project)

> Built for the **Hangover Part AI** hackathon by WeMakeDevs — theme: AI memory using [Cognee](https://www.cognee.ai/).

## The problem

Every new chat with an LLM starts from zero. You re-explain who you are, what
you're working on, what you already decided last week, and what your
preferences are — every single time. This project removes that tax.

## The idea

A memory layer that sits **between the user and an LLM**, so the model
always has the right context without the user repeating themselves. It
remembers preferences, ongoing projects, and past decisions across sessions,
using Cognee's four-verb memory lifecycle:

| Verb | What it does here |
|---|---|
| `remember()` | Stores new facts, preferences, and decisions from the conversation |
| `recall()` | Retrieves relevant memory before each LLM call, to inject as context |
| `improve()` | Consolidates/refines stored memory over time (e.g. merging duplicate or outdated facts) |
| `forget()` | Removes specific memories on request (user-controlled deletion) |

## How it works (high level)

```
User message
   │
   ▼
recall()  ──► relevant memories pulled from Cognee
   │
   ▼
Inject memories into the prompt as context
   │
   ▼
LLM call (Gemini)
   │
   ▼
remember()  ──► new facts from this exchange get stored
   │
   ▼
Response shown to user
```

A visible "What the AI remembers about you" panel shows the current memory
state at any time, so the effect is demonstrable, not just claimed.

## Status

This project is being built incrementally over 5 days. Checklist below is
updated as steps are completed.

- [x] Environment setup (Python, Gemini API key, Cognee account)
- [x] Cognee configured + basic remember/recall round-trip verified
- [~] Core memory loop in terminal (recall → inject → LLM call → remember) — built, currently debugging a live end-to-end test
- [ ] Manual memory commands (`/remember`, `/forget`)
- [ ] Memory consolidation via `improve()`
- [ ] Chat UI (Streamlit/Gradio or React)
- [ ] "What the AI remembers about you" visible panel
- [ ] Demo persona + before/after demo script
- [ ] Polish + this README finalized
- [ ] Demo video + submission

## Tech stack

- **LLM:** Gemini (Google AI Studio, free tier)
- **Memory:** [Cognee](https://www.cognee.ai/) (remember / recall / improve / forget)
- **UI:** TBD (Streamlit, Gradio, or React — decided in Step 6)
- **Language:** Python

## Setup

1. Clone this repo and create a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate   # Windows
   ```
2. Install dependencies:
   ```bash
   pip install cognee "cognee[neo4j]" python-dotenv google-generativeai
   ```
3. Copy `.env.example` to `.env` and fill in your real values:
   - A free Gemini API key from [Google AI Studio](https://aistudio.google.com)
   - A local Neo4j database (via [Neo4j Desktop](https://neo4j.com/download)) with the APOC plugin installed, running on the default `bolt://localhost:7687`
4. Make sure your Neo4j database instance is **started** in Neo4j Desktop before running any script.
5. Run the core chat loop:
   ```bash
   python chat_loop.py
   ```

## Why Cognee for chat-shaped memory?

Cognee is graph-backed, which is naturally suited to entities and
relationships (documents, codebases, org charts). A simpler flat memory
store could also solve "remember what the user said." We chose Cognee
specifically to take advantage of its knowledge-graph structure for
**connecting related facts across sessions** — e.g. linking a user's stated
preference to the specific project it applies to, rather than just storing
flat, disconnected facts. This tradeoff is discussed further in the final
write-up.

## Demo persona

_To be defined in Step 8 — a fictional user with a recurring project and a
few stable preferences, used to show a believable "before" (no memory) vs
"after" (memory-aware) conversation._

## License

TBD
