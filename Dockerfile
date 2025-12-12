FROM astral/uv:python3.13-trixie-slim

WORKDIR /app/

COPY pyproject.toml uv.lock /app

ENV UV_COMPILE_BYTECODE 1
ENV UV_LINK_MODE copy

# deps
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked
ENV PATH="/app/.venv/bin:$PATH"

COPY . /app

WORKDIR /app/toolspaedeia

CMD ["uvicorn", "toolspaedeia.asgi:application", "--host", "0.0.0.0", "--port", "8888", "--reload"]
