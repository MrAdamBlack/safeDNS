import sys
import re
import os
import glob

def validate_file(rpz_file, output_file):
    with open(rpz_file, 'r') as file:
        lines = file.readlines()

    # Validate RPZ format for the rest of the lines
    rpz_format = re.compile(r'^(\*\.)?[a-zA-Z0-9][a-zA-Z0-9\.\-]* CNAME \.$')
    for i, line in enumerate(lines, start=1):
        line = line.strip()
        if not rpz_format.match(line):  # Must match RPZ format
            print(f"Error: Line {i} in {rpz_file} is not in RPZ format. It is: {line}")
            continue
        if line.count('CNAME .') != 1:  # Only one "CNAME ." per line
            print(f"Error: Line {i} in {rpz_file} has more than one 'CNAME .'. It is: {line}")

    # Append lines to the output file
    with open(output_file, 'a') as file:
        file.writelines(lines)

def combine_files(directory, base_file=None):
    # If base file is not provided, create a new file in the directory
    if not base_file:
        base_file = os.path.join(directory, directory.split('/')[-1] + "_combine.txt")
        # Write header to the new file
        header = [
            "$TTL 86400\n",
            "@ SOA localhost. admin.safedns.com.au. 1710796200 43200 3600 259200 300\n",
            "  NS  localhost.\n"
        ]
        with open(base_file, 'w') as file:
            file.writelines(header)

    # Validate and combine all RPZ files in the directory
    for rpz_file in glob.glob(os.path.join(directory, '*.txt')):
        validate_file(rpz_file, base_file)

if __name__ == "__main__":
    directory = sys.argv[1]
    base_file = sys.argv[2] if len(sys.argv) > 2 else None
    combine_files(directory, base_file)

