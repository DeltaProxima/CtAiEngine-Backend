# Use an official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /

# Copy the requirements file to the container
COPY ./requirements.txt /requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /requirements.txt

# Copy the FastAPI app code to the container
COPY . /

# Expose the port FastAPI runs on
EXPOSE 8000

# Create uploads directory
RUN mkdir -p /uploads

# Command to run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
