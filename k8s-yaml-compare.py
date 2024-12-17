import sys
import yaml
from tabulate import tabulate
from deepdiff import DeepDiff
import re
import os


def beautify_path(key):
    """Clean and format the YAML path for better readability."""
    # Remove root and brackets, keeping nested structures clean
    key = re.sub(r"root\['(.*?)'\]", r"\1", key)  # Remove root['...']
    key = key.replace("']['", ".")  # Replace nested brackets with dots
    key = key.replace("[", "[").replace("]", "]")  # Keep list indices
    return key


def extract_name_from_yaml(file_path):
    """Extract the name field from the YAML file."""
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
            return data.get('metadata', {}).get('name', 'output')
    except Exception as e:
        print(f"Error extracting name from {file_path}: {e}")
        return 'output'


def compare_yaml_files(file1_path, file2_path, output_dir):
    try:
        # Load YAML files
        with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
            data1 = yaml.safe_load(f1)
            data2 = yaml.safe_load(f2)

        # Extract name for output file
        output_name = extract_name_from_yaml(file2_path)
        output_file = os.path.join(output_dir, f"{output_name}-comparison.txt")

        # Compare files using DeepDiff
        diff = DeepDiff(data1, data2, ignore_order=True)

        # Prepare results for tabulation
        results = []

        # Handle value changes
        if 'values_changed' in diff:
            for key, change in diff['values_changed'].items():
                results.append([
                    beautify_path(key),
                    'Value Changed',
                    change['old_value'],
                    change['new_value']
                ])

        # Handle added items
        if 'dictionary_item_added' in diff:
            for item in diff['dictionary_item_added']:
                clean_item = beautify_path(item)
                try:
                    value = eval(f"data2{item.replace('root', '')}")
                except:
                    value = "N/A"
                results.append([clean_item, 'Added in File 2', '-', value])

        # Handle removed items
        if 'dictionary_item_removed' in diff:
            for item in diff['dictionary_item_removed']:
                clean_item = beautify_path(item)
                try:
                    value = eval(f"data1{item.replace('root', '')}")
                except:
                    value = "N/A"
                results.append([clean_item, 'Removed from File 2', value, '-'])

        # Handle added or removed list items
        if 'iterable_item_added' in diff:
            for key, value in diff['iterable_item_added'].items():
                results.append([
                    beautify_path(key),
                    'Added to List in File 2',
                    '-',
                    value
                ])

        if 'iterable_item_removed' in diff:
            for key, value in diff['iterable_item_removed'].items():
                results.append([
                    beautify_path(key),
                    'Removed from List in File 2',
                    value,
                    '-'
                ])

        # Save results in a file
        os.makedirs(output_dir, exist_ok=True)
        with open(output_file, 'w') as f:
            if results:
                headers = ['Path', 'Change Type', 'File 1 Value', 'File 2 Value']
                table = tabulate(results, headers=headers, tablefmt='grid')
                f.write(table)
                print(f"Comparison results saved to {output_file}")
            else:
                f.write("No differences found between the two YAML files.\n")
                print("No differences found between the two YAML files.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure both file paths are correct.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():
    # Check if correct number of arguments is provided
    if len(sys.argv) != 4:
        print("Usage: python k8s-yaml-compare.py <file1_path> <file2_path> <output_dir>")
        sys.exit(1)

    # Get file paths from command-line arguments
    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    output_dir = sys.argv[3]

    # Run the comparison
    compare_yaml_files(file1_path, file2_path, output_dir)


if __name__ == "__main__":
    main()
