#!/bin/bash

sudo docker run -it -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY -e OPENAI_API_KEY=$OPENAI_API_KEY -v "$(pwd)/books:/app/books" summarizer

