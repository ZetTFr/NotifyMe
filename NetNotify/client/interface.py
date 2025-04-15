import os
import tempfile
import subprocess
from datetime import datetime
import subprocess
import time
import win32gui
import win32con
import win32process
import curses
import socket

# Функция для сканирования сети (поиск всех устройств в сети)
def scan_network(network='192.168.1.0/24'):
    import nmap
    nm = nmap.PortScanner()
    nm.scan(hosts=network, arguments='-sn')  # Scan only for live hosts
    live_hosts = []
    for host in nm.all_hosts():
        live_hosts.append(host)
    return live_hosts

# Получаем имя компьютера (имя хоста)
computer_name = os.environ.get('COMPUTERNAME', 'UnknownPC')  # для Windows

# Функция отправки уведомления
def send_notification(user, message, delay, recurring):
    print(f"Отправка уведомления для {user}")
    print(f"Сообщение: {message}")
    print(f"Задержка: {delay} секунд")
    print(f"Цикличность: {'Да' if recurring else 'Нет'}")

    time.sleep(delay)

    sender = os.environ.get('COMPUTERNAME', 'UnknownPC')
    receiver = user
    date_str = datetime.now().strftime('%Y-%m-%d')
    time_str = datetime.now().strftime('%H-%M-%S')

    # Получаем путь до корня проекта (NetNotify)
    base_dir = os.path.dirname(os.path.abspath(__file__))  # client/
    project_root = os.path.abspath(os.path.join(base_dir, "..", ".."))  # NetNotify/
    send_message_root = os.path.join(project_root, "send message")
    os.makedirs(send_message_root, exist_ok=True)

    # Создание подкаталогов
    dir_path = os.path.join(send_message_root, f"{sender}__{receiver}", date_str)
    os.makedirs(dir_path, exist_ok=True)

    # Путь к текстовому файлу
    file_path = os.path.join(dir_path, f"{time_str}.txt")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(message)

    # Открытие файла в блокноте
    process = subprocess.Popen(['notepad.exe', file_path])

    # Поднимаем окно блокнота наверх
    time.sleep(0.5)
    def enum_windows_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if file_path in title or time_str in title:
                win32gui.SetForegroundWindow(hwnd)
                win32gui.SetWindowPos(
                    hwnd, win32con.HWND_TOPMOST,
                    0, 0, 0, 0,
                    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
                )
    win32gui.EnumWindows(enum_windows_callback, None)

    print(f"Уведомление отправлено пользователю {user}")

# Основной интерфейс с возможностью навигации
def display_menu(stdscr):
    curses.curs_set(0)  # Скрыть курсор
    stdscr.clear()

    # Сканируем сеть для получения всех доступных компьютеров
    live_hosts = scan_network()

    users = [computer_name] + live_hosts  # Добавляем текущий компьютер в список

    current_selection = 0
    menu = ["Выбор пользователя", "Настройки времени", "Настройки цикличности", "Выход"]

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        for idx, item in enumerate(menu):
            if idx == current_selection:
                stdscr.addstr(height // 2 + idx, width // 2 - len(item) // 2, item, curses.A_REVERSE)
            else:
                stdscr.addstr(height // 2 + idx, width // 2 - len(item) // 2, item)

        key = stdscr.getch()

        if key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1
        elif key == curses.KEY_DOWN and current_selection < len(menu) - 1:
            current_selection += 1
        elif key == 10:  # Enter
            if current_selection == 0:
                user_input(stdscr, users)  # Переход в "Выбор пользователя"
            elif current_selection == 1:
                # Настройки времени
                pass
            elif current_selection == 2:
                # Настройки цикличности
                pass
            elif current_selection == 3:
                break  # Выход

        stdscr.refresh()

# Функция для выбора пользователя и отправки уведомлений
def user_input(stdscr, users):
    current_selection = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        stdscr.addstr(height // 2 - len(users) // 2 - 2, width // 2 - 20, "Выберите пользователя для уведомления:")

        for i, user in enumerate(users):
            y = height // 2 - len(users) // 2 + i
            if i == current_selection:
                stdscr.addstr(y, width // 2 - len(user) // 2, f"{user}", curses.A_REVERSE)
            else:
                stdscr.addstr(y, width // 2 - len(user) // 2, f"{user}")

        key = stdscr.getch()

        if key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1
        elif key == curses.KEY_DOWN and current_selection < len(users) - 1:
            current_selection += 1
        elif key == 10:  # Enter
            break

    user = users[current_selection]

    # Обычный ввод в консоли (можно позже тоже сделать curses-интерфейсом)
    curses.endwin()
    message = input("Введите сообщение для уведомления: ")
    delay = int(input("Введите задержку в секундах перед отправкой уведомления: "))
    recurring = input("Уведомление будет цикличным? (Да/Нет): ").strip().lower() == "да"

    send_notification(user, message, delay, recurring)

# Основная функция, которая запускает интерфейс
if __name__ == "__main__":
    curses.wrapper(display_menu)
