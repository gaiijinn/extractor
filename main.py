import asyncio
import time
from parser.email_extractor import EmailExtractor

from parser_helpers.cleaners.email_cleaner import RemoveDuplicatesEmails
from parser_helpers.csv_readers.csv_reader import CSVMultiReader
from parser_helpers.savers.email_saver import EmailSaver


async def main():
    start_time = time.perf_counter()  # Засекаем время начала

    # Создание парсера
    parser = CSVMultiReader(["uuid", "homepage_url"], file_path="crunchbase_data/test.csv")
    rows = await parser.read_file()  # Используем await для асинхронного вызова

    # Извлечение email'ов
    extractor = EmailExtractor(data=rows)
    await extractor.process_csv()  # Используем await для асинхронной функции

    emails = extractor.get_result()

    # Удаление дубликатов
    remover = RemoveDuplicatesEmails(emails)
    data = await remover.remove_duplicates()  # Используем await для асинхронного вызова

    # Сохранение результата
    saver = EmailSaver(output_file="finals/email.csv", data=data)
    await saver.save_result()  # Используем await для асинхронной функции

    end_time = time.perf_counter()  # Засекаем время окончания
    elapsed_time = end_time - start_time  # Разница во времени
    print(f"Execution time: {elapsed_time:.2f} seconds")


# Запуск основной асинхронной функции
if __name__ == "__main__":
    asyncio.run(main())
