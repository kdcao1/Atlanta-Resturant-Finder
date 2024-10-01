# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents (your Python code) into the container at /app
COPY . /app

# Install any required Python packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*


# If you don't have a requirements.txt, you can directly install required packages:
# RUN pip install --no-cache-dir googlemaps

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Define the command to run your Python script
CMD ["python", "Atlanta_Food_Finder/gmaps/gmapsAPI.py", "run"]