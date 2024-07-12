#!/bin/bash

# Specify the Database (Mongo) Container name
CONTAINER_NAME=my-mongo

# Kill the Database Container
docker kill "$CONTAINER_NAME"

# Remove the Database Container
docker rm "$CONTAINER_NAME"

# Verify that the MongoDB container has stopped running
docker ps | grep "$CONTAINER_NAME"