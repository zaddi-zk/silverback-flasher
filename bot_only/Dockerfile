### Multi-stage Dockerfile: build dependencies in a temporary stage
FROM python:3.11-slim AS build
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

### Final image: minimal runtime with non-root user
FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
ENV PATH=/usr/local/bin:$PATH
WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

# Copy installed packages from the build stage
COPY --from=build /install /usr/local

# Copy only the needed application files
COPY bot.py ./

RUN chown -R app:app /app
USER app

CMD ["python", "bot.py"]
