import yaml

def load_intent(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

intent = load_intent('intent.yaml')
print(intent)

