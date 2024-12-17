import yaml
from deepdiff import DeepDiff
from tabulate import tabulate


def load_yaml(file_path):
    """Loads a YAML file and returns its content as a dictionary."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def compare_yaml_files(file1, file2):
    """Compares two YAML files and returns the differences."""
    yaml1 = load_yaml(file1)
    yaml2 = load_yaml(file2)
    return DeepDiff(yaml1, yaml2, ignore_order=True)


def format_differences_as_table(differences):
    """Formats differences into a table-friendly format."""
    table_data = []
    for diff_type, changes in differences.items():
        if diff_type == "iterable_item_added" or diff_type == "iterable_item_removed":
            for key, value in changes.items():
                table_data.append([
                    diff_type,
                    key,
                    "N/A" if diff_type == "iterable_item_added" else value,
                    value if diff_type == "iterable_item_added" else "N/A",
                ])
        else:
            for key, change in changes.items():
                if isinstance(change, dict):
                    old_value = change.get("old_value", "N/A")
                    new_value = change.get("new_value", "N/A")
                else:
                    old_value = "N/A"
                    new_value = "N/A"
                table_data.append([diff_type, key, old_value, new_value])
    return table_data



def main(file1, file2):
    """Main function to compare two YAML files."""
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
