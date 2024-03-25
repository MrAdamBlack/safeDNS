import sys
import re

def validate_file(rpz_file):
    with open(rpz_file, 'r') as file:
        lines = file.readlines()

    # Validate header
    header = [
        "$TTL 86400",
        "@ SOA localhost. admin.safedns.com.au. 1710796200 43200 3600 259200 300",
        "  NS  localhost."
    ]
    for i in range(3):
        if lines[i].strip() != header[i]:
            print(f"Error: Line {i+1} is not correct. It is: {lines[i]}")

    # Validate RPZ format for the rest of the lines
    rpz_format = re.compile(r'^(\*\.)?[a-zA-Z0-9][a-zA-Z0-9\.\-]* CNAME \.$')
    for i in range(3, len(lines)):
        line = lines[i].strip()
        if not line:  # No blank lines
            print(f"Error: Line {i+1} is blank.")
            continue
        if not rpz_format.match(line):  # Must match RPZ format
            print(f"Error: Line {i+1} is not in RPZ format. It is: {line}")
            continue
        if line.count('CNAME .') != 1:  # Only one "CNAME ." per line
            print(f"Error: Line {i+1} has more than one 'CNAME .'. It is: {line}")

if __name__ == "__main__":
    rpz_file = sys.argv[1]
    validate_file(rpz_file)

