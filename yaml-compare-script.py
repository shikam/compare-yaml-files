import yaml
from tabulate import tabulate
from deepdiff import DeepDiff

def compare_yaml_files(file1_path, file2_path):
    # Load YAML files
    with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
        data1 = yaml.safe_load(f1)
        data2 = yaml.safe_load(f2)

    # Compare files using DeepDiff
    diff = DeepDiff(data1, data2, ignore_order=True)

    # Prepare results for tabulation
    results = []

    # Handle added items
    if 'dictionary_item_added' in diff:
        for item in diff['dictionary_item_added']:
            results.append([item, 'Added in File 2', '-', 'New Value'])

    # Handle removed items
    if 'dictionary_item_removed' in diff:
        for item in diff['dictionary_item_removed']:
            results.append([item, 'Removed from File 2', 'Old Value', '-'])

    # Handle value changes
    if 'values_changed' in diff:
        for key, change in diff['values_changed'].items():
            results.append([
                key, 
                'Value Changed', 
                change['old_value'], 
                change['new_value']
            ])

    # Display results in a table
    if results:
        headers = ['Path', 'Change Type', 'File 1 Value', 'File 2 Value']
        print(tabulate(results, headers=headers, tablefmt='grid'))
    else:
        print("No differences found between the two YAML files.")

# Example usage
if __name__ == "__main__":
    compare_yaml_files('file1.yaml', 'file2.yaml')
