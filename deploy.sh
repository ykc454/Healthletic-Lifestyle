#!/bin/bash

echo "Building Docker image..."

docker build -t flask-api:latest .

echo "Running Container..."

docker run -p 5000:5000 flask-api:latest