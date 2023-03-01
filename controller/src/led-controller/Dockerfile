FROM python:3.9.16-alpine

# Set the root directory for the app
WORKDIR /app

# Upgrade pip and install dependencies
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy over the required files into the working directory
COPY src/utils/* ./utils/
COPY src/led-controller.py .

# Run the Python script
CMD ["python", "-u", "led-controller.py"]
