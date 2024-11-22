import os
import csv
import ollama

def analyze_text_with_ollama(text_content):
    """
    Use the Ollama model to analyze the text content and classify it as trees, weeds, or crops.
    """
    # Prepare the prompt for classification
    prompt = f"Classify the following text as describing trees, weeds, or crops: '{text_content}'. Provide the results in a tabular way like a csv with each gender and species, along with their class."
    
    response = ollama.chat(model='llama3.2:1b', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    # Extract and return the classification
    return response.get('message', {}).get('content', 'No response')

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

def process_csv_files(test_images_dir):
    """
    Process all CSV files in the test_images directory, classify their text content, and save results.
    """
    # Verify that the test_images directory exists
    if not os.path.isdir(test_images_dir):
        print(f"Directory {test_images_dir} does not exist.")
        return

    # Iterate over all CSV files in the directory
    for file in os.listdir(test_images_dir):
        file_path = os.path.join(test_images_dir, file)

        # Skip non-CSV files
        if not file.lower().endswith('.csv'):
            print(f"Skipping non-CSV file: {file}")
            continue

        print(f"Processing CSV: {file}")
        try:
            # Read and analyze the content of the CSV
            with open(file_path, 'r') as csv_file:
                reader = csv.reader(csv_file)
                classifications = []
                for row in reader:
                    # Join the row content as a single string and analyze
                    text_content = " ".join(row)
                    classification = analyze_text_with_ollama(text_content)
                    classifications.append(f"Text: {text_content}\nClassification: {classification}\n")
                
                # Combine all classifications and save them
                result = "\n".join(classifications)
                save_result(file_path, result)
                print(f"Saved analysis for {file}.\n")
        except Exception as e:
            print(f"Error processing {file}: {e}\n")

if __name__ == "__main__":
    test_images_dir = "./test_images"  # Adjust path as needed
    process_csv_files(test_images_dir)
    print("All CSV files processed. Results saved to result/")