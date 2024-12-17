import yaml
from deepdiff import DeepDiff
from tabulate import tabulate


def load_yaml(file_path):
    """
    Loads a YAML file and returns its content as a dictionary.
    """
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def normalize_env_lists(yaml_dict):
    """
    Converts the 'env' lists in containers to dictionaries for better comparison.
    """
    containers = yaml_dict.get("spec", {}).get("template", {}).get("spec", {}).get("containers", [])
    if containers and isinstance(containers, list):
        for container in containers:
            if "env" in container:
                container["env"] = {env["name"]: env for env in container["env"] if "name" in env}


def compare_yaml_files(file1, file2):
    """
    Compares two YAML files and returns the differences.
    """
    yaml1 = load_yaml(file1)
    yaml2 = load_yaml(file2)

    # Normalize 'env' lists to dictionaries
    normalize_env_lists(yaml1)
    normalize_env_lists(yaml2)

    return DeepDiff(
        yaml1,
        yaml2,
        ignore_order=True,
        report_repetition=True,
    )


def format_differences_as_table(differences):
    """
    Formats differences into a table-friendly format.
    """
    table_data = []
    for diff_type, changes in differences.items():
        if isinstance(changes, dict):  # Handle dictionary-based differences
            for key, value in changes.items():
                if isinstance(value, dict):
                    old_value = value.get("old_value", "N/A")
                    new_value = value.get("new_value", "N/A")
                else:
                    old_value = "N/A"
                    new_value = value
                table_data.append([diff_type, key, old_value, new_value])
        elif isinstance(changes, (list, set)):  # Handle list-based differences
            for change in changes:
                table_data.append([diff_type, change, "N/A", "N/A"])
    return table_data


def main(file1, file2):
    """
    Main function to compare two YAML files.
    """
    print(f"Comparing {file1} with {file2}...")

    differences = compare_yaml_files(file1, file2)

    if differences:
        table_data = format_differences_as_table(differences)
        headers = ["Type", "Field", "Value in File 1", "Value in File 2"]
        print("\nDifferences found:\n")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    else:
        print("\nNo differences found!")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Compare two YAML files.")
    parser.add_argument("file1", type=str, help="Path to the first YAML file.")
    parser.add_argument("file2", type=str, help="Path to the second YAML file.")

    args = parser.parse_args()
    main(args.file1, args.file2)
