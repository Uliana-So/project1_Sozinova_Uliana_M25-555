from .constants import ROOMS
from .utils import (
    attempt_open_treasure,
    describe_current_room,
    italics_text,
)


def use_item(game_state, item_name):
    if item_name not in game_state["player_inventory"]:
        print("Нет такого предмета")
        return

    match item_name:
        case "torch":
            print(italics_text("Стало светлее"))
        case "sword":
            print(italics_text("Страх отступает." +
                "Этот меч — ваша надежда в глубинах лабиринта"))
        case "treasure_key":
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                print("Этот предмет можно использовать только в комнате treasure_room")
        case "bronze_box":
            print(italics_text("*звук открывания шкатулки*"))
            if "rusty_key" not in game_state["player_inventory"]:
                game_state["player_inventory"].append(item_name)
                print("rusty_key добавлен в инвентарь")
            else:
                print("У вас уже есть rusty_key")
        case _:
            print("Непонятно, как использовать {}".format(item_name))



def take_item(game_state, item_name):
    room = ROOMS.get(game_state['current_room'])
    items_room = room.get('items')
    if item_name in items_room:
        if item_name == "treasure_chest":
            print("Вы не можете поднять сундук, он слишком тяжелый")
            return
        game_state['player_inventory'].append(item_name)
        ROOMS[game_state['current_room']]['items'].remove(item_name)
        print("Вы подняли:", item_name)
    else:
        print("Такого предмета здесь нет")


def move_player(game_state, direction):
    room = ROOMS.get(game_state['current_room'])
    exits = room.get('exits')
    if direction in exits:
        game_state["current_room"] = exits[direction]
        game_state['steps_taken'] += 1
        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении")


def show_inventory(game_state):
    if game_state.get('player_inventory'):
        print("Инвентарь:", ", ".join(game_state['player_inventory']))
    else:
        print("Инвентарь пуст")


def get_input(prompt="> "):
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        return "quit"
