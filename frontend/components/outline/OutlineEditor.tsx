"use client";
import { useState } from "react";
import { DndContext, closestCenter, type DragEndEvent } from "@dnd-kit/core";
import { SortableContext, useSortable, arrayMove, verticalListSortingStrategy } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { GripVertical, Trash2, Plus } from "lucide-react";
import type { SubQuestion } from "@/lib/types";

function Row({ q, onChange, onDelete }: { q: SubQuestion; onChange: (t: string) => void; onDelete: () => void }) {
  const { attributes, listeners, setNodeRef, transform, transition } = useSortable({ id: q.id });
  return (
    <div ref={setNodeRef} style={{ transform: CSS.Transform.toString(transform), transition }} className="glass flex items-center gap-2 p-2">
      <button {...attributes} {...listeners} aria-label="Reorder" className="cursor-grab p-1 text-[var(--muted)]"><GripVertical size={16} /></button>
      <input value={q.text} onChange={(e) => onChange(e.target.value)} className="flex-1 bg-transparent py-1 outline-none" />
      <button onClick={onDelete} aria-label="Remove question" className="p-1 text-[var(--muted)] hover:text-rose-400"><Trash2 size={16} /></button>
    </div>
  );
}

export default function OutlineEditor({ initial, onApprove }: { initial: SubQuestion[]; onApprove: (o: SubQuestion[]) => void }) {
  const [items, setItems] = useState(initial);
  const onDragEnd = ({ active, over }: DragEndEvent) => {
    if (over && active.id !== over.id)
      setItems((l) => arrayMove(l, l.findIndex((i) => i.id === active.id), l.findIndex((i) => i.id === over.id)));
  };
  return (
    <section className="glass p-5">
      <h2 className="text-lg font-semibold">Review the research plan</h2>
      <p className="mb-4 mt-1 text-sm text-[var(--muted)]">Edit, reorder, remove or add questions. Each one gets its own researcher.</p>
      <DndContext collisionDetection={closestCenter} onDragEnd={onDragEnd}>
        <SortableContext items={items.map((i) => i.id)} strategy={verticalListSortingStrategy}>
          <div className="space-y-2">
            {items.map((q) => (
              <Row key={q.id} q={q}
                onChange={(t) => setItems((l) => l.map((i) => (i.id === q.id ? { ...i, text: t } : i)))}
                onDelete={() => setItems((l) => l.filter((i) => i.id !== q.id))} />
            ))}
          </div>
        </SortableContext>
      </DndContext>
      <div className="mt-4 flex justify-between">
        <button onClick={() => setItems((l) => [...l, { id: `q${Date.now() % 10000}`, text: "", status: "pending" }])}
          className="flex items-center gap-1 text-sm text-indigo-300"><Plus size={14} />Add question</button>
        <button className="btn" disabled={!items.some((i) => i.text.trim())} onClick={() => onApprove(items.filter((i) => i.text.trim()))}>Approve and start</button>
      </div>
    </section>
  );
}
