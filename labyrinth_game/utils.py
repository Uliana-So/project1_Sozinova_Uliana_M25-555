import math

from .constants import (
    COMMANDS,
    EVENT_PROBABILITY,
    EVENT_TYPE,
    ROOMS,
)


def red_text(text):
    return "\033[31m{}\033[0m".format(text)


def red_italics_text(text):
    return "\033[3m\033[31m{}\033[0m".format(text)


def green_text(text):
    return "\033[32m{}\033[0m".format(text)


def yellow_text(text):
    return "\033[33m{}\033[0m".format(text)


def yellow_italics_text(text):
    return "\033[3m\033[33m{}\033[0m".format(text)


def blue_text(text):
    return "\033[34m{}\033[0m".format(text)


def turquoise_text(text):
    return "\033[36m{}\033[0m".format(text)


def bold_text(text):
    return "\033[1m{}\033[0m".format(text)


def italics_text(text):
    return "\033[3m{}\033[0m".format(text)


def underlined_text(text):
    return "\033[4m{}\033[0m".format(text)


def attempt_open_treasure(game_state: dict) -> None:
    from .player_actions import get_input

    room = ROOMS.get(game_state['current_room'])
    puzzle = room.get('puzzle')
    items_room = room.get('items')

    if "treasure_chest" not in items_room:
        print(italics_text("В комнате нет сундука"))
        return

    if 'treasure_key' in game_state["player_inventory"]:
        print(green_text("Вы применяете ключ, и замок щёлкает. Сундук открыт! " +
                         "В сундуке сокровище! Вы победили!"))
        ROOMS[game_state['current_room']]['items'].remove("treasure_chest")
        game_state["game_over"] = True
    else:
        answer = get_input("Сундук заперт. ... Ввести код? (да/нет) ")
        if answer.lower() == "да":
            code = get_input("Код: ")
            if code == puzzle[1]:
                print(green_text("Замок щёлкнул и раскрылся! Вы открыли сундук и " +
                                 "нашли сокровища! Поздравляем — вы победили!"))
                ROOMS[game_state['current_room']]['items'].remove("treasure_chest")
                game_state["game_over"] = True
            else:
                print(red_text("Замок не поддаётся. Магия защищает сундук..."))
        else:
            print(italics_text("Вы отступаете от сундука"))


def solve_puzzle(game_state: dict) -> None:
    from .player_actions import get_input

    room = ROOMS.get(game_state['current_room'])
    puzzle = room.get('puzzle')
    if not puzzle:
        print(italics_text("Загадок здесь нет"))
        return

    # альтернативные ответы для некоторых загадок
    alt_answers = {
        "10": ["10", "десять", "ten"],
    }

    print(turquoise_text(puzzle[0]))
    user_answer = get_input("Ваш ответ: ").lower().strip()
    correct_answer = puzzle[1]

    if correct_answer in alt_answers:
        if user_answer in alt_answers[correct_answer]:
            is_correct = True
        else:
            is_correct = False
    else:
        is_correct = user_answer == correct_answer
        
    if is_correct:
        ROOMS[game_state['current_room']]['puzzle'] = None
        print(green_text("Правильно!"))
        if "treasure_key" not in game_state["player_inventory"]:
            game_state["player_inventory"].append('treasure_key')
            print(italics_text("treasure_key добавлен в инвентарь"))
    else:
        print(red_text("Неверно. Попробуйте снова"))


def describe_current_room(game_state: dict) -> None:
    room = ROOMS.get(game_state['current_room'])
    description = room.get('description')
    items_room = room.get('items')
    exits = room.get('exits')
    puzzle = room.get('puzzle')

    print(yellow_text(f'\n\t== {game_state['current_room'].upper()} =='))
    if description:
        print(yellow_italics_text(description))
    if items_room:
        print(underlined_text('Заметные предметы:') + " " + 
              ', '.join(items_room))
    if exits:
        print(underlined_text('Выходы:') + " " +
              ", ".join(f"{d} -> {r}" for d, r in exits.items()))
    if puzzle:
        print("Кажется, здесь есть загадка (используйте команду solve)")
    print()


def show_help() -> None:
    print(bold_text("\nДоступные команды:"))
    for i, v in COMMANDS.items():
        print(f"{i:<16} — {v}")


def pseudo_random(seed, modulo) -> int:
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional = x - math.floor(x)
    return int(fractional * modulo)


def trigger_trap(game_state: dict) -> None:
    print(italics_text("Ловушка активирована! Пол стал дрожать..."))

    inventory = game_state.get("player_inventory")
    seed = game_state.get("steps_taken")

    if inventory:
        item_index = pseudo_random(seed, len(inventory))
        lost_item = inventory.pop(item_index)
        print(italics_text(f"Вы потеряли предмет: {lost_item}!"))
        return

    danger_value = pseudo_random(seed, EVENT_PROBABILITY)

    if danger_value < 3:
        print(red_text("Ловушка была смертельной! Игра окончена..."))
        game_state["game_over"] = True
    else:
        print(italics_text("Вы чудом выжили! Но не расслабляйтесь..."))


def random_event(game_state):
    seed = game_state.get("steps_taken")
    current_room = game_state.get("current_room")
    inventory = game_state.get("inventory")

    # Определяем, произойдет ли событие (пример: шанс 1 из 10)
    if pseudo_random(seed, EVENT_PROBABILITY) != 0:
        return

    print(blue_text("\nСлучайное событие происходит...\n"))

    # Выбор сценария (0–2)
    event_type = pseudo_random(seed, EVENT_TYPE)

    # Находка монетки
    if event_type == 0:
        print(italics_text("Вы нашли на полу монетку!"))
        room = ROOMS.get(current_room)
        if room is not None:
            room.setdefault("items", []).append("coin")
        return

    # Испуг
    if event_type == 1:
        print(italics_text("Где-то рядом послышался шорох..."))
        if "sword" in inventory:
            print(italics_text("Вы вскинули меч, и существо убежало прочь!"))
        return

    # Ловушка (только в trap_room и без факела)
    if event_type == 2:
        if current_room == "trap_room" and "torch" not in inventory:
            print(italics_text("Кажется, в этой комнате опасно..."))
            trigger_trap(game_state)
        else:
            print(italics_text("Вы услышали тихий щелчок, но ничего не произошло."))
