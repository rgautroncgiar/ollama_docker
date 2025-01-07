import os
import ollama

def analyze_images_with_ollama(prompt, image_files_paths):
    """
    Use the Ollama model to analyze image content and classify it as trees, weeds, or crops.
    """
    results = []

    for image_file_path in image_files_paths:
        try:
            response = ollama.chat(
                model="llama3.2-vision",
                messages=[
                    {
                        "role": "user",
                        "content": prompt + f" \n FYI: image path is {image_file_path}",
                        "images": [image_file_path],  # Send image as binary
                    }
                ],
            )
            # Extract and store the classification response
            content = response.get("message", {}).get("content", "No response")
            results.append((image_file_path, content))

        except Exception as e:
            results.append((image_file_path, f"Error: {e}"))
    
    return results

def save_result(file_path, result):
    """
    Save the result in /result/<file_name>.txt.
    """
    # Ensure the results directory exists
    os.makedirs("result", exist_ok=True)

    # Extract the file name without extension
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    result_path = f"result/{file_name}.txt"

    # Write the result to a text file
    with open(result_path, "w") as f:
        f.write(result)

def get_image_paths(test_images_dir):
    """
    Gather all image files in the specified directory and return their full paths.
    """
    # Verify that the test_images directory exists
    if not os.path.isdir(test_images_dir):
        raise ValueError(f"Directory {test_images_dir} does not exist.")

    image_files_paths = [
        os.path.join(test_images_dir, f)
        for f in os.listdir(test_images_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
    ]
    
    if not image_files_paths:
        raise ValueError('No images found')
    
    return image_files_paths
        
if __name__ == "__main__":
    test_images_dir = "./test_images"  # Adjust path as needed
    image_files_paths = get_image_paths(test_images_dir)

    prompt = (
        "Based on the image(s) captured from a cheap smartphone in Africa, provide me with a list of answers to the following questions:\n"
        "-general description of the cropping plot\n"
        "-is it an agroforestry system?\n"
        "-is the system diversified?\n"
        "-is soil covered?\n"
        "-first present crop?\n"
        "-second present crop?\n"
        "-third present crop?\n"
        "-other present crops?\n"
        "additional instructions: format the answer as a csv file with a first column with the question, second column with the closed answer to the corresponding question, and third column with your comments if relevant; keep it as compact as possible.\n"
        "regarding present crops, answer only if relevant; the order of the crops follow their abundance in the picture."
    )

    # Call the function with correct argument order
    results = analyze_images_with_ollama(prompt, image_files_paths)

    # Save each result to its corresponding .txt file
    for file_path, content in results:
        save_result(file_path, content)

    print("All image files processed. Results saved to result/")