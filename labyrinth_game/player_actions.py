from .constants import ROOMS
from .utils import (
    attempt_open_treasure,
    describe_current_room,
    italics_text,
    random_event,
)


def use_item(game_state: dict, item_name: str) -> None:
    """
    Использование игроком предмета

    Args:
        game_state (dict): Текущее состояние игры.
        item_name (str): Название предмета.
    """

    if item_name not in game_state["player_inventory"]:
        print(italics_text("Нет такого предмета"))
        return

    match item_name:
        case "torch":
            print(italics_text("Стало светлее"))
        case "sword":
            print(italics_text("Страх отступает. " +
                "Этот меч — ваша надежда в глубинах лабиринта"))
        case "treasure_key":
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                print(italics_text(f"{item_name} можно использовать только " +
                                   "в комнате treasure_room"))
        case "bronze_box":
            print(italics_text("*звук открывания шкатулки*"))
            if "rusty_key" not in game_state["player_inventory"]:
                game_state["player_inventory"].remove(item_name)
                game_state["player_inventory"].append("rusty_key")
                print(italics_text("rusty_key добавлен в инвентарь"))
            else:
                print(italics_text("У вас уже есть rusty_key"))
        case _:
            print(italics_text(f"Непонятно, как использовать {item_name}"))



def take_item(game_state: dict, item_name: str) -> None:
    """
    Позволяет игроку поднять предмет в текущей комнате.

    Args:
        game_state (dict): Текущее состояние игры.
        item_name (str): Название предмета.
    """

    room = ROOMS.get(game_state["current_room"])
    items_room = room.get("items")
    if item_name in items_room:
        if item_name == "treasure_chest":
            print(italics_text("Вы не можете поднять сундук, он слишком тяжелый"))
        else:
            game_state["player_inventory"].append(item_name)
            ROOMS[game_state["current_room"]]["items"].remove(item_name)
            print(italics_text(f"Вы подняли: {item_name}"))
    else:
        print(italics_text("Такого предмета здесь нет"))


def move_player(game_state: dict, direction: str) -> None:
    """
    Перемещает игрока в указанном направлении, если это возможно.

    Args:
        game_state (dict): Текущее состояние игры.
        direction (str): Направление движения.
    """

    room = ROOMS.get(game_state["current_room"])
    exits = room.get("exits")
    if direction in exits:
        if exits[direction] == "treasure_room" and \
                "rusty_key" not in game_state["player_inventory"]:
            print(italics_text("Дверь заперта. Нужен ключ, чтобы пройти дальше"))
            return

        elif exits[direction] == "treasure_room" and \
                "rusty_key" in game_state["player_inventory"]:
            print(italics_text("Вы используете найденный ключ," +
                  "чтобы открыть путь в комнату сокровищ"))

        game_state["current_room"] = exits[direction]
        game_state["steps_taken"] += 1
        describe_current_room(game_state)
        random_event(game_state)
    else:
        print(italics_text("Нельзя пойти в этом направлении"))


def show_inventory(game_state) -> None:
    """
    Показывает инвентарь игрока, если он есть.

    Args:
        game_state (dict): Текущее состояние игры.
    """

    if game_state.get("player_inventory"):
        print(italics_text("Инвентарь: " + ", ".join(game_state["player_inventory"])))
    else:
        print(italics_text("Инвентарь пуст"))


def get_input(prompt:str = "> ") -> str:
    """
    Безопасный ввод команды от пользователя.

    Args:
        prompt (str): текст приглашения для ввода (по умолчанию "> ").

    Returns:
        str: введённая строка или "quit" в случае прерывания.
    """

    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        return "quit"
