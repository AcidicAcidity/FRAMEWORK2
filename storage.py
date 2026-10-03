"""Сохранение и загрузка данных проекта в JSON-файлах."""
import json
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
CARS_FILE = DATA_DIR / "cars.json"
TRIPS_FILE = DATA_DIR / "trips.json"


class StorageError(Exception):
    """Ошибка чтения или записи файла данных."""


def _read_json(filename: Path) -> list[dict]:
    """Прочитать список записей из JSON-файла.

    Если файла нет, возвращается пустой список.
    """
    try:
        with open(filename, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise StorageError(
            f"файл {filename.name} повреждён: {error}"
        ) from error
    except OSError as error:
        raise StorageError(
            f"не удалось прочитать {filename.name}: {error}"
        ) from error
    if not isinstance(data, list):
        raise StorageError(f"файл {filename.name} должен содержать список")
    return data


def _write_json(filename: Path, data: list[dict]) -> None:
    """Записать список записей в JSON-файл."""
    try:
        filename.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except OSError as error:
        raise StorageError(
            f"не удалось записать {filename.name}: {error}"
        ) from error


def load_cars(filename: Path = CARS_FILE) -> list[dict]:
    """Загрузить автомобили из JSON-файла."""
    return _read_json(filename)


def save_cars(cars: list[dict], filename: Path = CARS_FILE) -> None:
    """Сохранить автомобили в JSON-файл."""
    _write_json(filename, cars)


def load_trips(filename: Path = TRIPS_FILE) -> list[dict]:
    """Загрузить поездки из JSON-файла (дата строки -> объект date)."""
    trips = _read_json(filename)
    try:
        for trip in trips:
            trip["trip_date"] = date.fromisoformat(trip["trip_date"])
    except (KeyError, TypeError, ValueError) as error:
        raise StorageError(
            f"файл {filename.name} содержит некорректную запись: {error}"
        ) from error
    return trips


def save_trips(trips: list[dict], filename: Path = TRIPS_FILE) -> None:
    """Сохранить поездки в JSON-файл (объект date -> строка ISO)."""
    data = [
        {**trip, "trip_date": trip["trip_date"].isoformat()}
        for trip in trips
    ]
    _write_json(filename, data)
