# Release Notes

All notable changes to Bifrost are documented here.

---

## [v0.4.0] — 2026-05-24

### Added
- **Neon PostgreSQL** — notes-api now persists data in a real database instead of in-memory storage. Uses SQLAlchemy 2.0 + psycopg2-binary with `NullPool` (serverless-safe). Table auto-created on cold start.
- **Vercel Analytics** — injected `/_vercel/insights/script.js` into the HTML landing page to track page views and visitors.
- **HTML Landing Page** — root `/` now serves a styled dark-mode HTML page listing all live services with links to their Swagger docs, replacing the plain JSON registry.
- **Vercel Speed Insights** — injected `/_vercel/speed-insights/script.js` to track Core Web Vitals (LCP, FID, CLS).

### Changed
- **Project renamed** from `python-turborepo` to **Bifrost** across GitHub repo, pyproject.toml, README, docs, config, and API registry.
- **Vercel URL** updated to `bifrost-api.vercel.app`.

---

## [v0.3.0] — 2026-05-24

### Added
- **API Registry** — `GET /` returns a live list of all deployed services with base paths, docs URLs, and available endpoints.

---

## [v0.2.0] — 2026-05-24

### Added
- **Code Reviewer** (`apps/code-reviewer/`) — `POST /code-review` accepts code + language and returns a structured JSON review with score (1–10), issues (type/severity/description/suggestion), strengths, and recommendation. Powered by Groq's free tier using `llama-3.3-70b-versatile`.
- **Automated release workflow** — pushing a `v*.*.*` tag now automatically creates a GitHub release with a changelog generated from commits since the previous tag.

### Changed
- Switched from Anthropic SDK to **Groq** (free tier) for the code reviewer to remove cost dependency.

---

## [v0.1.0] — 2026-05-24

### Added
- **Initial monorepo scaffold** using `uv` workspaces.
- **apps/hello-api** — quotes, UUID, and timestamp endpoints. Live at `/`.
- **apps/notes-api** — full CRUD notes API (in-memory at this point). Live at `/notes`.
- **apis/gateway** — streaming chat endpoint via Anthropic SDK.
- **apis/webhooks** — webhook event receiver.
- **agents/research-agent** — LangGraph pipeline: researcher → synthesizer.
- **agents/coding-agent** — LangGraph pipeline: coder → reviewer.
- **mcp-servers/knowledge-base** — search tool + status resource via FastMCP.
- **mcp-servers/code-runner** — executes Python snippets in a subprocess via FastMCP.
- **packages/core** — Pydantic settings, structured logging, shared types.
- **packages/llm** — Anthropic client + streaming helpers.
- **packages/tools** — web search, file ops, memory tools.
- **Vercel multi-app routing** via root `vercel.json`.
- **Dockerfiles** for all APIs, agents, and MCP servers.
- **GitHub Actions CI** for gateway, research-agent, coding-agent.
- **Docs** — HLD, LLD, and GUIDE covering architecture and developer workflows.
