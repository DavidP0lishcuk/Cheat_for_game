import csv
from pynput import mouse, keyboard
from datetime import datetime

# Флаг для определения режима записи и остановки
is_recording = True
special_mode = False

# Файл для записи данных
filename = 'recorded_events.csv'

# Функция для записи данных в CSV файл
def write_to_csv(event_type, details):
    global special_mode
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    mode = 'special' if special_mode else 'normal'
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, event_type, details, mode])

# Обработчик событий мыши
def on_click(x, y, button, pressed):
    if is_recording:
        action = 'Pressed' if pressed else 'Released'
        write_to_csv('mouse_click', f'{action} {button} at ({x}, {y})')

def on_scroll(x, y, dx, dy):
    if is_recording:
        write_to_csv('mouse_scroll', f'Scrolled {"down" if dy < 0 else "up"} at ({x}, {y})')

# Обработчик событий клавиатуры
def on_press(key):
    global is_recording, special_mode

    if key == keyboard.Key.page_down:
        special_mode = not special_mode
        write_to_csv('key_press', 'Page Down (toggle mode)')
    elif key == keyboard.Key.page_up:
        is_recording = False
        write_to_csv('key_press', 'Page Up (stop recording)')
        return False  # Остановить слушатель клавиатуры

    if is_recording:
        try:
            write_to_csv('key_press', f'{key.char}')
        except AttributeError:
            write_to_csv('key_press', f'{key}')

def on_release(key):
    if is_recording:
        try:
            write_to_csv('key_release', f'{key.char}')
        except AttributeError:
            write_to_csv('key_release', f'{key}')

# Инициализация CSV файла
with open(filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'event_type', 'details', 'mode'])

# Запуск слушателей
mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

mouse_listener.start()
keyboard_listener.start()

keyboard_listener.join()  # Дождаться завершения слушателя клавиатуры
mouse_listener.stop()  # Остановить слушатель мыши, когда клавиатурный слушатель завершен