import type { RunEvent, SubQuestion } from "./types";

const wait = (ms: number) => new Promise((r) => setTimeout(r, ms));
const src = (domain: string, snippet: string) => ({ url: `https://${domain}/article`, domain, snippet });

// Plays a fake run. `approval` resolves with the user's edited outline.
export async function runMock(topic: string, emit: (e: RunEvent) => void, approval: Promise<SubQuestion[]>, cancelled: () => boolean) {
  const step = async (ms: number, e?: RunEvent) => { await wait(ms); if (!cancelled() && e) emit(e); };

  await step(300, { type: "node_start", node: "planner", id: "planner", label: "Planner" });
  await step(1200, { type: "node_end", node: "planner", id: "planner" });
  const draft: SubQuestion[] = [
    { id: "q1", text: `What is the current state of ${topic}?`, status: "pending" },
    { id: "q2", text: "What are the main technical approaches and trade-offs?", status: "pending" },
    { id: "q3", text: "What risks and open problems remain?", status: "pending" },
  ];
  await step(0, { type: "interrupt", kind: "outline_approval", outline: draft });
  const outline = await approval;
  if (cancelled()) return;

  for (const q of outline) emit({ type: "node_start", node: "researcher", id: `r-${q.id}`, label: `Researcher ${q.id.slice(1)}` });
  for (const [i, q] of outline.entries()) {
    await step(900, { type: "finding", questionId: q.id, claim: `Key claim for “${q.text.slice(0, 40)}…”`, confidence: i === 1 ? "low" : "high",
      source: src(["arxiv.org", "nature.com", "mit.edu"][i % 3], "Supporting passage extracted from the page…") });
    await step(400, { type: "node_end", node: "researcher", id: `r-${q.id}` });
  }
  await step(300, { type: "node_start", node: "critic", id: "critic", label: "Critic" });
  await step(1000, { type: "critique", questionId: outline[0]?.id, verdict: "supported" });
  const weak = outline[1];
  if (weak) {
    await step(300, { type: "critique", questionId: weak.id, verdict: "weak" });
    await step(300, { type: "node_start", node: "researcher", id: `r-${weak.id}`, label: `Researcher ${weak.id.slice(1)} (retry)` });
    await step(1200, { type: "finding", questionId: weak.id, claim: "Stronger evidence found on retry.", confidence: "high", source: src("openreview.net", "Benchmark results confirm…") });
    await step(300, { type: "node_end", node: "researcher", id: `r-${weak.id}` });
    await step(600, { type: "critique", questionId: weak.id, verdict: "supported" });
  }
  await step(300, { type: "node_end", node: "critic", id: "critic" });
  await step(200, { type: "node_start", node: "writer", id: "writer", label: "Writer" });
  await step(1500, { type: "report", sources: [src("arxiv.org", "Supporting passage…"), src("nature.com", "Supporting passage…"), src("openreview.net", "Benchmark results confirm…")],
    markdown: `# ${topic}\n\n## Overview\nThe field has matured quickly, with several approaches now in production [1]. Evidence from peer-reviewed work supports this view [2].\n\n## Approaches and trade-offs\nBenchmarks show clear differences between methods once evaluated on harder tasks [3].\n\n## Open problems\nReliability and cost remain the main barriers [1][3].` });
  await step(300, { type: "node_end", node: "writer", id: "writer" });
  await step(200, { type: "done" });
}
