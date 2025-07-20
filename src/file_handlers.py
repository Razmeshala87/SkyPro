import csv
import json
from typing import Any, Dict, List, Union

import openpyxl


def load_json(filename: str) -> List[Dict[str, Union[str, int, float, bool, None]]]:
    """Загружает данные из JSON файла"""
    with open(filename, 'r', encoding='utf-8') as f:
        data: List[Dict[str, Union[str, int, float, bool, None]]] = json.load(f)
        return data


def load_csv(filename: str) -> List[Dict[str, str]]:
    """Загружает данные из CSV файла"""
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_xlsx(filename: str) -> List[Dict[str, Any]]:
    """Загружает данные из XLSX файла"""
    workbook = openpyxl.load_workbook(filename)
    sheet = workbook.active

    if sheet is None:
        return []

    headers = [str(cell.value) if cell.value is not None else ""
               for cell in sheet[1]]  # type: ignore[index]

    data: List[Dict[str, Any]] = []
    for row in sheet.iter_rows(min_row=2, values_only=True):  # type: ignore[union-attr]
        row_dict = {}
        for header, cell_value in zip(headers, row):
            row_dict[header] = cell_value
        data.append(row_dict)

    return data
