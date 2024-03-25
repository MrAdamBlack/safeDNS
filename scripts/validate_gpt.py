import sys
import re

def validate_rpz_file(file_path):
    errors_found = False

    with open(file_path, 'r') as file:
        # Validate first three lines
        expected_headers = [
            "$TTL 86400",
            "@ SOA localhost. admin.safedns.com.au. 1710796200 43200 3600 259200 300",
            "  NS localhost."
        ]
        for index, expected_header in enumerate(expected_headers):
            line = file.readline().strip()
            if line != expected_header:
                print(f"Error in line {index + 1}: Expected '{expected_header}' but found '{line}'")
                errors_found = True

        # Validate the remaining lines
        line_number = 4
        for line in file:
            line = line.strip()
            if not line or line.startswith(';'):
                print(f"Error in line {line_number}: Blank or comment line found")
                errors_found = True
            elif not re.match(r'^(\*\.|[\w-]+\.)*[\w-]+\s+CNAME\s*.$', line):
                print(f"Error in line {line_number}: Line does not match RPZ format: {line}")
                errors_found = True
            elif line.count("CNAME") != 1:
                print(f"Error in line {line_number}: More than one 'CNAME' found: {line}")
                errors_found = True
            line_number += 1

    if not errors_found:
        print("RPZ file is valid.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py rpzFile.txt")
        sys.exit(1)

    rpz_file = sys.argv[1]

    validate_rpz_file(rpz_file)

