# Multi-Agent Research and Report Generator (LangGraph)

An interactive, agentic research and report generation system powered by LangGraph and Next.js. The system coordinates multiple specialized AI agents to plan, execute, critique, and write in-depth, citation-backed research reports with human-in-the-loop outline approval.

---

## 🚀 Overview

The system breaks complex research tasks into discrete stages executed by specialized agents:

1. **Planner Agent**: Analyzes the topic and generates a structured research outline composed of key sub-questions.
2. **Human-in-the-Loop Approval**: Allows the user to review, reorder, add, or refine outline topics before deep research commences.
3. **Researcher Agents**: Investigate sub-questions in parallel, gathering facts, quotes, confidence scores, and source URLs.
4. **Critic Agent**: Reviews collected findings, identifies gaps or unsubstantiated claims, and requests revisions when necessary.
5. **Writer Agent**: Synthesizes verified findings into a cohesive, comprehensive Markdown report complete with source citations.

---

## 📂 Repository Structure

```text
.
├── .gitignore
├── README.md
└── frontend/                   # Next.js App Router frontend
    ├── app/                    # Pages, layouts, and route handlers
    │   ├── page.tsx            # Topic input & research depth selector
    │   ├── layout.tsx          # Root layout and theme provider
    │   ├── globals.css         # Styling, glassmorphic effects, and variables
    │   └── runs/[id]/          # Live run dashboard (graph, feed, report)
    ├── components/             # UI components
    │   ├── feed/               # Live agent activity feed & logs
    │   ├── evidence/           # Collected findings & source citations
    │   ├── graph/              # React Flow interactive agent DAG
    │   ├── outline/            # Drag-and-drop outline approval editor
    │   └── report/             # Rendered markdown report viewer
    ├── lib/                    # State management and event streaming
    │   ├── mock.ts             # Simulated agent event stream
    │   ├── store.ts            # Zustand global state store
    │   ├── types.ts            # Event and node type definitions
    │   └── useRunStream.ts     # SSE connection and event handling
    ├── package.json
    └── tsconfig.json
```

---

## ✨ Features

- **Live Agent Graph (DAG)**: Interactive visualization of the agent execution graph built with `@xyflow/react`.
- **Real-Time Event Stream**: Server-Sent Events (SSE) stream agent steps, critiques, and findings as they occur.
- **Interactive Outline Review**: Drag-and-drop sub-question reordering and editing using `@dnd-kit`.
- **Evidence & Source Verification**: Transparent evidence cards displaying confidence ratings and clickable references.
- **Full Report Generation**: Clean Markdown rendering with export and source citation support.
- **Built-in Mock Mode**: Test and develop the frontend without a live backend connection.

---

## 🛠️ Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (v18 or higher recommended)
- `npm` or `pnpm` / `yarn`

### Setup and Running

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

4. **Open the application**:
   Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## ⚙️ Configuration

By default, the frontend runs in **Mock Mode** using realistic simulated agent events.

To connect to your live LangGraph backend:
1. In `frontend/lib/useRunStream.ts`, set `NEXT_PUBLIC_USE_MOCK=false` (or create a `.env.local` file with `NEXT_PUBLIC_USE_MOCK=false`).
2. Ensure your backend exposes the SSE streaming endpoint at `/api/runs/[id]/stream` and resume endpoint at `/api/runs/[id]/resume`.
>>>>>>> ef86ac4 (Initial commit: Multi-Agent Research and Report Generator with LangGraph and Next.js)
