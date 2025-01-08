#!/bin/bash
cd ~/ollama_docker

# Pull the latest changes from the repository
git pull

# Build the Docker image with the specified Dockerfile
docker build -t llama-multimodal -f ./ollama.dockerfile .

# Run the Docker container with GPU support and necessary configurations
docker run --gpus=all --rm --privileged -it \
    -p 11434:11434 \
    -v $(pwd)/test_images:/test_images \
    -v $(pwd)/result:/result \
    llama-multimodal bash