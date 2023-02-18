FROM python:3.9.16-alpine3.16

# Set the root directory for the app
WORKDIR /app

# Copy the code files to the working directory
COPY scheduler.py .
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the Python script
CMD ["python", "scheduler.py"]
