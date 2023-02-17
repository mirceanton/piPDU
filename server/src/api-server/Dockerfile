FROM python:3.9.16-alpine3.16

WORKDIR /app

# Copy the code files to the working directory
COPY api.py .
COPY routes/ .
COPY requirements.txt .

# Install the required packages
RUN pip install -r requirements.txt

# Run the Python script
CMD ["python", "api.py"]
