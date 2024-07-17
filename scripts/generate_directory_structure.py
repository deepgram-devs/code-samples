import os
import yaml

def generate_directory_structure(root_dir, base_dir_name):
    directory_dict = {base_dir_name: {}}

    for root, dirs, files in os.walk(root_dir):
        # Skip directories above the base_dir_name
        if base_dir_name not in root:
            continue

        path = root.split(os.sep)
        # Find the index of the base_dir_name in the path
        base_index = path.index(base_dir_name)
        # Create a sub-path starting from the base_dir_name
        sub_path = path[base_index:]
        parent = directory_dict[base_dir_name]
        for folder in sub_path[1:]:  # Skip the base_dir_name itself
            parent = parent.setdefault(folder, {})
        for file in files:
            parent.setdefault('files', []).append(file)

    return directory_dict

def write_yaml_file(data, output_file):
    with open(output_file, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

def main():
    project_root = os.getcwd()
    languages_dir = os.path.join(project_root, 'languages')
    output_file = os.path.join(languages_dir, 'project_structure.yaml')

    directory_structure = generate_directory_structure(project_root, 'languages')
    write_yaml_file({'code-samples': directory_structure}, output_file)

if __name__ == "__main__":
    main()
