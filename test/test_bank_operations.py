from typing import Any, Dict, List

import pytest

from src.bank_operations import (filter_by_status, filter_rub_only, process_bank_operations, process_bank_search,
                                 sort_by_date)


@pytest.fixture
def sample_data() -> List[Dict[str, Any]]:
    return [
        {
            'id': 1,
            'description': 'Payment for groceries',
            'status': 'EXECUTED',
            'date': '2023-01-15',
            'currency_code': 'RUB'
        },
        {
            'id': 2,
            'description': 'Salary deposit',
            'status': 'EXECUTED',
            'date': '2023-01-10',
            'currency_code': 'USD'
        },
        {
            'id': 3,
            'description': 'Online purchase',
            'status': 'CANCELED',
            'date': '2023-01-05',
            'currency_code': 'EUR'
        },
        {
            'id': 4,
            'description': 'Grocery store payment',
            'status': 'PENDING',
            'date': '2023-01-20',
            'currency_code': 'RUB'
        },
        {
            'id': 5,
            'description': 'Restaurant bill',
            'status': 'EXECUTED',
            'date': '2023-01-12',
            'currency_code': 'RUB'
        },
        {
            'id': 6,
            'description': 'No status operation',
            'date': '2023-01-18'
        }
    ]


class TestProcessBankSearch:
    def test_search_by_word(self, sample_data: List[Dict[str, Any]]) -> None:
        result = process_bank_search(sample_data, r'\bgrocery\b')
        assert len(result) == 1
        assert result[0]['id'] == 4

    def test_case_insensitive_search(self, sample_data: List[Dict[str, Any]]) -> None:
        result = process_bank_search(sample_data, 'PAYMENT')
        assert len(result) == 2
        assert {op['id'] for op in result} == {1, 4}

    def test_no_matches(self, sample_data: List[Dict[str, Any]]) -> None:
        assert not process_bank_search(sample_data, 'nonexistent')

    def test_empty_data(self) -> None:
        assert not process_bank_search([], 'test')

    def test_special_chars_in_search(self, sample_data: List[Dict[str, Any]]) -> None:
        modified_data = sample_data + [{'description': 'Special $100 payment'}]
        result = process_bank_search(modified_data, r'\$100')
        assert len(result) == 1

    def test_empty_string_search(self, sample_data: List[Dict[str, Any]]) -> None:
        result = process_bank_search(sample_data, '')
        assert len(result) == len([op for op in sample_data if 'description' in op])


class TestProcessBankOperations:
    def test_category_counting(self, sample_data: List[Dict[str, Any]]) -> None:
        categories = ['grocery', 'payment', 'salary', 'nonexistent']
        result = process_bank_operations(sample_data, categories)
        assert result == {'grocery': 1, 'payment': 2, 'salary': 1, 'nonexistent': 0}

    def test_empty_categories(self, sample_data: List[Dict[str, Any]]) -> None:
        assert not process_bank_operations(sample_data, [])

    def test_empty_data(self) -> None:
        assert process_bank_operations([], ['test']) == {'test': 0}

    def test_partial_matches(self, sample_data: List[Dict[str, Any]]) -> None:
        result = process_bank_operations(sample_data, ['store', 'bill'])
        assert result == {'store': 1, 'bill': 1}


class TestFilterByStatus:
    def test_executed_status(self, sample_data: List[Dict[str, Any]]) -> None:
        result = filter_by_status(sample_data, 'executed')
        assert len(result) == 3
        assert {op['id'] for op in result} == {1, 2, 5}

    def test_case_insensitivity(self, sample_data: List[Dict[str, Any]]) -> None:
        result = filter_by_status(sample_data, 'PeNdInG')
        assert len(result) == 1
        assert result[0]['id'] == 4

    def test_no_status_field(self, sample_data: List[Dict[str, Any]]) -> None:
        result = filter_by_status(sample_data, 'EXECUTED')
        assert len(result) == 3
        assert {op['id'] for op in result} == {1, 2, 5}

    def test_nonexistent_status(self, sample_data: List[Dict[str, Any]]) -> None:
        assert not filter_by_status(sample_data, 'nonexistent')


class TestSortByDate:
    def test_ascending_sort(self, sample_data: List[Dict[str, Any]]) -> None:
        result = sort_by_date(sample_data)
        assert [op['id'] for op in result] == [3, 2, 5, 1, 6, 4]

    def test_descending_sort(self, sample_data: List[Dict[str, Any]]) -> None:
        result = sort_by_date(sample_data, reverse=True)
        assert [op['id'] for op in result] == [4, 6, 1, 5, 2, 3]

    def test_missing_date_fields(self) -> None:
        data: List[Dict[str, Any]] = [{'id': 1}, {'id': 2, 'date': '2023-01-01'}]
        result = sort_by_date(data)
        assert [op['id'] for op in result] == [1, 2]

    def test_invalid_date_format(self) -> None:
        data = [{'date': 'invalid'}, {'date': '2023-01-01'}]
        result = sort_by_date(data)
        assert [op['date'] for op in result] == ['2023-01-01', 'invalid']


class TestFilterRubOnly:
    def test_rub_transactions(self, sample_data: List[Dict[str, Any]]) -> None:
        result = filter_rub_only(sample_data)
        assert len(result) == 3
        assert {op['id'] for op in result} == {1, 4, 5}

    def test_no_rub_transactions(self) -> None:
        data: List[Dict[str, Any]] = [{'currency_code': 'USD'}, {'currency_code': 'EUR'}]
        assert not filter_rub_only(data)

    def test_missing_currency_field(self) -> None:
        data: List[Dict[str, Any]] = [{'id': 1}, {'currency_code': 'RUB'}]
        result = filter_rub_only(data)
        assert len(result) == 1
        assert result[0]['currency_code'] == 'RUB'


class TestEdgeCases:
    def test_none_data(self) -> None:
        with pytest.raises(TypeError):
            process_bank_search(None, 'test')  # type: ignore[arg-type]

    def test_invalid_data_types(self) -> None:
        with pytest.raises(AttributeError):
            process_bank_operations([{'description': 123}], ['test'])  # type: ignore[arg-type]

    def test_mixed_data_structures(self) -> None:
        data = [{'status': 'EXECUTED'}, {}, {}]
        result = filter_by_status(data, 'executed')
        assert len(result) == 1
