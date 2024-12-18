import subprocess
import sys
import os


def clean_openshift_yaml(input_file, output_file):
    """
    Cleans an OpenShift YAML file by removing unnecessary fields using yq.
    Automatically handles both object and array structures.
    """
    try:
        # Define the fields to remove
        fields_to_remove = [
            "metadata.annotations?",
            "metadata.managedFields?",
            "metadata.selfLink?",
            "metadata.creationTimestamp?",
            "metadata.resourceVersion?",
            "metadata.uid?",
            "status?"
        ]

        # Build the yq command dynamically
        yq_command = [
            "yq", "eval",
            " | ".join(f"del(.{field})" for field in fields_to_remove),
            input_file
        ]

        # Write the cleaned output to a file
        with open(output_file, "w") as f:
            subprocess.run(yq_command, stdout=f, check=True)

        print(f"Cleaned YAML saved to {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"Error running yq: {e}")
        print(f"Command used: {' '.join(yq_command)}")
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
