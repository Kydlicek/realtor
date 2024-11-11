import re


def extract_location(data):
    location = {"street": None, "city": None, "city_part": None}

    # Case: with city part, pattern "City - City Part"
    city_part_pattern = r"(.+?)\s*-\s*(.+)"
    # Case: city with a number, pattern "City Number"
    city_number_pattern = r"(.+?)\s+(\d+)"

    if len(data) == 2:
        location["street"] = data[0].strip()

        # Check if city contains city part with hyphen
        match = re.match(city_part_pattern, data[1].strip())
        if match:
            city = match.group(1).strip()
            city_part = match.group(2).strip()

            # Standardize city name to "Praha" if it starts with "Praha"
            if "Praha" in city:
                location["city"] = "Praha"
                location["city_part"] = city_part
            else:
                location["city"] = city
                location["city_part"] = city_part
        else:
            # Check if city contains a number directly after city name (e.g., "Plzeň 5")
            match = re.match(city_number_pattern, data[1].strip())
            if match:
                location["city"] = match.group(1).strip()
                location["city_part"] = match.group(2).strip()
            else:
                # Standardize city name to "Praha" if it starts with "Praha"
                if "Praha" in data[1]:
                    location["city"] = "Praha"
                else:
                    location["city"] = data[1].strip()

    return location


# Test cases
data1 = ["Manželů Burdychových", " Červený Kostelec"]
data2 = ["Haštalská", " Praha 1 - Staré Město"]
data3 = ["Karlova", " Praha 5"]
data4 = ["Karlova", "Plzeň 5"]
data5 = ["Karlova", "Brno"]

print(extract_location(data1))
print(extract_location(data2))
print(extract_location(data3))
print(extract_location(data4))
print(extract_location(data5))
