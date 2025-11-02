#!/usr/bin/env python3

from .constants import ROOMS


game_state = {
    'player_inventory': [],
    'current_room': 'entrance',
    'game_over': False,
    'steps_taken': 0
}
  
def main():
    print("Первая попытка запустить проект!")
