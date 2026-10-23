from datetime import date

# ----- Сущность: Пользователь -----
client_name = "Иванов Иван Иванович"
client_phone = "+7 999 123-45-67"

# ----- Сущность: Автомобиль -----
car_model = "Kia Rio"
car_license_plate = "Е777ОУ777"

# ----- Сущность: Парковочное место -----
parking_spot_id = 15
is_spot_covered = True
is_spot_available = True

# ----- Сущность: Период бронирования (импортируемый тип date) -----
booking_start = date(2026, 9, 20)
booking_end = date(2026, 9, 25)

# ----- Операции и преобразование типов -----
daily_rate = 450.75
booking_days = (booking_end - booking_start).days
total_price_float = booking_days * daily_rate
total_price_int = int(total_price_float)  # преобразование типов: float -> int

# ----- Ветвления (if / elif / else) -----
#breakpoint()
if not is_spot_available:
    print("[ОШИБКА] Выбранное парковочное место уже занято.")
elif booking_days <= 0:
    print("[ОШИБКА] Неверно указан период бронирования.")
else:
    if is_spot_covered:
        spot_type = "Крытое"
    else:
        spot_type = "Открытое"

    print("=" * 45)
    print("   ЧЕК БРОНИРОВАНИЯ ПАРКОВОЧНОГО МЕСТА")
    print("=" * 45)
    print(f"Клиент: {client_name}")
    print(f"Телефон: {client_phone}")
    print(f"Автомобиль: {car_model} ({car_license_plate})")
    print(f"Место № {parking_spot_id} ({spot_type})")
    print(f"Период: с {booking_start} по {booking_end}")
    print(f"Количество дней: {booking_days}")
    print(f"Итоговая стоимость: {total_price_int} руб.")
    print("Статус: [OK] Бронирование подтверждено!")
    print("=" * 45)