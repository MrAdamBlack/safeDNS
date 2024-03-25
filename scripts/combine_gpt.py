import sys
import os
import re

def combine_rpz_files(directory, base_file=None):
    # Initialize set to store combined entries
    combined_entries = set()

    # If base file is provided, read its content and add to combined entries
    if base_file:
        with open(base_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith(';') and not line.startswith('$TTL') and not line.startswith('@') and not line.startswith('NS'):
                    combined_entries.add(line)

    # Get list of RPZ files in the directory
    rpz_files = [f for f in os.listdir(directory) if f.endswith('.txt')]

    # Combine entries from RPZ files in the directory
    for rpz_file in rpz_files:
        with open(os.path.join(directory, rpz_file), 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith(';') and not line.startswith('$TTL') and not line.startswith('@') and not line.startswith('NS'):
                    combined_entries.add(line)

    # Extract directory name
    directory_name = os.path.basename(os.path.normpath(directory))

    # Write combined entries to a new file in the current directory
    output_file = os.path.join(os.getcwd(), f"{directory_name}_combined.txt")
    with open(output_file, 'w') as combined_file:
        combined_file.write("$TTL 86400\n")
        combined_file.write("@ SOA localhost. admin.safedns.com.au. 1710796200 43200 3600 259200 300\n")
        combined_file.write("  NS localhost.\n")
        for entry in sorted(combined_entries):
            combined_file.write(entry + '\n')

    print(f"Combination and deduplication successful. Output written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 script.py /path/to/rpz/files/ [baseFile.txt]")
        sys.exit(1)

    directory = sys.argv[1]
    base_file = sys.argv[2] if len(sys.argv) == 3 else None

    combine_rpz_files(directory, base_file)

