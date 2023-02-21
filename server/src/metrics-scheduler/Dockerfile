FROM python:3.9.16-alpine3.16

# Set the root directory for the app
WORKDIR /app

# Upgrade pip and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the code files to the working directory
COPY utils/* utils/
COPY scheduler.py .


# Run the Python script
CMD ["python", "-u", "scheduler.py"]
