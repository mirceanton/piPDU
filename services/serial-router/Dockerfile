FROM python:3.9.16-alpine3.16

# Set the root directory for the app
WORKDIR /app

# Upgrade pip and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy over the required files into the working directory
COPY src/utils/* ./utils/
COPY src/router.py .

# Run the Python script
CMD ["python", "-u", "router.py"]
