#!/bin/bash

# Run the database creation script
python create_db.py

# Start the application with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
