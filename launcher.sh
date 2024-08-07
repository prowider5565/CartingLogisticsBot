#!/bin/bash

echo "Running migration.sh script..."



alembic revision --autogenerate -m "create models"
echo "revision complated"

alembic upgrade head
echo "upgrade complated"

#cd src || exit
chmod -R 777 /app/src/media 


gunicorn src.runner:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000


echo "Migration script completed."
