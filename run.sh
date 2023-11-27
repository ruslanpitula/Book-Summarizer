#!/bin/bash

# Run the Docker container, sharing the current working directory
sudo docker run -it -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY -v "$(pwd):/app" summarizer

