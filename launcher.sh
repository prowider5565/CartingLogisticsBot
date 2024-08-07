#!/bin/bash

echo "Running migration.sh script..."
uvicorn main:app --host 0.0.0.0 --port 8000
echo "Uvicorn server and Webhook bot initiated successfully!"
