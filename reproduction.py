import csv
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key
from datetime import datetime
import time
import random

# Файл с записанными действиями
filename = 'recorded_events.csv'

# Переменная для определения случайности времени записи
random_time_offset = {
    'normal': 0.5,   # Случайное время от 0 до 0.5 секунд для режима normal
    'special': 0.2   # Случайное время от 0 до 0.2 секунд для режима special
}

# Функция для воспроизведения записей из CSV файла
def replay_recorded_events():
    mouse = MouseController()
    keyboard = KeyboardController()

    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Пропускаем заголовок

        for row in reader:
            timestamp, event_type, details, mode = row
            timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')

            # Вычисляем случайное время задержки в зависимости от режима
            if mode == 'normal':
                random_offset = random.uniform(0, random_time_offset['normal'])
            elif mode == 'special':
                random_offset = random.uniform(0, random_time_offset['special'])
            else:
                random_offset = 0  # По умолчанию нет случайной задержки

            # Вычисляем время ожидания с учетом случайной задержки
            wait_time = (timestamp - datetime.now()).total_seconds() + random_offset

            # Ожидаем до момента события
            if wait_time > 0:
                time.sleep(wait_time)

            # Воспроизводим событие
            try:
                if event_type == 'mouse_click':
                    action, button_info = details.split(' ', 1)
                    button = getattr(Button, button_info)
                    if action == 'Pressed':
                        mouse.press(button)
                    elif action == 'Released':
                        mouse.release(button)
                elif event_type == 'mouse_scroll':
                    direction, coordinates = details.split(' ', 1)
                    x, y = eval(coordinates)
                    if direction == 'Scrolled':
                        mouse.scroll(x, y)
                elif event_type == 'key_press':
                    if details == 'Page Down (toggle mode)':
                        keyboard.press(Key.page_down)
                        keyboard.release(Key.page_down)
                    elif details == 'Page Up (stop recording)':
                        keyboard.press(Key.page_up)
                        keyboard.release(Key.page_up)
                    else:
                        key = getattr(Key, details) if hasattr(Key, details) else details
                        keyboard.press(key)
                        keyboard.release(key)
            except ValueError:
                print(f"Ошибка в записи: невозможно разделить детали '{details}'")
            except Exception as e:
                print(f"Произошла ошибка при воспроизведении записи: {e}")

# Вызов функции для воспроизведения записей
replay_recorded_events()