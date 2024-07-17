import os
import yaml
from pathlib import Path
import subprocess

def read_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            print(f"Reading YAML file: {file_path}")
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error reading YAML file {file_path}: {e}")
        return None

def write_yaml(file_path, data):
    try:
        with open(file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)
    except Exception as e:
        print(f"Error writing YAML file {file_path}: {e}")

def write_to_readme(language, content, documentation_path):
    try:
        readme_path = os.path.join(documentation_path, f'{language}-readme.md')
        print(f"Writing content to: {readme_path}")
        with open(readme_path, 'w') as readme_file:
            readme_file.write(content)
    except Exception as e:
        print(f"Error writing to {readme_path}: {e}")

def scrape_code_from_files(language_path, target_files, language):
    content = ""
    for root, _, files in os.walk(language_path):
        for target in target_files:
            for file_name in files:
                if Path(file_name).match(target):
                    file_path = os.path.join(root, file_name)
                    relative_path = os.path.relpath(file_path, language_path)
                    print(f"Scraping content from: {file_path}")
                    try:
                        with open(file_path, 'r') as code_file:
                            file_content = code_file.read()
                            content += f"### {relative_path}\n\n"
                            content += f"```{language}\n{file_content}\n```\n\n"
                    except Exception as e:
                        print(f"Error reading file {file_path}: {e}")
    return content

def print_directory_tree(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")

def process_language(language_path, documentation_path, language):
    print(f"Directory structure for {language_path}:")
    print_directory_tree(language_path)

    config_path = os.path.join(language_path, 'config.yaml')
    if os.path.exists(config_path):
        config = read_yaml(config_path)
        if config:
            target_files = config.get('target_files', [])
            if target_files:
                content = scrape_code_from_files(language_path, target_files, language)
                if content:
                    write_to_readme(language, content, documentation_path)
                else:
                    print(f"No content scraped for language: {language}")
            else:
                print(f"No target files specified in config.yaml for {language_path}")
        else:
            print(f"Failed to read config.yaml in {language_path}")
    else:
        print(f"config.yaml not found in {language_path}")

def reset_update_languages(update_languages_path):
    with open(update_languages_path, 'r') as file:
        lines = file.readlines()

    with open(update_languages_path, 'w') as file:
        for line in lines:
            stripped_line = line.lstrip()
            if stripped_line.startswith('- '):
                indent = line[:len(line) - len(stripped_line)]
                file.write(f'{indent}# - {stripped_line[2:].strip()}\n')
            else:
                file.write(line)

    print(f"Reset {update_languages_path} with all languages commented out.")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir, '../languages')
    documentation_path = os.path.join(script_dir, '../documentation')
    update_languages_path = os.path.join(documentation_path, 'update_languages.yaml')
    
    update_config = read_yaml(update_languages_path)
    if not update_config:
        print("Failed to read update_languages.yaml or it is empty")
        return

    languages_to_update = update_config.get('languages', [])
    if not languages_to_update:
        print("No languages to update")
        return

    for language_path in languages_to_update:
        if not language_path.startswith('#'):
            full_language_path = os.path.join(base_path, language_path.strip())
            language = os.path.basename(language_path.strip())
            print(f"Processing language path: {full_language_path}")
            process_language(full_language_path, documentation_path, language)
    
    # Call the generate_descriptions.py script
    generate_descriptions_path = os.path.join(script_dir, 'generate_descriptions.py')
    subprocess.run(['python', generate_descriptions_path])

    # Reset update_languages.yaml
    reset_update_languages(update_languages_path)

if __name__ == "__main__":
    main()
