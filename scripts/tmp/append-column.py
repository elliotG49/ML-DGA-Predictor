# Define the input and output file paths
input_file = '/root/project-mitnick/dictionaries/wordlist.10000'
output_file = '/root/project-mitnick/dictionaries/english-wordlist.csv'

# Open the input file and read its contents
with open(input_file, 'r') as file:
    words = file.readlines()

# Remove any trailing newline characters and join words with commas
csv_content = ','.join(word.strip() for word in words)

# Write the CSV content to the output file
with open(output_file, 'w') as file:
    file.write(csv_content)

print(f"CSV file created at {output_file}")
