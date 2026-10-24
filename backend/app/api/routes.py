import asyncio
import json
from uuid import uuid4
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from langgraph.types import Command
from app.api.runner import Run, drive
from app.schemas.models import ResumeRun, StartRun

router = APIRouter(prefix="/api")
RUNS: dict[str, Run] = {}


def _cfg(run_id: str) -> dict:
    return {"configurable": {"thread_id": run_id}}


@router.post("/runs")
async def start_run(body: StartRun, request: Request):
    run_id = body.run_id or uuid4().hex[:8]
    if run_id in RUNS:
        raise HTTPException(409, "Run already exists")
    run = RUNS[run_id] = Run(body.topic, body.depth)
    asyncio.create_task(drive(run, request.app.state.graph, _cfg(run_id), {"topic": body.topic, "depth": body.depth}))
    return {"run_id": run_id}


@router.get("/runs/{run_id}/stream")
async def stream(run_id: str):
    run = RUNS.setdefault(run_id, Run())

    async def gen():
        async for e in run.subscribe():
            yield ": ping\n\n" if e is None else f"data: {json.dumps(e)}\n\n"

    return StreamingResponse(gen(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@router.post("/runs/{run_id}/resume")
async def resume(run_id: str, body: ResumeRun, request: Request):
    graph = request.app.state.graph
    snap = await graph.aget_state(_cfg(run_id))
    if not snap.next:
        raise HTTPException(409, "Run is not waiting for approval")
    run = RUNS.setdefault(run_id, Run())   # also works after a server restart: state comes from the checkpoint
    run.status = "running"
    outline = [q.model_dump() for q in body.outline]
    asyncio.create_task(drive(run, graph, _cfg(run_id), Command(resume=outline)))
    return {"ok": True}


@router.get("/runs")
async def list_runs():
    return [{"id": k, "topic": v.topic, "status": v.status} for k, v in RUNS.items()]


@router.get("/runs/{run_id}")
async def get_run(run_id: str, request: Request):
    snap = await request.app.state.graph.aget_state(_cfg(run_id))
    if not snap.values:
        raise HTTPException(404, "Unknown run")
    v = snap.values
    return {"id": run_id, "topic": v.get("topic"), "paused": bool(snap.next), "outline": v.get("outline"),
            "report": v.get("report"), "sources": v.get("sources")}
