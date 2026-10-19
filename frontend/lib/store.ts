import { create } from "zustand";
import type { RunEvent, SubQuestion, Finding, GraphNode, Source } from "./types";

interface RunState {
  nodes: Record<string, GraphNode>;
  feed: string[];
  findings: Finding[];
  outline: SubQuestion[];
  awaiting: boolean;
  report: string;
  sources: Source[];
  done: boolean;
  reset: () => void;
  apply: (e: RunEvent) => void;
}

const init = { nodes: {}, feed: [], findings: [], outline: [], awaiting: false, report: "", sources: [], done: false };

const setQ = (o: SubQuestion[], id: string, status: SubQuestion["status"]) =>
  o.map((q) => (q.id === id ? { ...q, status } : q));

export const useRun = create<RunState>((set) => ({
  ...init,
  reset: () => set({ ...init }),
  apply: (e) =>
    set((s) => {
      switch (e.type) {
        case "node_start": {
          const label = e.label ?? e.node;
          const outline = e.node === "researcher" ? setQ(s.outline, e.id.slice(2), "researching") : s.outline;
          return {
            outline,
            nodes: { ...s.nodes, [e.id]: { id: e.id, node: e.node, label, status: "running" } },
            feed: [...s.feed, `${label} started`],
          };
        }
        case "node_end": {
          const n = s.nodes[e.id];
          const outline = e.node === "researcher" ? setQ(s.outline, e.id.slice(2), "done") : s.outline;
          return { outline, nodes: n ? { ...s.nodes, [e.id]: { ...n, status: "done" } } : s.nodes };
        }
        case "finding":
          return { findings: [...s.findings, e], feed: [...s.feed, `Found evidence on ${e.source.domain}`] };
        case "critique":
          return {
            outline: e.verdict === "supported" ? s.outline : setQ(s.outline, e.questionId, "weak"),
            feed: [...s.feed, e.verdict === "supported" ? `Critic accepted ${e.questionId}` : `Critic flagged ${e.questionId} as ${e.verdict}, sending it back`],
          };
        case "interrupt":
          return { outline: e.outline, awaiting: true, feed: [...s.feed, "Outline ready, waiting for your approval"] };
        case "report":
          return { report: e.markdown, sources: e.sources };
        case "done":
          return { done: true, feed: [...s.feed, "Report complete"] };
      }
    }),
}));
