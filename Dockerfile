FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN /bin/bash -c "pip install -r requirements.txt"


# Copy the rest of the application code
COPY . .

# Run the create_db.py script to create the database and table
RUN /bin/bash -c "python create_db.py"

# Make sure gunicorn is available in the virtual environment
CMD ["/bin/bash", "-c", "gunicorn -w 4 -b 0.0.0.0:5000 app:app"]
