from datetime import datetime

# Функция 1: Регистрация автомобиля владельцем
def register_car(brand: str, model: str, number: str, owner: str) -> str:
    """Проверяет данные автомобиля и регистрирует его в системе."""
    if len(brand) == 0:
        return "Ошибка: не указана марка автомобиля."
    if len(model) == 0:
        return "Ошибка: не указана модель автомобиля."
    if len(number) == 0:
        return "Ошибка: не указан государственный номер."
    if len(owner) == 0:
        return "Ошибка: не указан владелец автомобиля."
    return f"Автомобиль {brand} {model} ({number}) зарегистрирован владельцем {owner}."

# Функция 2: Проверка доступности автомобиля
def check_availability(is_available: bool) -> str:
    """Возвращает статус доступности автомобиля."""
    if is_available:
        return "Автомобиль доступен для аренды."
    return "Автомобиль занят и недоступен для аренды."

# Функция 3: Расчёт стоимости поездки
def calculate_price(hours: int, price_per_hour: int) -> str:
    """Считает стоимость поездки и применяет скидку при длительной аренде."""
    total = hours * price_per_hour
    if hours >= 24:
        discount = total * 0.15
        final_price = total - discount
        return f"Стоимость поездки: {int(final_price)} руб. (применена скидка 15% за аренду от 24 часов)."
    elif hours >= 6:
        discount = total * 0.05
        final_price = total - discount
        return f"Стоимость поездки: {int(final_price)} руб. (применена скидка 5% за аренду от 6 часов)."
    else:
        return f"Стоимость поездки: {total} руб."

# Функция 4: Оформление поездки
def create_trip(user: str, car: str, hours: int) -> str:
    """Формирует описание поездки пользователя."""
    if hours <= 0:
        return "Ошибка: длительность поездки должна быть больше нуля."
    if len(user) == 0:
        return "Ошибка: не указан пользователь."
    return f"Поездка оформлена. Пользователь: {user}. Автомобиль: {car}. Длительность: {hours} ч."

# Функция 5: Полный вывод информации о поездке
def display_trip(user, car, owner, hours, price, trip_date):
    print("            СИСТЕМА КАРШЕРИНГА — КАРТОЧКА ПОЕЗДКИ")
    print(f"ДАТА ПОЕЗДКИ : {trip_date}")
    print(f"ПОЛЬЗОВАТЕЛЬ : {user}")
    print(f"АВТОМОБИЛЬ   : {car}")
    print(f"ВЛАДЕЛЕЦ     : {owner}")
    print(f"ДЛИТЕЛЬНОСТЬ : {hours} ч.")
    print(f"СТОИМОСТЬ    : {price}")

print("     СИСТЕМА СОВМЕСТНОГО ИСПОЛЬЗОВАНИЯ АВТОМОБИЛЕЙ")

# 1. Ввод данных пользователем
owner = input("Введите имя владельца автомобиля: ")
brand = input("Введите марку автомобиля: ")
model = input("Введите модель автомобиля: ")
number = input("Введите государственный номер: ")

user = input("Введите имя пользователя (арендатора): ")

hours_str = input("Введите длительность поездки в часах (только цифры): ")
hours = int(hours_str)

price_str = input("Введите стоимость аренды за 1 час (только цифры): ")
price_per_hour = int(price_str)

availability_str = input("Автомобиль доступен? (да/нет): ")
is_available = availability_str.lower() == "да"

# 2. Вызов функций
status_register = register_car(brand, model, number, owner)
status_availability = check_availability(is_available)
status_price = calculate_price(hours, price_per_hour)
status_trip = create_trip(user, f"{brand} {model}", hours)
trip_date = datetime.now().strftime('%d.%m.%Y %H:%M')

# 3. Вывод промежуточных результатов
print("\n" + status_register)
print(status_availability)
print(status_trip)

# 4. Вывод полностью оформленной карточки поездки
if is_available and "Ошибка" not in status_register and "Ошибка" not in status_trip:
    display_trip(user, f"{brand} {model} ({number})", owner, hours, status_price, trip_date)
else:
    print("\nПоездка не может быть оформлена. Проверьте данные или доступность автомобиля.")
