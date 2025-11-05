#!/usr/bin/env python3

from .constants import COMMANDS
from .player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from .utils import (
    attempt_open_treasure,
    describe_current_room,
    italics_text,
    red_italics_text,
    red_text,
    show_help,
    solve_puzzle,
)


def process_command(game_state: dict, command: str) -> None:
    """
    Обрабатывает пользовательскую команду и выполняет соответствующее действие.

    Args:
        game_state (dict): Текущее состояние игры.
        command (str): Строка, введенная пользователем.
    """

    if not command:
        print(italics_text("Введите команду (help - список команд)"))
        return

    split_command = command.lower().split()
    match split_command[0]:
        case "go" | "north" | "east" | "south" | "west":
            if split_command[0] in ["north", "east", "south", "west"]:
                move_player(game_state, split_command[0])
            elif split_command[0] == "go" and len(split_command) == 2:
                move_player(game_state, split_command[1])
            else:
                print(red_italics_text("Введите направление: north/east/south/west"))
        case "look":
            describe_current_room(game_state)
        case "take":
            if len(split_command) != 2:
                print(red_italics_text("Введите предмет"))
            else:
                take_item(game_state, split_command[1])
        case "use":
            if len(split_command) != 2:
                print(red_italics_text("Введите предмет"))
            else:
                use_item(game_state, split_command[1])
        case "inventory":
            show_inventory(game_state)
        case "solve":
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "help":
            show_help(COMMANDS)
        case "quit" | "exit":
            print(italics_text("Выход из игры."))
            game_state["game_over"] = True
        case _:
            print(red_italics_text("Неизвестная команда. Введите help."))


def main():
    """
    Основной игровой цикл.

    Функция инициализирует состояние игры, приветствует игрока и отображает
    первую комнату. Затем запускается бесконечный цикл обработки команд,
    который продолжается, пока игра не будет завершена.

    Структура game_state включает:
        - "player_inventory" (list[str]): инвентарь игрока
        - "current_room" (str): комната, в которой находится игрок
        - "game_over" (bool): флаг завершения игры
        - "steps_taken" (int): количество совершённых действий/передвижений
    """

    game_state = {
        "player_inventory": [],
        "current_room": "entrance",
        "game_over": False,
        "steps_taken": 0
    }
    
    print(red_text("Добро пожаловать в Лабиринт сокровищ!"))
    describe_current_room(game_state)
    while not game_state["game_over"]:
        command = get_input()
        process_command(game_state, command)


if __name__ == "__main__":
    main()
