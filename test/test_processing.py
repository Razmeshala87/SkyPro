from typing import Any, Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


# Фикстуры с тестовыми данными
@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-10-01T12:00:00.000"},
        {"id": 2, "state": "PENDING", "date": "2023-10-02T12:00:00.000"},
        {"id": 3, "state": "EXECUTED", "date": "2023-09-01T12:00:00.000"},
        {"id": 4, "state": "CANCELED", "date": "2023-08-01T12:00:00.000"},
        {"id": 5, "state": "EXECUTED", "date": "2023-10-01T12:00:00.000"},
        {"id": 6, "date": "2023-11-01T12:00:00.000"},
    ]


@pytest.fixture
def edge_case_transactions() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "invalid_date"},
        {"id": 2, "state": "PENDING"},
        {"id": 3},
    ]


# Тесты для filter_by_state
@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3, 5]),
        ("PENDING", [2]),
        ("CANCELED", [4]),
        ("UNKNOWN", []),
        (None, [6]),
    ],
)
def test_filter_by_state(sample_transactions: List[Dict[str, Any]], state: str, expected_ids: List[int]) -> None:
    filtered = filter_by_state(sample_transactions, state)
    assert [t["id"] for t in filtered] == expected_ids


def test_filter_by_state_empty_input() -> None:
    assert filter_by_state([], "EXECUTED") == []


# Тесты для sort_by_date
@pytest.mark.parametrize(
    "reverse, expected_order",
    [
        (True, [6, 2, 1, 5, 3, 4]),
        (False, [4, 3, 1, 5, 2, 6]),
    ],
)
def test_sort_by_date(sample_transactions: List[Dict[str, Any]], reverse: bool, expected_order: List[int]) -> None:
    sorted_transactions = sort_by_date(sample_transactions, reverse)
    assert [t["id"] for t in sorted_transactions] == expected_order


def test_sort_by_date_with_same_dates(sample_transactions: List[Dict[str, Any]]) -> None:
    sorted_transactions = sort_by_date(sample_transactions, True)
    ids = [t["id"] for t in sorted_transactions]
    assert 1 in ids and 5 in ids


def test_sort_by_date_edge_cases(edge_case_transactions: List[Dict[str, Any]]) -> None:
    sorted_transactions = sort_by_date(edge_case_transactions, True)
    assert len(sorted_transactions) == 3


def test_sort_by_date_empty_input() -> None:
    assert sort_by_date([], True) == []
