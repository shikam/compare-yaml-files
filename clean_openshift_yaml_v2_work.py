import yaml
import sys
import os


def clean_openshift_yaml(input_file, output_file):
    """
    Cleans an OpenShift YAML file by removing unnecessary fields like annotations, managedFields, etc.
    """
    fields_to_remove = [
        "annotations",
        "managedFields",
        "selfLink",
        "creationTimestamp",
        "resourceVersion",
        "uid",
        "status"
    ]

    try:
        # Load YAML data
        with open(input_file, 'r') as f:
            data = yaml.safe_load(f)

        # Recursive function to remove fields
        def remove_fields(data, keys):
            if isinstance(data, dict):
                for key in list(data.keys()):  # Use list to avoid runtime changes
                    if key in keys:
                        del data[key]
                    else:
                        remove_fields(data[key], keys)
            elif isinstance(data, list):
                for item in data:
                    remove_fields(item, keys)

        # Apply cleaning
        remove_fields(data, fields_to_remove)

        # Save cleaned data
        with open(output_file, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)

        print(f"Cleaned YAML saved to {output_file}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python clean_openshift_yaml.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist.")
        sys.exit(1)

    clean_openshift_yaml(input_file, output_file)


if __name__ == "__main__":
    main()
