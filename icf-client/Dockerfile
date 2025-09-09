FROM python:3.12-slim

WORKDIR /app
COPY app/requirements.txt .
RUN apt-get update && apt-get install -y libpq-dev gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove gcc \
    && rm -rf /var/lib/apt/lists/*

COPY app ./app
ENV PYTHONUNBUFFERED=1
CMD ["python", "app/main.py"]
