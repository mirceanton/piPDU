FROM python:3.9.16-alpine3.16

# Set the root directory for the app
WORKDIR /app

# Upgrade pip and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy over the required files into the working directory
COPY src/utils/* ./utils/
COPY src/button-controller.py .

# Run the Python script
CMD ["python", "-u", "button-controller.py"]
