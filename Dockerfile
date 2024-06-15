FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN /bin/bash -c "pip install -r requirements.txt"

# Copy the rest of the application code
COPY . .

# Ensure the entrypoint script is executable
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
