# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies for OpenCV, Poppler, and Tesseract
RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 poppler-utils tesseract-ocr && \
    rm -rf /var/lib/apt/lists/*  # Entferne die nicht mehr benötigten Installationsdateien

# Install virtualenv
RUN pip install virtualenv

# Create a virtual environment
RUN virtualenv venv

# Copy the requirements file into the container
COPY requirements.txt .

# Activate the virtual environment and install the necessary packages
RUN /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

# Copy the rest of the application code into the container
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5050

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run the application within the virtual environment
CMD ["/bin/bash", "-c", "source venv/bin/activate && python run.py"]
