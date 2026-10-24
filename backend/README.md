# Research Desk backend

Requires Python 3.11+.

    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env        # add your LLM key (e.g. ANTHROPIC_API_KEY or XAI_API_KEY)
    uvicorn app.main:app --reload --port 8000

Check http://localhost:8000/health, then run `python -m pytest` and `python -m evals.citation_check`.

Other LLM providers: install e.g. `langchain-google-genai` and set `LLM_MAIN=google_genai:<model>` and `LLM_FAST=google_genai:<model>` in `.env`.

| Endpoint | Purpose |
|---|---|
| POST /api/runs | start a run `{topic, depth, run_id?}` |
| GET /api/runs/{id}/stream | SSE of UI events (replays history, stays open while paused) |
| POST /api/runs/{id}/resume | send the approved outline `{outline: [{id, text}]}` |
| GET /api/runs, GET /api/runs/{id} | history, state from checkpoint |
