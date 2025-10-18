FROM python:3.11-slim AS build
RUN apt-get update && apt-get install -y build-essential
RUN pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir -r requirements.txt -w /wheels

FROM python:3.11-slim
WORKDIR /app
RUN --mount=type=bind,from=build,source=/wheels,target=/wheels,ro pip install --no-cache-dir /wheels/*
COPY . .

CMD ["python3", "display.py"]
