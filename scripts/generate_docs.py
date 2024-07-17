import os
import yaml
import fnmatch
import subprocess
from deepdiff import DeepDiff

def load_yaml_file(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def generate_directory_structure(root_dir, base_dir_name):
    directory_dict = {base_dir_name: {}}

    for root, dirs, files in os.walk(root_dir):
        if base_dir_name not in root:
            continue

        path = root.split(os.sep)
        base_index = path.index(base_dir_name)
        sub_path = path[base_index:]
        parent = directory_dict[base_dir_name]
        for folder in sub_path[1:]:
            parent = parent.setdefault(folder, {})
        for file in files:
            parent.setdefault('files', []).append(file)

    return directory_dict

def write_yaml_file(data, output_file):
    with open(output_file, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

def get_target_files(config_path):
    config = load_yaml_file(config_path)
    if isinstance(config, dict):
        return config.get('target_files', [])
    else:
        print(f"Error: Config file at {config_path} is not formatted correctly.")
        return []

def generate_readme_for_language(language_dir, target_patterns, documentation_dir, updated_files):
    readme_path = os.path.join(documentation_dir, f"{os.path.basename(language_dir)}-readme.md")
    original_content = None
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as readme_file:
            original_content = readme_file.read()

    new_content = []
    for root, _, files in os.walk(language_dir):
        for file in files:
            if file == 'project_structure.yaml':
                continue  # Skip the project_structure.yaml file
            if any(fnmatch.fnmatch(file, pattern) for pattern in target_patterns):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, language_dir)
                new_content.append(f"### {relative_path}\n\n")
                new_content.append("```{}\n".format(os.path.basename(language_dir)))
                with open(file_path, 'r') as code_file:
                    new_content.append(code_file.read())
                new_content.append("\n```\n\n")

    new_content_str = ''.join(new_content)

    if original_content != new_content_str or not os.path.exists(readme_path):  # Include newly created files
        with open(readme_path, 'w') as readme_file:
            readme_file.write(new_content_str)
        updated_files.append(readme_path)

def main():
    project_root = os.getcwd()
    languages_dir = os.path.join(project_root, 'languages')
    documentation_dir = os.path.join(project_root, 'documentation')
    os.makedirs(documentation_dir, exist_ok=True)
    old_project_structure_path = os.path.join(languages_dir, 'project_structure.yaml')

    # Load the old project structure
    old_project_structure = load_yaml_file(old_project_structure_path)

    # Generate the new project structure
    new_directory_structure = generate_directory_structure(project_root, 'languages')
    new_project_structure = {'code-samples': new_directory_structure}

    # Compare the old and new project structures
    diff = DeepDiff(old_project_structure, new_project_structure, ignore_order=True)
    updated_languages = []

    if diff:
        # Update the project_structure.yaml file
        write_yaml_file(new_project_structure, old_project_structure_path)

        # Identify updated or newly added languages
        if 'dictionary_item_added' in diff or 'values_changed' in diff:
            for item in diff.get('dictionary_item_added', []):
                path_parts = item.split('[')
                if len(path_parts) > 2 and path_parts[1].strip(']') == "'languages'":
                    updated_languages.append(path_parts[2].strip("]'"))
            for item in diff.get('values_changed', []):
                path_parts = item.split('[')
                if len(path_parts) > 2 and path_parts[1].strip(']') == "'languages'":
                    updated_languages.append(path_parts[2].strip("]'"))

    # Track updated files
    updated_files = []

    # Generate the readme files based on the new project structure and config files
    for language in os.listdir(languages_dir):
        language_dir = os.path.join(languages_dir, language)
        if os.path.isdir(language_dir):
            config_path = os.path.join(language_dir, 'config.yaml')
            if os.path.exists(config_path):
                target_patterns = get_target_files(config_path)
                if target_patterns:
                    generate_readme_for_language(language_dir, target_patterns, documentation_dir, updated_files)
                else:
                    print(f"Warning: No target patterns found for {language}.")
            else:
                print(f"Warning: config.yaml not found for {language}. Skipping.")
        else:
            print(f"Skipping non-directory item: {language}")

    # Write the list of updated files to a temporary file
    updated_files_path = os.path.join(project_root, 'updated_files.txt')
    with open(updated_files_path, 'w') as file:
        for updated_file in updated_files:
            file.write(updated_file + '\n')

    # Run the generate_descriptions.py script if there are updated files
    if updated_files:
        print("Running generate_descriptions.py to update descriptions...")
        subprocess.run(['python', 'scripts/generate_descriptions.py'])

     # Clear the updated_files.txt after processing
    with open(updated_files_path, 'w') as file:
        file.write('')
        
if __name__ == "__main__":
    main()
