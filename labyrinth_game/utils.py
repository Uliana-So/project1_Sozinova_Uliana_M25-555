from .constants import ROOMS


def red_text(text):
    return "\033[31m{}\033[0m".format(text)


def green_text(text):
    return "\033[32m{}\033[0m".format(text)


def yellow_text(text):
    return "\033[33m{}\033[0m".format(text)


def yellow_italics_text(text):
    return "\033[3m\033[33m{}\033[0m".format(text)


def blue_text(text):
    return "\033[34m{}\033[0m".format(text)


def violet_text(text):
    return "\033[35m{}\033[0m".format(text)


def bold_text(text):
    return "\033[1m{}\033[0m".format(text)


def italics_text(text):
    return "\033[3m{}\033[0m".format(text)


def underlined_text(text):
    return "\033[4m{}\033[0m".format(text)


def attempt_open_treasure(game_state):
    from .player_actions import get_input

    room = ROOMS.get(game_state['current_room'])
    puzzle = room.get('puzzle')
    items_room = room.get('items')

    if "treasure_chest" not in items_room:
        print("В комнате нет сундука")
        return

    if 'treasure_key' in game_state["player_inventory"]:
        print(green_text("Вы применяете ключ, и замок щёлкает. Сундук открыт!" +
                         "В сундуке сокровище! Вы победили!"))
        ROOMS[game_state['current_room']]['items'].remove("treasure_chest")
        game_state["game_over"] = True
    else:
        answer = get_input("Сундук заперт. ... Ввести код? (да/нет) ")
        if answer == "да":
            code = get_input("Код: ")
            if code == puzzle[1]:
                print(green_text("Замок щёлкнул и раскрылся! Вы открыли сундук и " +
                                 "нашли сокровища! Поздравляем — вы победили!"))
                ROOMS[game_state['current_room']]['items'].remove("treasure_chest")
                game_state["game_over"] = True
            else:
                print(red_text("Замок не поддаётся. Магия защищает сундук... пока что."
))
        else:
            print("Вы отступаете от сундука")


def solve_puzzle(game_state):
    from .player_actions import get_input

    room = ROOMS.get(game_state['current_room'])
    puzzle = room.get('puzzle')
    if not puzzle:
        print("Загадок здесь нет")
        return
    
    if game_state['current_room'] == "treasure_room" and \
            "treasure_key" not in game_state['current_room']:
        attempt_open_treasure(game_state)
        return

    print(violet_text(puzzle[0]))
    answer = get_input("Ваш ответ: ")
    if answer == puzzle[1]:
        ROOMS[game_state['current_room']]['puzzle'] = None
        print(green_text("Правильно!"))
        if "treasure_key" not in game_state["player_inventory"]:
            game_state["player_inventory"].append('treasure_key')
            print("Вы выиграли treasure_key. treasure_key добавлен в инвентарь")
    else:
        print(red_text("Неверно. Попробуйте снова"))


def describe_current_room(game_state):
    room = ROOMS.get(game_state['current_room'])
    description = room.get('description')
    items_room = room.get('items')
    exits = room.get('exits')
    puzzle = room.get('puzzle')

    print(yellow_text(f'\t== {game_state['current_room'].upper()} =='))
    if description:
        print(yellow_italics_text(description))
    if items_room:
        print(underlined_text('Заметные предметы:') + " " + ', '.join(items_room))
    if exits:
        print(underlined_text('Выходы:') + " " +
            ", ".join(f"{d} -> {r}" for d, r in exits.items()))
    if puzzle:
        print("Кажется, здесь есть загадка (используйте команду solve)")


def show_help():
    print(bold_text("\nДоступные команды:"))
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
