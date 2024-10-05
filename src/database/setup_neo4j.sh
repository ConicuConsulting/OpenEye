#!/bin/bash
# Script to set up Neo4j using Docker
docker run \
    --name openeye-neo4j \
    -p7474:7474 -p7687:7687 \
    -d \
    -e NEO4J_AUTH=neo4j/your_password \
    neo4j:latest
