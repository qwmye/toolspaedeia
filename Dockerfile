FROM astral/uv:python3.13-trixie-slim

COPY . /app
WORKDIR /app/toolspaedeia/

# deps
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked
ENV PATH="/app/.venv/bin:$PATH"

# static files
RUN ./manage.py collectstatic
