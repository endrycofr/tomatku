Berikut adalah README.md yang diperbarui dengan langkah-langkah instalasi yang baru:

---

# Building a Detection System for Tomato Leaf Disease using AWS Cloud Infrastructure

This project aims to develop a detection system for tomato leaf diseases using AWS Cloud Infrastructure. The system helps farmers and agricultural professionals identify diseases in tomato leaves before harvesting, ensuring better crop management and yield.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [AWS Services Used](#aws-services-used)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Tomato leaf diseases can significantly impact crop yield and quality. Early detection and management are crucial to minimize damage. This project leverages AWS Cloud Infrastructure to build a scalable and efficient system for detecting tomato leaf diseases using machine learning.

## Features

- **Real-time detection**: Process and analyze images of tomato leaves to identify diseases in real-time.
- **Scalability**: Built on AWS, the system can handle a large volume of images and data.
- **User-friendly interface**: Easy-to-use interface for farmers to upload images and receive results.
- **Automated alerts**: Send notifications to farmers when diseases are detected.

## Architecture

![Architecture Diagram](https://github.com/endrycofr/tomatku/blob/master/images/design_architecture.jpg)
The system architecture includes:

1. **Image Capture**: Farmers capture images of tomato leaves using a mobile device and upload them via a Streamlit application interface.
2. **Request Routing**: Amazon Route 53 directs requests to an Amazon EC2 instance hosting the application.
3. **Web Server and Proxy**: Nginx acts as a web server and reverse proxy, forwarding requests to the Streamlit application running inside a Docker container.
4. **Image Analysis**: The Streamlit application contains a deep learning CNN model that analyzes the images and detects diseases.
5. **Source Code Management**: The application source code is managed through Git for effective collaboration and versioning.
6. **Monitoring**: Amazon CloudWatch monitors the EC2 instance, providing real-time metrics and notifications for optimal performance and availability.

## Prerequisites

- AWS account
- Basic knowledge of AWS services (Route 53, EC2, Docker, Git, CloudWatch)
- Python 3.6+ installed on your local machine

## Installation

1. Update and upgrade your system:

   ```bash
   sudo apt update
   sudo apt upgrade
   ```

2. Install Git:

   ```bash
   sudo apt install git
   git --version
   ```

3. Clone the repository:

   ```bash
   git clone https://github.com/endrycofr/tomatku.git
   cd tomatku
   ```

4. Install Docker and Nginx:

   ```bash
   sudo apt update
   sudo apt install docker.io
   sudo apt install nginx
   sudo usermod -aG docker $USER
   ```

5. Build and run the Docker container for the Streamlit application:

   ```bash
   cd tomatku

   # Create Dockerfile
   nano Dockerfile
   ```

   Paste the following into the Dockerfile:

   ```dockerfile
   # Menggunakan base image Python versi 3.8
   FROM python:3.8-slim-buster

   # Expose the port that Streamlit will run on
   EXPOSE 8501

   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       build-essential \
       software-properties-common \
       git \
       && rm -rf /var/lib/apt/lists/*

   # Set the working directory
   WORKDIR /app

   # Copy the requirements file first to leverage Docker cache
   COPY requirements.txt .

   # Install Python dependencies
   RUN pip3 install --no-cache-dir -r requirements.txt

   # Copy the rest of the application code
   COPY . .

   # Set the entry point to run the Streamlit app
   ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

6. Build and run the Docker container:

   ```bash
   sudo systemctl start docker
   sudo systemctl status docker

   docker build -t mytomat-app .
   docker run -d -p 8501:8501 mytomat-app
   ```

7. Verify if the Docker container is running:

   ```bash
   docker images -a
   docker ps
   ```

8. Check access to the Streamlit app:

   ```bash
   curl -L http://127.0.0.1:8501
   ```

9. Configure the Nginx web server:

   ```bash
   sudo systemctl start nginx
   sudo systemctl status nginx

   # Copy static files to the web server directory
   sudo cp -r /home/ubuntu/tomatku /var/www/html/

   # Check the directory
   cd /var/www/html
   ls
   ```

10. Configure Nginx as a reverse proxy:

    ```bash
    sudo nano /etc/nginx/sites-available/default
    ```

    Update the configuration as follows:

    ```nginx
    server {
        listen 80;
        server_name www.agrofuture.site;

        location / {
            proxy_pass http://127.0.0.1:8501;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;

            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        access_log /var/log/nginx/tomatku_access.log;
        error_log /var/log/nginx/tomatku_error.log;

        root /var/www/html/tomatku;
        index index.html index.htm;

        error_page 404 /404.html;
        error_page 500 502 503 504 /50x.html;

        location = /50x.html {
            root /usr/share/nginx/html;
        }
    }
    ```

11. Test and restart Nginx:

    ```bash
    sudo nginx -t
    sudo systemctl restart nginx
    ```

12. Access the application publicly:
    [https://www.agrofuture.site/](https://www.agrofuture.site/)

## Usage

1. Upload images via the Streamlit application interface.
2. The deep learning model analyzes the images and provides detection results.
3. Check the results in the application interface or receive notifications via CloudWatch if any issues occur.

## AWS Services Used

- **Amazon Route 53**: DNS web service for directing requests.
- **Amazon EC2**: Compute service for hosting the application.
- **Nginx**: Web server and reverse proxy.
- **Docker**: Containerization of the Streamlit application.
- **Git**: Source code management.
- **Amazon CloudWatch**: Monitoring and logging service.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to modify and expand upon this README as needed for your specific project requirements.
