FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -e .
EXPOSE 8080
CMD ["python", "-m", "incident_intelligence.api"]
