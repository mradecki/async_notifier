# Use an official Python runtime as the parent image
FROM python:3.9-slim

RUN apt-get update && apt-get install -y wait-for-it && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 80

ENV PYTHONUNBUFFERED 1

# Run main.py when the container launches
CMD ["python", "main.py"]
