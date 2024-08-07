#!/bin/bash

echo "Running migration.sh script..."



alembic revision --autogenerate -m "create models"
echo "revision complated"

alembic upgrade head
echo "upgrade complated"



echo "Migration script completed."
