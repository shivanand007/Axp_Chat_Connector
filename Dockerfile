# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set metadata for the image
LABEL maintainer="shivanand masne shivanandmasne1998@email.com"
LABEL description="Docker image for a FastAPI application"

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that your FastAPI server will run on
EXPOSE 9000

# Define the command to run your FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
