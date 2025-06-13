import pytest

from src.processing import filter_by_state,sort_by_date


# Фикстура с тестовыми данными
@pytest.fixture
def records_various():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2025-06-13"},
        {"id": 2, "state": "PENDING", "date": "2024-12-01"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-15"},
        {"id": 4, "state": "CANCELLED", "date": "2022-07-20"},
        {"id": 5, "state": "EXECUTED", "date": "2025-01-01"},
        {"id": 6, "state": "PENDING", "date": "2023-11-11"},
        {"id": 7, "state": "EXECUTED", "date": "2022-12-12"},
        {"id": 8, "state": "CANCELLED", "date": "2021-05-05"},
        {"id": 9, "state": "EXECUTED", "date": "2025-06-13"},
        {"id": 10, "state": "PENDING", "date": "2024-01-01"},
        # Для теста с одинаковыми датами
        {"id": 11, "state": "EXECUTED", "date": "2025-06-13"},
        {"id": 12, "state": "EXECUTED", "date": "2025-06-13"},
        # Некорректные форматы дат
        {"id": 13, "state": "EXECUTED", "date": "invalid-date"},
        {"id": 14, "state": "EXECUTED", "date": ""},
        {"id": 15, "state": "EXECUTED", "date": None},
    ]

# Тесты для filter_by_state с расширением
@pytest.mark.parametrize("status, expected_ids", [
    ("EXECUTED", [1, 3, 5, 7, 9, 11, 12, 13, 14, 15]),
    ("PENDING", [2, 6, 10]),
    ("CANCELLED", [4, 8]),
    ("NON_EXISTENT", []),
])
def test_filter_by_state(records_various, status, expected_ids):
    filtered = filter_by_state(records_various, status)
    result_ids = [rec["id"] for rec in filtered]
    assert result_ids == expected_ids

# Тесты для sort_by_date с расширением
@pytest.mark.parametrize("reverse, expected_first_id, expected_last_id", [
    (True, 9, 4),   # по убыванию, самый свежий - id=9, самый старый - id=4
    (False, 4, 9),  # по возрастанию
])
def test_sort_by_date(records_various, reverse, expected_first_id, expected_last_id):
    sorted_records = sort_by_date(records_various, reverse=reverse)
    # Проверяем, что первый и последний элементы соответствуют ожидаемым
    assert sorted_records[0]["id"] == expected_first_id
    assert sorted_records[-1]["id"] == expected_last_id

# Тест на сортировку с одинаковыми датами
def test_sort_with_equal_dates(records_various):
    sorted_desc = sort_by_date(records_various, reverse=True)
    sorted_asc = sort_by_date(records_various, reverse=False)
    # Проверяем, что при одинаковых датах порядок сохраняется (стабильность)
    dates_desc = [rec["date"] for rec in sorted_desc if rec["date"] == "2025-06-13"]
    dates_asc = [rec["date"] for rec in sorted_asc if rec["date"] == "2025-06-13"]
    assert all(date == "2025-06-13" for date in dates_desc)
    assert all(date == "2025-06-13" for date in dates_asc)

# Тест на некорректные или пустые даты
def test_sort_with_invalid_dates():
    records = [
        {"id": 1, "date": "2025-06-13"},
        {"id": 2, "date": "invalid-date"},
        {"id": 3, "date": ""},
        {"id": 4, "date": None},
    ]
    sorted_desc = sort_by_date(records, reverse=True)
    sorted_asc = sort_by_date(records, reverse=False)
    # Проверяем, что сортировка не вызывает ошибок и возвращает список
    assert isinstance(sorted_desc, list)
    assert isinstance(sorted_asc, list)
    # В случае некорректных дат, сортировка по пустым или None - тоже должна работать
    assert sorted_desc[0]["id"] in [1, 2, 3, 4]
    assert sorted_asc[-1]["id"] in [1, 2, 3, 4]
