# Stage 1: Pull the model
FROM ollama/ollama:latest AS model_stage

# Start the Ollama service to pull the model
RUN ollama serve & sleep 5 && ollama pull llama3.2-vision:90b

# Stage 2: Build the final image
FROM ollama/ollama:latest

# Install basic dependencies for Python
RUN apt-get update && apt-get install -y python3-pip wget curl unzip && \
    pip install --upgrade pip && \
    pip install Pillow ollama

# Copy the pulled model from the first stage
COPY --from=model_stage /root/.ollama/models /root/.ollama/models

# Copy the Python script
COPY process_images.py /app/process_images.py

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set the working directory
# Use the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]