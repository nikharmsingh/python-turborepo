FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock .python-version ./
COPY packages/core          ./packages/core
COPY mcp-servers/code-runner ./mcp-servers/code-runner

RUN pip install uv && \
    uv sync --package code-runner --frozen --no-dev

EXPOSE 8000

CMD ["uv", "run", "--package", "code-runner", "python", "src/server.py"]
