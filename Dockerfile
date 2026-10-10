FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml ./
COPY fraud_email ./fraud_email
COPY api ./api
RUN pip install --no-cache-dir '.[api]'
RUN useradd --create-home appuser
USER appuser
EXPOSE 8000
CMD ["uvicorn","api.app:app","--host","0.0.0.0","--port","8000"]
