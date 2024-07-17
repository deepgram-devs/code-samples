import os
from openai import OpenAI

client = OpenAI(api_key='')
import re

# Set your OpenAI API key

def read_markdown_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_markdown_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def generate_title_and_description(code_sample, relative_path):
    prompt = (
        f"Read the following code examples and write a suitable title and a short description (approximately 250 characters) of what the code does/what library is used. DO NOT autogenerate code. Only describe the code that is given to you."
        f"Structure the response with headings for each category and include the code sample paths as shown in the example below:\n\n"
        f"## Speech-to-Text Conversion using Deepgram API\n\n"
        f"1. **Title:** title here\n"
        f"   **Code Sample:** filename here\n\n"
        f"   **Description:** description here\n\n"
        f"2. **Title:** title here\n"
        f"   **Code Sample:** filename here\n\n"
        f"   **Description:** description here\n\n"
        f"## Text-to-Speech Conversion Using Deepgram API\n\n"
        f"3. **Title:** title here\n"
        f"   **Code Sample:** filename here\n\n"
        f"   **Description:** description here\n\n"
        f"Now, read the following code example and write a suitable title and description in the same format:\n\n"
        f"Code Sample: {relative_path}\n\n{code_sample}"
    )

    response = client.chat.completions.create(
      model="gpt-4",
      messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": prompt}
      ],
      max_tokens=1500,
      n=1,
      stop=None,
      temperature=0.5
    )

    return response.choices[0].message.content.strip()

def extract_code_samples(content):
    pattern = r"(### .*?\n\n```.*?\n.*?\n```)"
    matches = re.findall(pattern, content, re.DOTALL)
    return matches

def process_markdown_file(file_path):
    content = read_markdown_file(file_path)
    code_samples = extract_code_samples(content)

    for code_sample in code_samples:
        match = re.search(r"### (.*?)\n\n```.*?\n(.*?)\n```", code_sample, re.DOTALL)
        if match:
            title = match.group(1)
            code = match.group(2)
            relative_path_match = re.search(r"### (.*?)\n", code_sample)
            if relative_path_match:
                relative_path = relative_path_match.group(1)
                title_and_description = generate_title_and_description(code, relative_path)
                content = content.replace(code_sample, title_and_description + "\n\n" + code_sample)

    write_markdown_file(file_path, content)

def main():
    project_root = os.getcwd()
    documentation_dir = os.path.join(project_root, 'documentation')

    updated_files_path = os.path.join(project_root, 'updated_files.txt')
    if not os.path.exists(updated_files_path):
        print("No files to process.")
        return

    with open(updated_files_path, 'r') as file:
        updated_files = [line.strip() for line in file]

    for file_path in updated_files:
        if file_path.endswith('-readme.md'):
            process_markdown_file(file_path)
            print(f"Processed {file_path}")

if __name__ == "__main__":
    main()
