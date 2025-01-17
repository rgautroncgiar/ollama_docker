import os
import ollama
from tqdm import tqdm  # pip install tqdm

def analyze_images_with_ollama(prompt, image_files_paths):
    """
    Use the Ollama model to analyze image content and classify it as trees, weeds, or crops.
    """
    results = []

    # Wrap the iteration in a tqdm progress bar
    for image_file_path in tqdm(image_files_paths, desc="Processing images"):
        try:
            response = ollama.chat(
                model="llama3.2-vision:11b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt + f"\nFYI: image path is {image_file_path}",
                        "images": [image_file_path],
                    }
                ],
            )

            # Adjust to match your actual Ollama response structure
            content = response.get("message", {}).get("content", "No response")
            results.append((image_file_path, content))

        except Exception as e:
            print(f'Exception occured: {e}')
            results.append((image_file_path, f"Error: {str(e)}"))
    
    return results

def save_result(file_path, result):
    """
    Save the result in /result/<file_name>.txt
    where <file_name> is the image's base name (no extension).
    """
    # Ensure the results directory exists
    os.makedirs("result", exist_ok=True)

    file_name_no_ext = os.path.splitext(os.path.basename(file_path))[0]
    result_path = os.path.join("result", f"{file_name_no_ext}.txt")

    with open(result_path, "w", encoding="utf-8") as f:
        f.write(result)

def get_image_paths(test_images_dir):
    """
    Gather all image files in the specified directory and return their full paths.
    """
    if not os.path.isdir(test_images_dir):
        raise ValueError(f"Directory '{test_images_dir}' does not exist.")

    image_files_paths = [
        os.path.join(test_images_dir, f)
        for f in os.listdir(test_images_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
    ]
    
    if not image_files_paths:
        raise ValueError(f"No images found in the {test_images_dir}.")
    
    return image_files_paths
        
if __name__ == "__main__":
    test_images_dir = "./test_images"  # Adjust path as needed
    test_size = 10
    image_files_paths = get_image_paths(test_images_dir)[:test_size]

    # Read the prompt from prompt.txt
    with open("./prompt.txt", "r", encoding="utf-8") as file:
        prompt = file.read()

    # Analyze images with Ollama
    results = analyze_images_with_ollama(prompt, image_files_paths)

    # Save each result to its corresponding .txt file
    for file_path, content in results:
        save_result(file_path, content)

    print("All image files processed. Results saved to 'result/' directory.")
