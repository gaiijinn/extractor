import csv


input_file = 'crunchbase_data/organizations.csv'
output_file = '../crunchbase_data/investors.csv'

filter_column = 'primary_role'
filter_value = 'investor'

with open(input_file, mode='r', encoding='utf-8') as infile, \
        open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)

    writer.writeheader()

    for row in reader:
        if row[filter_column] == filter_value:
            writer.writerow(row)