import os
import ollama

def generate_description_from_filename(image_filename):
    """
    Generate a description based on the image filename using the Llama 3.2 1B model.
    """
    # Prepare the prompt
    prompt = f"Describe the content of an image with the following filename: {image_filename}."

    
    response:ollama.ChatResponse = ollama.chat(model='llama3.2:1b', messages=[
    {
        'role': 'user',
        'content': prompt,
    },
    ])
    # Extract and return the generated description
    return response.get('message', {}).get('content', 'No response')

def save_result(image_path, result):
    """
    Save the result in /result/<image_name>.txt.
    """
    # Ensure the results directory exists
    os.makedirs("result", exist_ok=True)

    # Extract the image name without extension
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    result_path = f"result/{image_name}.txt"

    # Write the result to a text file
    with open(result_path, "w") as f:
        f.write(result)

def process_all_images(test_images_dir):
    """
    Process all images in the test_images directory and save results.
    """
    # Verify that the test_images directory exists
    if not os.path.isdir(test_images_dir):
        print(f"Directory {test_images_dir} does not exist.")
        return

    # Iterate over all files in the directory
    for image_file in os.listdir(test_images_dir):
        image_path = os.path.join(test_images_dir, image_file)

        # Skip non-image files
        if not image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            print(f"Skipping non-image file: {image_file}")
            continue

        print(f"Processing: {image_file}")
        try:
            # Generate description based on the filename and save the result
            description = generate_description_from_filename(image_file)
            save_result(image_path, description)
            print(f"Saved description for {image_file}.\n")
        except Exception as e:
            print(f"Error processing {image_file}: {e}\n")

if __name__ == "__main__":
    test_images_dir = "./test_images"  # Adjust path as needed
    process_all_images(test_images_dir)
    print("All images processed. Results saved to result/")