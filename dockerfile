FROM python:3.8

# Install required packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the Streamlit app
COPY . /app
WORKDIR /app

# Expose the port Streamlit runs on
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]