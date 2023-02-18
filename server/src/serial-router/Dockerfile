FROM python:3.9.16-alpine3.16

# Set the root directory for the app
WORKDIR /app

# Copy over the required files into the working directory
COPY router.py .
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the Python script
CMD ["python", "router.py"]
