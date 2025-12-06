import logging
import functools
import sys
from datetime import datetime


def logger(func=None, *, handle=sys.stdout):
    """
    Декоратор для логирования вызовов функций.

    Args:
        func: Декорируемая функция.
        handle: Поток для вывода логов или экземпляр logging.Logger.
    """

    def resolve_writers():
        """
        В зависимости от типа handle возвращает две функции:
        info_writer(message) и error_writer(message).
        """
        if isinstance(handle, logging.Logger):

            def info_writer(message: str) -> None:
                handle.info(message)

            def error_writer(message: str) -> None:
                handle.error(message)
        else:
            def write(prefix: str, text: str) -> None:
                handle.write(f"{prefix}{text}\n")

            def info_writer(message: str) -> None:
                write("INFO: ", message)

            def error_writer(message: str) -> None:
                write("ERROR: ", message)

        return info_writer, error_writer

    info_log, error_log = resolve_writers()

    def timestamp() -> str:
        """Вернуть текущий момент времени в виде строки."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def format_call(fn, args, kwargs) -> str:
        """
        Сформировать представление вызова функции
        """
        parts = []
        if args:
            parts.extend(repr(arg) for arg in args)
        if kwargs:
            parts.extend(f"{name}={repr(value)}" for name, value in kwargs.items())
        joined = ", ".join(parts)
        return f"{fn.__name__}({joined})"

    def decorator(target):
        @functools.wraps(target)
        def wrapped(*args, **kwargs):
            call_repr = format_call(target, args, kwargs)
            info_log(f"[{timestamp()}] Вызов функции {call_repr}")

            try:
                result = target(*args, **kwargs)
            except Exception as exc:
                error_log(
                    f"[{timestamp()}] "
                    f"В функции {target.__name__} произошло исключение "
                    f"{type(exc).__name__}: {exc}"
                )
                raise
            else:
                info_log(
                    f"[{timestamp()}] "
                    f"Функция {target.__name__} успешно завершена. "
                    f"Результат: {repr(result)}"
                )
                return result

        return wrapped

    if func is not None and callable(func):
        return decorator(func)

    return decorator
