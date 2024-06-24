FROM python:3.8-slim-buster

EXPOSE 8501

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install essential packages first
COPY requirements-part1.txt /app/
RUN pip3 install --no-cache-dir -r requirements-part1.txt

# Install remaining packages
COPY requirements-part2.txt /app/
RUN pip3 install --no-cache-dir -r requirements-part2.txt

# Copy the rest of the application code
COPY . /app

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
