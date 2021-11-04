import pyautogui
import time
from vision import Vision
from windowcapture import WindowCapture
from config import Configuration
import cv2


def show_screen(output_image, shiny):
    cv2.imshow("ComputerVision", output_image)
    if cv2.waitKey(1) == ord('q') or shiny:
        cv2.destroyAllWindows()

class WildEncounter:

    def __init__(self, route, pokemon_list):
        self.route = route
        self.pokemon_list = pokemon_list
        self.encounter_counter = 0
        self.found_shiny = False
        self.found_pokemon = False
        self.path = "Sprites/Shiny/"
        self.in_battle = False
    

    def startWildHunting(self, wincap, control):

        while not self.found_shiny:
            vision_battle =  Vision("Sprites/hp_bar.png")
            while True:
                screenshot = wincap.screenshot()
                screenshot = screenshot[0:200, 0:300]
                rectangles, self.in_battle = vision_battle.findPosition(screenshot, 0.4)
                if not self.in_battle:
                    control.move_trainer()
                    time.sleep(0.5)
                else:
                    for pokemon in self.pokemon_list:
                        vision_pokemon = Vision(self.path + pokemon + ".png")
                        rectangles, self.found_pokemon = vision_pokemon.findPosition(screenshot, 0.2)
                        output_image, self.found_shiny = vision_pokemon.draw_rectangles(screenshot, rectangles, pokemon)
                        if self.found_shiny:
                            break
                    show_screen(output_image, self.found_shiny)
                    if self.found_shiny:
                        print("Found a shiny")
                        break
                    else:
                        control.run_from_battle()
                        time.sleep(0.5)
                        self.encounter_counter += 1
                        print(f"ENCOUNTER {self.encounter_counter}")