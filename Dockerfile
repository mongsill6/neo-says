FROM python:3.11-slim AS base

WORKDIR /app

RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

COPY pyproject.toml .
RUN pip install --no-cache-dir .[server]

COPY src/ src/
COPY data/ data/
COPY sample-packs/ sample-packs/

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["python", "-m", "neo_says.server"]
