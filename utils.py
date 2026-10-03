"""Вспомогательные функции: безопасный ввод данных и форматирование."""
from datetime import date, datetime
from typing import Iterable, Optional

DATE_FORMAT = "%d.%m.%Y"


def input_str(prompt: str) -> str:
    """Запросить непустую строку; при пустом вводе повторить запрос."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: значение не может быть пустым.")


def input_int(prompt: str, min_value: Optional[int] = None) -> int:
    """Запросить целое число; при ошибке ввода повторить запрос."""
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")
            continue
        if min_value is not None and value < min_value:
            print(f"Ошибка: число должно быть не меньше {min_value}.")
            continue
        return value


def input_date(prompt: str) -> date:
    """Запросить дату в формате ДД.ММ.ГГГГ; при ошибке повторить запрос."""
    while True:
        text = input(prompt).strip()
        try:
            return datetime.strptime(text, DATE_FORMAT).date()
        except ValueError:
            print("Ошибка: введите дату в формате ДД.ММ.ГГГГ.")


def input_yes_no(prompt: str) -> bool:
    """Запросить ответ «да»/«нет»; при ошибке повторить запрос."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("да", "д", "yes", "y"):
            return True
        if answer in ("нет", "н", "no", "n"):
            return False
        print("Ошибка: ответьте «да» или «нет».")


def format_date(value: date) -> str:
    """Вернуть дату в формате ДД.ММ.ГГГГ."""
    return value.strftime(DATE_FORMAT)


def next_id(ids: Iterable[int]) -> int:
    """Вернуть следующий свободный идентификатор."""
    return max(ids, default=0) + 1
