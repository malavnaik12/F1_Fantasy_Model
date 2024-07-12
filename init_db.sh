#!/bin/bash

# Define the container name and data directory
CONTAINER_NAME=my-mongo
DATA_DIR=$(pwd)/mongo-data

# Pull the latest MongoDB Docker image
docker pull mongo

# Create a data directory if it doesn't exist
mkdir -p "$DATA_DIR"

# Run the MongoDB container with data persistence
docker run --name "$CONTAINER_NAME" -d -p 27017:27017 -v "$DATA_DIR:/data/db" mongo

# Verify that the MongoDB container is running
docker ps | grep "$CONTAINER_NAME"
