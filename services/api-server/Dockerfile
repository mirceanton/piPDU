FROM python:3.9.16-alpine3.16

WORKDIR /app

# Upgrade pip and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the code files to the working directory
COPY src/* ./

# Run the Python script
CMD ["python", "-u", "__init__.py"]
