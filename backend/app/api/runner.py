import asyncio
from langgraph.graph.state import CompiledStateGraph


class Run:
    """In-memory event log + live subscribers for one run. The graph state itself lives in the SQLite checkpointer."""

    def __init__(self, topic: str = "", depth: str = ""):
        self.topic, self.depth, self.status = topic, depth, "running"
        self.events: list[dict] = []
        self.subs: list[asyncio.Queue] = []

    def push(self, event: dict):
        self.events.append(event)
        for q in self.subs:
            q.put_nowait(event)

    async def subscribe(self):
        q: asyncio.Queue = asyncio.Queue()
        for e in self.events:          # replay history so a refreshed page catches up
            q.put_nowait(e)
        self.subs.append(q)
        try:
            while True:
                try:
                    e = await asyncio.wait_for(q.get(), timeout=15)
                except asyncio.TimeoutError:
                    yield None         # keep-alive while paused for approval
                    continue
                yield e
                if e["type"] in ("done", "error"):
                    return
        finally:
            self.subs.remove(q)


async def drive(run: Run, graph: CompiledStateGraph, config: dict, payload):
    """Runs the graph until it finishes or pauses at the approval interrupt, pushing UI events as it goes."""
    try:
        async for mode, chunk in graph.astream(payload, config, stream_mode=["custom", "updates"]):
            if mode == "custom":
                run.push(chunk)
            elif "__interrupt__" in chunk:
                run.status = "paused"
                run.push({"type": "interrupt", **chunk["__interrupt__"][0].value})
                return
        run.status = "completed"
        run.push({"type": "done"})
    except Exception as e:  # surface failures to the UI instead of hanging the stream
        run.status = "failed"
        run.push({"type": "error", "message": str(e)})
