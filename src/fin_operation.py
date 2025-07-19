import csv
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet


class TransactionState(Enum):
    EXECUTED = "EXECUTED"
    CANCELED = "CANCELED"
    PENDING = "PENDING"


@dataclass
class Transaction:
    id: int
    state: TransactionState
    date: datetime
    amount: float
    currency_name: str
    currency_code: str
    from_account: Optional[str]
    to_account: str
    description: str


def read_transactions_from_csv(file_path: str) -> List[Transaction]:
    """
    Чтение транзакций из CSV-файла

    Args:
        file_path: Путь к CSV-файлу

    Returns:
        Список объектов Transaction
    """
    transactions: List[Transaction] = []

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')

        for row in reader:
            # Пропускаем пустые строки
            if not row.get('id'):
                continue

            try:
                transaction = Transaction(
                    id=int(row['id']),
                    state=TransactionState(row['state']),
                    date=datetime.strptime(row['date'], '%Y-%m-%dT%H:%M:%SZ'),
                    amount=float(row['amount']),
                    currency_name=row['currency_name'],
                    currency_code=row['currency_code'],
                    from_account=row['from'] if row['from'] else None,
                    to_account=row['to'],
                    description=row['description']
                )
                transactions.append(transaction)
            except (ValueError, KeyError) as e:
                print(f"Ошибка при обработке строки {row}: {e}")
                continue

    return transactions


def read_transactions_from_excel(file_path: str, sheet_name: Optional[str] = None) -> List[Transaction]:
    """
    Чтение транзакций из Excel-файла
    """
    transactions: List[Transaction] = []
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook[sheet_name] if sheet_name else workbook.active

    if not isinstance(sheet, Worksheet):
        raise ValueError("Invalid sheet type")

    headers = [str(cell.value) if cell.value is not None else "" for cell in sheet[1]]

    for row in sheet.iter_rows(min_row=2, values_only=True):
        if not row[0]:
            continue

        row_dict = dict(zip(headers, row))
        try:
            transaction = Transaction(
                id=int(str(row_dict['id'])),
                state=TransactionState(str(row_dict['state'])),
                date=datetime.strptime(str(row_dict['date']), '%Y-%m-%dT%H:%M:%SZ'),
                amount=float(str(row_dict['amount'])),
                currency_name=str(row_dict['currency_name']),
                currency_code=str(row_dict['currency_code']),
                from_account=str(row_dict['from']) if row_dict.get('from') else None,
                to_account=str(row_dict['to']),
                description=str(row_dict['description'])
            )
            transactions.append(transaction)
        except (ValueError, KeyError, TypeError) as e:
            print(f"Ошибка при обработке строки {row_dict}: {e}")
            continue

    return transactions


def get_transaction_stats(transactions: List[Transaction]) -> Dict[str, Any]:
    """
    Получение статистики по транзакциям

    Args:
        transactions: Список транзакций

    Returns:
        Словарь с различной статистикой
    """
    if not transactions:
        return {}

    stats: Dict[str, Any] = {
        'total_transactions': len(transactions),
        'executed_count': sum(1 for t in transactions if t.state == TransactionState.EXECUTED),
        'canceled_count': sum(1 for t in transactions if t.state == TransactionState.CANCELED),
        'pending_count': sum(1 for t in transactions if t.state == TransactionState.PENDING),
        'total_amount': sum(t.amount for t in transactions),
        'currencies': {t.currency_code for t in transactions},
        'first_date': min(t.date for t in transactions),
        'last_date': max(t.date for t in transactions)
    }

    return stats
