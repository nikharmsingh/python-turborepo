# High Level Design (HLD)

## What is Turborepo?

Turborepo is a **build system for JavaScript/TypeScript monorepos** created by Vercel. A monorepo is a single Git repository that holds multiple projects (apps, libraries, services) instead of one repo per project.

Turborepo solves three core problems in monorepos:

| Problem | How Turborepo solves it |
|---|---|
| Shared code between apps | npm/yarn/pnpm **workspaces** — packages reference each other locally |
| Slow builds | **Task caching** — if inputs didn't change, skip the task |
| Parallel work | **Task pipeline** — runs tasks in parallel where dependencies allow |

### Turborepo's typical JS structure

```
my-turborepo/
├── turbo.json           ← task pipeline config (build, test, lint)
├── package.json         ← workspace root
├── packages/
│   ├── ui/              ← shared React component library
│   └── config/          ← shared ESLint/TS config
└── apps/
    ├── web/             ← Next.js frontend
    └── api/             ← Express backend
```

Apps import shared packages: `import { Button } from "@repo/ui"`.
Turborepo builds `ui` before `web` because `web` depends on it.

---

## What is this repo?

This repo is the **Python equivalent** of a Turborepo monorepo. It uses `uv` (Python's modern package manager) in workspace mode to achieve the same goals — shared code, isolated apps, single lockfile — without the JavaScript toolchain.

```
python-turborepo/
├── pyproject.toml       ← workspace root (uv replaces turbo.json + package.json)
├── uv.lock              ← single lockfile for all packages (like pnpm-lock.yaml)
├── packages/            ← shared libraries (imported by apps)
│   ├── core/
│   ├── llm/
│   └── tools/
├── apps/                ← deployable web services
│   ├── hello-api/
│   └── notes-api/
├── apis/                ← internal backend services
│   ├── gateway/
│   └── webhooks/
├── agents/              ← LangGraph AI agents
│   ├── research-agent/
│   └── coding-agent/
└── mcp-servers/         ← Model Context Protocol servers
```

---

## How this repo maps to Turborepo concepts

| Turborepo (JS) | This repo (Python) | Purpose |
|---|---|---|
| `package.json` workspaces | `pyproject.toml` `[tool.uv.workspace]` | Declares all packages in the monorepo |
| `pnpm-lock.yaml` | `uv.lock` | Single lockfile at repo root |
| `packages/ui` | `packages/core`, `llm`, `tools` | Shared libraries imported by apps |
| `apps/web` | `apps/hello-api`, `apps/notes-api` | Deployable applications |
| `import "@repo/ui"` | `from core.config import Settings` | Cross-package imports |
| `turbo build` | `uv run --package gateway uvicorn ...` | Run a specific app |
| Turborepo task cache | — (not implemented; uv has no task runner) | Build caching |
| Vercel integration | Vercel + `vercel.json` | Deployment |

> **Key difference:** Turborepo adds a task graph and remote build cache on top of workspaces. This Python repo uses only the workspace layer — `uv` resolves and installs packages but does not cache task outputs. For Python, this is rarely needed because there are no compilation steps.

---

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   GitHub Repository                  │
│                  (single git repo)                   │
└──────────────────────────┬──────────────────────────┘
                           │ push to main
                           ▼
┌─────────────────────────────────────────────────────┐
│                  Vercel Platform                     │
│                                                      │
│  vercel.json (root)                                  │
│  ┌─────────────────┐    ┌──────────────────────┐    │
│  │  /notes(.*)     │───▶│  notes-api function  │    │
│  │                 │    │  apps/notes-api/     │    │
│  └─────────────────┘    └──────────────────────┘    │
│  ┌─────────────────┐    ┌──────────────────────┐    │
│  │  /(.*)          │───▶│  hello-api function  │    │
│  │  (catch-all)    │    │  apps/hello-api/     │    │
│  └─────────────────┘    └──────────────────────┘    │
└─────────────────────────────────────────────────────┘
                           │
                           ▼
              python-turborepo.vercel.app


┌──────────────────────────────────────────┐
│          Local Development               │
│                                          │
│  packages/core  ◀──┐                    │
│  packages/llm   ◀──┼── gateway          │
│  packages/tools ◀──┤                    │
│                    ├── research-agent   │
│                    └── coding-agent     │
│                                          │
│  uv workspace resolves all deps from     │
│  a single uv.lock at repo root           │
└──────────────────────────────────────────┘
```

---

## Technology Choices

| Layer | Tool | Why |
|---|---|---|
| Workspace manager | `uv` | Fastest Python package manager; native workspace support; single lockfile |
| Web framework | FastAPI | Async, Pydantic-native, auto OpenAPI docs |
| Agent framework | LangGraph | Stateful multi-step agent graphs |
| LLM SDK | Anthropic Python SDK | Claude model access |
| MCP servers | FastMCP | Model Context Protocol for tool-use |
| Deployment | Vercel | Zero-config serverless Python functions |
| Build backend | hatchling | Lightweight; PEP 517 compliant |

---

## Deployment Strategy

Apps in `apps/` are deployed as **Vercel Serverless Functions** (stateless, auto-scaling).
Apps in `apis/` and `agents/` are intended for **containerised deployment** (Docker + cloud run) where persistent state or longer execution time is needed.

```
apps/          → Vercel (serverless, stateless)
apis/          → Docker / Cloud Run (long-running)
agents/        → Docker / Cloud Run (long-running, stateful graphs)
mcp-servers/   → stdio process (Claude Desktop / Claude Code)
```
