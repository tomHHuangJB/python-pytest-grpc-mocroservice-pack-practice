FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY proto ./proto

RUN python -m pip install --upgrade pip && \
    pip install -e .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "order_app.api:app", "--host", "0.0.0.0", "--port", "8000"]
