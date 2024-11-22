build: docker build -t llama-multimodal -f ./ollama.dockerfile .

run: docker run --rm --privileged --name llama_container -p 11434:11434 \
    -v $(pwd)/test_images:/test_images \                                                                                     
    -v $(pwd)/result:/result \
    llama-multimodal