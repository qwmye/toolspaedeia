FROM astral/uv:python3.13-trixie-slim

COPY . /app
WORKDIR /app/toolspaedeia/

# deps
RUN uv sync --locked
ENV PATH="/app/.venv/bin:$PATH"

# migrations
RUN ./manage.py migrate
