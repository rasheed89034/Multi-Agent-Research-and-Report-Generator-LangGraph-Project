import { Handle, Position, type NodeProps } from "@xyflow/react";
import { Brain, Search, Scale, PenLine, Loader2, Check } from "lucide-react";

const icons = { planner: Brain, researcher: Search, critic: Scale, writer: PenLine } as const;
type Data = { label: string; kind: keyof typeof icons; status: "idle" | "running" | "done" };

export default function AgentNode({ data }: NodeProps) {
  const { label, kind, status } = data as Data;
  const Icon = icons[kind];
  const ring = status === "running" ? "border-indigo-400 shadow-[0_0_24px_rgba(99,102,241,.5)]" : status === "done" ? "border-emerald-500/60" : "border-white/10";
  return (
    <div className={`glass flex w-40 items-center gap-2 px-3 py-2.5 text-sm ${ring}`}>
      <Handle type="target" position={Position.Left} className="!bg-white/30" />
      <Icon size={16} className={status === "idle" ? "text-[var(--muted)]" : "text-indigo-300"} />
      <span className="flex-1 truncate">{label}</span>
      {status === "running" && <Loader2 size={14} className="animate-spin text-indigo-300" />}
      {status === "done" && <Check size={14} className="text-emerald-400" />}
      <Handle type="source" position={Position.Right} className="!bg-white/30" />
    </div>
  );
}
