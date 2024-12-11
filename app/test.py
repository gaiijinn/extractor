
import os
from io import BytesIO

import pytest
from fastapi.testclient import TestClient

from app.app import app

client = TestClient(app)

@pytest.fixture
def sample_csv_file(tmpdir):
    """Створює тимчасовий CSV файл для тестування."""
    csv_content = "homepage_url\nhttps://example.com\nhttps://test.com\n"
    file_path = os.path.join(tmpdir, "test.csv")
    with open(file_path, "w") as f:
        f.write(csv_content)
    return file_path


def test_process_file_with_default_params(sample_csv_file): #pass
    """Тестує ендпоінт із використанням параметрів за замовчуванням."""
    with open(sample_csv_file, "rb") as file:
        response = client.post(
            "/process/",
            files={"file": file}
        )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "success"
    assert isinstance(response_data["result"], list)

def test_process_file_with_custom_params(sample_csv_file): #fail
    """Тестує ендпоінт із вказаними потоками, процесами та іншими параметрами."""
    with open(sample_csv_file, "rb") as file:
        response = client.post(
            "/process/?threads=20&processes=4&row_names=homepage_url",
            files={"file": file}
        )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "success"
    assert isinstance(response_data["result"], list)

def test_process_file_with_custom_params_without_file():  # Тест без файлу
    response = client.post(
        "/process/?threads=20&processes=4&row_names=homepage_url"
    )
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "success"

def test_process_file_invalid_file(): #fail
    """Тестує обробку некоректного файлу."""
    response = client.post(
        "/process/",
        files={"file": ("test.txt", b"This is not a CSV file")}
    )
    assert response.status_code == 422  # У вашому коді буде повернено помилку
    response_data = response.json()
    assert response_data["status"] == "error"
    assert "detail" in response_data

def test_process_file_missing_params(sample_csv_file): #pass
    """Тестує ендпоінт, коли параметри не передано."""
    with open(sample_csv_file, "rb") as file:
        response = client.post(
            "/process/",
            files={"file": file}
        )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "success"
    assert isinstance(response_data["result"], list)

def test_process_file_invalid_params(sample_csv_file): #fpass
    """Тестує ендпоінт із некоректними параметрами."""
    with open(sample_csv_file, "rb") as file:
        response = client.post(
            "/process/?threads=-1&processes=0",  # Некоректні значення
            files={"file": file}
        )
    assert response.status_code == 422  # FastAPI автоматично валідує ці параметри


########

def test_extract_emails_success():
    # Підготовка тестового файлу
    file_content = b"uuid,column1,column2\n123,foo@example.com,bar@example.com\n"
    file = BytesIO(file_content)
    file.name = "test.csv"

    # Параметри для запиту
    fields = ["column1", "column2"]

    response = client.post(
        "/extract_emails/",
        files={"file": ("test.csv", file, "text/csv")},
        data={"fields": fields}
    )

    assert response.status_code == 200
    assert "results" in response.json()
    assert len(response.json()["results"]) > 0
    assert "emails" in response.json()["results"][0]


# Тест на випадок, коли файл не передано
def test_extract_emails_no_file(): #pass
    response = client.post(
        "/extract_emails/",
        data={"fields": '["column1", "column2"]'}
    )

    assert response.status_code == 422  # HTTP статус для помилок валідації


# Тест на випадок, коли параметри некоректні
def test_extract_emails_invalid_fields(): #pass
    # Підготовка тестового файлу
    file_content = b"uuid,column1,column2\n123,foo@example.com,bar@example.com\n"
    file = BytesIO(file_content)
    file.name = "test.csv"

    # Некоректні параметри
    response = client.post(
        "/extract_emails/",
        files={"file": ("test.csv", file, "text/csv")},
        data={"fields": '["non_existing_field"]'}
    )

    assert response.status_code == 422  # HTTP статус для помилок валідації


# Тест на випадок, коли сталася помилка при обробці
def test_extract_emails_processing_error(): #pass
    # Підготовка тестового файлу
    file_content = b"uuid,column1,column2\n123,foo@example.com,bar@example.com\n"
    file = BytesIO(file_content)
    file.name = "test.csv"

    # Симулюємо помилку в процесі обробки (наприклад, якщо CSV не можна прочитати)
    response = client.post(
        "/extract_emails/",
        files={"file": ("test.csv", file, "text/csv")},
        data={"fields": ["column1", "column2"]}
    )

    assert response.status_code == 500  # HTTP статус для помилок сервера
    assert "Error during email extraction" in response.json()["detail"]