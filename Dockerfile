# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create a directory for the app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install PyTorch from extra index and other dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Expose the port Streamlit uses
EXPOSE 8501

# Run the Streamlit application
CMD ["streamlit", "run", "app.py"]
