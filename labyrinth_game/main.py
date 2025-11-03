#!/usr/bin/env python3

from .player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from .utils import (
    describe_current_room,
    red_text,
    show_help,
    solve_puzzle,
)

game_state = {
    'player_inventory': [],
    'current_room': 'entrance',
    'game_over': False,
    'steps_taken': 0
}


def process_command(game_state, command):
    split_command = command.split()
    match split_command[0]:
        case "go":
            if len(split_command) != 2:
                print("ОШИБКА. Введите направление")
                return
            move_player(game_state, split_command[1])
        case "look":
            describe_current_room(game_state)
        case "take":
            if len(split_command) != 2:
                print("ОШИБКА. Введите предмет")
                return
            take_item(game_state, split_command[1])
        case "use":
            if len(split_command) != 2:
                print("ОШИБКА. Введите предмет")
                return
            use_item(game_state, split_command[1])
        case "inventory":
            show_inventory(game_state)
        case "solve":
            solve_puzzle(game_state)
        case "help":
            show_help()
        case "quit" | "exit":
            print("Выход из игры.")
            game_state['game_over'] = True
        case _:
            print("Неизвестная команда. Введите help.")


def main():
    print(red_text("Добро пожаловать в Лабиринт сокровищ!"))
    describe_current_room(game_state)
    while not game_state['game_over']:
        command = get_input()
        process_command(game_state, command)


if __name__ == '__main__':
    main()
