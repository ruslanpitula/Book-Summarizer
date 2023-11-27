# Use the official Ubuntu image
FROM ubuntu:latest

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip

# Set the working directory
WORKDIR /app

# Copy the script and requirements files
COPY summarizer.py /app/
COPY requirements.txt /app/

# Install Python dependencies
RUN pip3 install -r requirements.txt

RUN python3 -c "import nltk; nltk.download('punkt')"

# Run the script
CMD ["python3", "summarizer.py"]
