#!/bin/bash

# Wait for GraphDB to be ready
until curl -s http://graphdb:7200/rest/repositories > /dev/null; do
  echo "Waiting for GraphDB..."
  sleep 2
done

# Creation of the repository
curl -X POST \
  -H "Content-Type: multipart/form-data" \
  -F "config=@/repo-config.ttl" \
  http://graphdb:7200/rest/repositories