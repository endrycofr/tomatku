FROM python:3.8-slim-buster

EXPOSE 8501

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/

# Instal dependensi utama dalam bagian yang lebih kecil
RUN pip3 install --no-cache-dir streamlit Pillow numpy
RUN pip3 install --no-cache-dir tensorflow

# Instal sisa dependensi
RUN pip3 install --no-cache-dir -r requirements.txt

# Salin sisa kode aplikasi
COPY . /app

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"