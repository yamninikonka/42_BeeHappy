# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /beehappy

# Copy requirements (if you have one)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY src/ ./src
# COPY data/ ./data

# Set environment variables if needed
# ENV SOME_VAR=some_value

# Run the main program
CMD ["python", "src/run.py"]
