export type NodeName = "planner" | "researcher" | "critic" | "writer";
export type Confidence = "high" | "medium" | "low";

export interface SubQuestion { id: string; text: string; status: "pending" | "researching" | "done" | "weak" }
export interface Source { url: string; domain: string; snippet: string }
export interface Finding { questionId: string; claim: string; source: Source; confidence: Confidence }
export interface GraphNode { id: string; node: NodeName; label: string; status: "running" | "done" }

export type RunEvent =
  | { type: "node_start"; node: NodeName; id: string; label?: string }
  | { type: "node_end"; node: NodeName; id: string }
  | ({ type: "finding" } & Finding)
  | { type: "critique"; questionId: string; verdict: "supported" | "weak" | "unsupported" }
  | { type: "interrupt"; kind: "outline_approval"; outline: SubQuestion[] }
  | { type: "report"; markdown: string; sources: Source[] }
  | { type: "done" };
