FROM python:3.9.16-alpine3.16

WORKDIR /app

# Copy the code files to the working directory
COPY metrics.py .
COPY requirements.txt .

# Install the required packages
RUN pip install -r requirements.txt

# Expose the default port for the Prometheus metrics endpoint
EXPOSE 8000

# Run the Python script
CMD ["python", "metrics.py"]
