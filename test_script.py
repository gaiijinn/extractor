import csv

# Файлы
input_file = 'crunchbase_data/organizations.csv'
output_file = 'crunchbase_data/investors.csv'

filter_column = 'primary_role'
filter_value = 'investor'

# Читаем и записываем данные
with open(input_file, mode='r', encoding='utf-8') as infile, \
        open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile)  # Читаем файл с заголовками
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)  # Создаем объект записи

    writer.writeheader()  # Пишем заголовки в новый файл

    for row in reader:
        if row[filter_column] == filter_value:  # Проверяем условие
            writer.writerow(row)  # Записываем строку, если условие выполнено