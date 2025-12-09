FROM astral/uv:python3.13-trixie-slim

COPY . /app
WORKDIR /app/toolspaedeia/

ENV UV_LINK_MODE copy

# deps
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked
ENV PATH="/app/.venv/bin:$PATH"

# static files
RUN ./manage.py collectstatic

ENTRYPOINT ["uvicorn", "toolspaedeia.asgi:application", "--host", "0.0.0.0", "--port", "8888", "--reload"]
