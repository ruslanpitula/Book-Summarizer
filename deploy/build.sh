#!/bin/bash

# Build the Docker image
sudo docker build -t summarizer -f deploy/Dockerfile .
