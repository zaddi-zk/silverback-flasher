FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

EXPOSE 5000

# Launch the Flask web backend. Use this container on Python hosts or Docker deployments.
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120"]
