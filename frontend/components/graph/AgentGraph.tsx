"use client";
import { useMemo } from "react";
import { ReactFlow, Background, type Node, type Edge } from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import AgentNode from "./AgentNode";
import { useRun } from "@/lib/store";

const nodeTypes = { agent: AgentNode };

export default function AgentGraph() {
  const nodes = useRun((s) => s.nodes);
  const { rfNodes, rfEdges } = useMemo(() => {
    const st = (id: string) => nodes[id]?.status ?? "idle";
    const researchers = Object.values(nodes).filter((n) => n.node === "researcher");
    const mid = Math.max(researchers.length - 1, 0) * 35;
    const rfNodes: Node[] = [
      { id: "planner", type: "agent", position: { x: 0, y: mid }, data: { label: "Planner", kind: "planner", status: st("planner") } },
      ...researchers.map((r, i): Node => ({ id: r.id, type: "agent", position: { x: 230, y: i * 70 }, data: { label: r.label, kind: "researcher", status: r.status } })),
      { id: "critic", type: "agent", position: { x: 470, y: mid }, data: { label: "Critic", kind: "critic", status: st("critic") } },
      { id: "writer", type: "agent", position: { x: 700, y: mid }, data: { label: "Writer", kind: "writer", status: st("writer") } },
    ];
    const e = (a: string, b: string, animated = false): Edge => ({ id: `${a}-${b}`, source: a, target: b, animated, style: { stroke: "rgba(255,255,255,.25)" } });
    const rfEdges = [
      ...researchers.flatMap((r) => [e("planner", r.id, r.status === "running"), e(r.id, "critic", st("critic") === "running")]),
      ...(researchers.length ? [] : [e("planner", "critic")]),
      e("critic", "writer", st("writer") === "running"),
    ];
    return { rfNodes, rfEdges };
  }, [nodes]);

  return (
    <div className="glass h-80 overflow-hidden">
      <ReactFlow nodes={rfNodes} edges={rfEdges} nodeTypes={nodeTypes} fitView fitViewOptions={{ padding: 0.2 }}
        nodesDraggable={false} nodesConnectable={false} proOptions={{ hideAttribution: true }}>
        <Background color="rgba(255,255,255,.06)" gap={24} />
      </ReactFlow>
    </div>
  );
}
