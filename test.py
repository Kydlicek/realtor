def filter_additional_info(add_text):
    # Initialize an empty dictionary to store filtered values
    filtered_values = {
        'kauce': None,
        'services': None,
        'energy': None,
        'rk': None
    }

    # Check for keywords and extract the corresponding values
    if 'kauce' in add_text:
        parts = add_text.split('kauce', 1)
        if len(parts) > 1:
            value_part = parts[1].split(' ', 1)[0].strip()
            try:
                value = int(value_part.replace(',', '').replace('.', ''))
                filtered_values['kauce'] = value
            except ValueError:
                pass

    if 'services' in add_text:
        parts = add_text.split('services', 1)
        if len(parts) > 1:
            value_part = parts[1].split(' ', 1)[0].strip()
            try:
                value = int(value_part.replace(',', '').replace('.', ''))
                filtered_values['services'] = value
            except ValueError:
                pass

    if 'energy' in add_text:
        parts = add_text.split('energy', 1)
        if len(parts) > 1:
            value_part = parts[1].split(' ', 1)[0].strip()
            try:
                value = int(value_part.replace(',', '').replace('.', ''))
                filtered_values['energy'] = value
            except ValueError:
                pass

    if 'RK' in add_text:
        parts = add_text.split('RK', 1)
        if len(parts) > 1:
            value_part = parts[1].split(' ', 1)[0].strip()
            try:
                value = int(value_part.replace(',', '').replace('.', ''))
                filtered_values['RK'] = value
            except ValueError:
                pass

    return filtered_values

# Example usage:
add_text = 'Záloha na služby, vratná kauce a provize RK'
filtered_values = filter_additional_info(add_text)
print(filtered_values)
