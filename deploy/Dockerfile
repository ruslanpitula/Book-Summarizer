# Use the official Ubuntu image
FROM ubuntu:latest

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip

# Install Python dependencies
RUN pip3 install \
    anthropic \
    openai \
    Ebooklib \
    click \
    colorama

# Set the working directory
WORKDIR /app

# Copy files
COPY utils/* /app/


# Run the script
CMD ["python3", "summarizer.py"]
