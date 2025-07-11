import os
import sys
from pathlib import Path
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.decorators import log  # noqa: E402


def test_file_logging(tmp_path: Path) -> None:
    """Тестирование логирования в файл."""
    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def test_func(x: int, y: int) -> int:
        return x * y

    assert test_func(3, 4) == 12
    with open(log_file, "r", encoding="utf-8") as f:
        logs = f.read()
        assert "test_func started" in logs
        assert "test_func ok" in logs

    with pytest.raises(ZeroDivisionError):
        @log(filename=str(log_file))
        def div(a: int, b: int) -> float:
            return a / b

        div(1, 0)

    with open(log_file, "r", encoding="utf-8") as f:
        logs = f.read()
        assert "ZeroDivisionError" in logs
        assert "Inputs: (1, 0)" in logs


def test_console_logging(capsys: pytest.CaptureFixture) -> None:
    """Тестирование логирования в консоль."""

    @log()
    def test_func(a: int, b: int) -> int:
        return a + b

    assert test_func(2, 3) == 5
    captured = capsys.readouterr()
    assert "test_func started" in captured.out
    assert "test_func ok" in captured.out

    with pytest.raises(ZeroDivisionError):
        @log()
        def div(a: int, b: int) -> float:
            return a / b

        div(1, 0)

    captured = capsys.readouterr()
    assert "ZeroDivisionError" in captured.out
    assert "Inputs: (1, 0)" in captured.out


def test_log_without_filename(capsys: pytest.CaptureFixture) -> None:
    """Тестирование декоратора без указания filename."""

    @log()
    def greet(name: str) -> str:
        return f"Hello, {name}"

    result = greet("Alice")
    assert result == "Hello, Alice"
    captured = capsys.readouterr()
    assert "greet started" in captured.out
    assert "greet ok" in captured.out


def test_log_with_filename(tmp_path: Path) -> None:
    """Тестирование декоратора с указанием filename."""
    log_file = tmp_path / "output.log"

    @log(filename=str(log_file))
    def multiply(x: float, y: float) -> float:
        return x * y

    result = multiply(2.5, 4.0)
    assert result == 10.0
    with open(log_file, "r", encoding="utf-8") as f:
        logs = f.read()
        assert "multiply started" in logs
        assert "multiply ok" in logs
