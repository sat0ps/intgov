def check_cost(intent_cost, current_cost):
    if current_cost > intent_cost:
        print("Cost exceeds the defined limit!")
    else:
        print("Cost is within the limit.")

def check_availability(intent_availability, current_availability):
    if current_availability < intent_availability:
        print("Availability is below the defined target!")
    else:
        print("Availability is within the limit.")

def check_security(intent_security, current_security):
    if current_security != intent_security:
        print("Security configuration does not match the intent!")
    else:
        print("Security is within the defined target.")

# Example usage:
intent_data = {
    'cost': 300,  # GBP
    'availability': 99.9,  # percentage
    'security': "Private access only"
}

current_data = {
    'cost': 280,  # GBP
    'availability': 99.8,  # percentage
    'security': "Private access only"
}

check_cost(intent_data['cost'], current_data['cost'])
check_availability(intent_data['availability'], current_data['availability'])
check_security(intent_data['security'], current_data['security'])
