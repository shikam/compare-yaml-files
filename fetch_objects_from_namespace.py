import subprocess
import os
import sys


def fetch_objects_from_namespace(ns_name, object_type, output_dir):
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{object_type}.yaml")

        print(f"Fetching {object_type} from namespace: {ns_name}")
        subprocess.run(
            ["oc", "get", object_type, "-n", ns_name, "-o", "yaml"],
            stdout=open(output_file, "w"),
            stderr=subprocess.DEVNULL,
            check=True
        )
        print(f"Saved {object_type} to {output_file}")
        return output_file

    except subprocess.CalledProcessError:
        print(f"No {object_type} found in namespace: {ns_name}")
        return None


def main():
    if len(sys.argv) != 3:
        print("Usage: python extract_and_compare.py <namespace> <source_yaml>")
        sys.exit(1)

    ns_name = sys.argv[1]
    source_yaml = sys.argv[2]
    base_output_dir = "./comparison_results"

    object_types = [
        "deploymentconfig", "route", "service", "pvc", "imagestream", "buildconfig"
    ]

    for obj_type in object_types:
        output_dir = os.path.join(base_output_dir, ns_name, obj_type)
        yaml_file = fetch_objects_from_namespace(ns_name, obj_type, output_dir)

        if yaml_file:
            print(f"Comparing {obj_type}...")
            compare_output_dir = os.path.join(base_output_dir, ns_name, "results", obj_type)
            os.makedirs(compare_output_dir, exist_ok=True)

            subprocess.run([
                "python", "k8s-yaml-compare.py", source_yaml, yaml_file, compare_output_dir
            ])


if __name__ == "__main__":
    main()
