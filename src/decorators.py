import functools
from datetime import datetime
from typing import Callable, TypeVar, Any, Optional

T = TypeVar('T')  # Обобщенный тип для возвращаемого значения функции


def log(filename: Optional[str] = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Декоратор для логирования выполнения функций."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message_start = f"{start_time} - {func.__name__} started\n"
            log_message_success = f"{start_time} - {func.__name__} ok\n"
            log_message_error = (
                f"{start_time} - {func.__name__} error: {{error_type}}. Inputs: {args}, {kwargs}\n"
            )

            # Логируем начало выполнения
            if filename:
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(log_message_start)
            else:
                print(log_message_start, end="")

            try:
                result = func(*args, **kwargs)
                # Логируем успешное завершение
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message_success)
                else:
                    print(log_message_success, end="")
                return result
            except Exception as e:
                # Логируем ошибку
                error_message = log_message_error.format(error_type=type(e).__name__)
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(error_message)
                else:
                    print(error_message, end="")
                raise  # Пробрасываем ошибку дальше

        return wrapper
    return decorator
