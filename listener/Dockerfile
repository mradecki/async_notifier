FROM python:3.9-slim

RUN apt-get update && apt-get install -y wait-for-it && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

ENV PYTHONUNBUFFERED 1

CMD ["python", "main.py"]
