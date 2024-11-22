#!/bin/bash

# Start the Ollama service in the background
ollama serve &

# Wait for the Ollama service to initialize
echo "Waiting for Ollama service to start..."
while ! curl -s http://localhost:11434/models > /dev/null; do
    sleep 2
done
echo "Ollama service is running."

# Run the Python script to process images
python3 /app/process_images.py