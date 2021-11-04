import pyautogui
import time
from random import randint
class Configuration:


    def __init__(self, configuration):
        self.window = configuration["Window Name"]
        self.A = configuration["Controls"]["A"]
        self.B = configuration["Controls"]["B"]
        self.Start = configuration["Controls"]["Start"]
        self.Select = configuration["Controls"]["Select"]
        self.L = configuration["Controls"]["L"]
        self.R = configuration["Controls"]["R"]
        self.Right = configuration["Controls"]["Right"]
        self.Left = configuration["Controls"]["Left"]
        self.Up = configuration["Controls"]["Up"]
        self.Down = configuration["Controls"]["Down"]
        self.last_move = None
        self.prev_move = None

    def reset_game(self):
        pyautogui.keyDown(self.L)
        pyautogui.keyDown(self.R)
        pyautogui.keyDown(self.Start)
        pyautogui.keyDown(self.Select)
        pyautogui.keyUp(self.Select)
        pyautogui.keyUp(self.Start)
        pyautogui.keyUp(self.R)
        pyautogui.keyUp(self.L)
    
    def skip_dialog(self):
        pyautogui.keyDown(self.A)
        pyautogui.keyUp(self.A)
        time.sleep(0.5)
    
    def move_pokemon_selection(self):
        pyautogui.keyDown(self.Left)
        pyautogui.keyUp(self.Left)
        time.sleep(0.5)
    

    def move_trainer(self):
        possible_moves = [self.Up, self.Down, self.Left, self.Right]
    
        while True:
            move = randint(0, len(possible_moves)-1)
            if possible_moves[move] != self.last_move:
                self.last_move = possible_moves[move]
                break
        
        pyautogui.keyDown(possible_moves[move])
        pyautogui.keyUp(possible_moves[move])
        time.sleep(0.2)
    
    def run_from_battle(self):
        time.sleep(0.4)
        pyautogui.keyDown(self.Left)
        pyautogui.keyUp(self.Left)
        pyautogui.keyDown(self.Left)
        pyautogui.keyUp(self.Left)
        pyautogui.keyDown(self.Right)
        pyautogui.keyUp(self.Right)
        self.skip_dialog()