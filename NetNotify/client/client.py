import curses
from client.interface import display_menu # curses-интерфейс

if __name__ == "__main__":
    try:
        curses.wrapper(display_menu)
    except Exception as e:
        print(f"Ошибка в curses.wrapper: {e}")
