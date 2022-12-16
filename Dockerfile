FROM registry.access.redhat.com/ubi9/python-39
ARG POETRY_VERSION

RUN pip install --upgrade pip && \
    pip install poetry==$POETRY_VERSION
COPY --chown=1000 skupper_prometheus_collector skupper_prometheus_collector
COPY --chown=1000 README.md pyproject.toml poetry.* ./
RUN poetry install
USER 1000
CMD [".venv/bin/skupper-prometheus-collector"]
