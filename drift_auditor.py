def detect_drift(current_state, intended_state):
    drift = {}
    for key, value in intended_state.items():
        if current_state.get(key) != value:
            drift[key] = {
                'intended': value,
                'current': current_state.get(key)
            }
    return drift

# Example data
intended_state = {
    'cost': 300,  # GBP
    'availability': 99.9,  # percentage
    'security': "Private access only"
}

current_state = {
    'cost': 280,  # GBP
    'availability': 98.5,  # percentage (drift detected here)
    'security': "Private access only"
}

drift = detect_drift(current_state, intended_state)

if drift:
    print("Drift detected:")
    for key, value in drift.items():
        print(f"{key}: Intended: {value['intended']} | Current: {value['current']}")
else:
    print("No drift detected.")
