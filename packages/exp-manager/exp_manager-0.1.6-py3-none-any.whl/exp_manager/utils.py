import yaml

def read_yaml(file):
    with open(file, "r") as f:
        return yaml.safe_load(f)
