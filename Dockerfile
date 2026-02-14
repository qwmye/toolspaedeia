FROM astral/uv:python3.13-trixie-slim

WORKDIR /app/

COPY pyproject.toml uv.lock /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install git and ruff
RUN apt-get update && apt-get install -y git \
	&& pip install ruff \
	&& rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked
ENV PATH="/app/.venv/bin:$PATH"

COPY . /app

WORKDIR /app/toolspaedeia

CMD ["uv", "run", "uvicorn", "toolspaedeia.asgi:application", "--host", "0.0.0.0", "--port", "8888", "--reload"]
