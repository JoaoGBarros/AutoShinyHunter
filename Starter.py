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


class StarterReset:

    def __init__(self):
        self.starters = ["152", "155", "158"]
        self.reset_counter = 0
        self.found_pokemon = False
        self.found_shiny = False
        self.pokemon_counter = 0
        self.path = "Sprites/Shiny/"

    def Start_Hunting(self, wincap, control):
        while not self.found_shiny :
            for pokemon in self.starters:
                vision_pokemon = Vision(self.path + pokemon + ".png")
                while True:
                    screenshot = wincap.screenshot()
                    screenshot = screenshot[0:200, 0:300]
                    rectangles, self.found_pokemon = vision_pokemon.findPosition(screenshot, 0.3)

                    if not self.found_pokemon:
                        control.skip_dialog()

                    else:
                        output_image, self.found_shiny = vision_pokemon.draw_rectangles(screenshot, rectangles, pokemon)
                        show_screen(output_image, self.found_shiny)
                        if self.found_shiny:
                            print("Found a shiny")
                        break

                self.pokemon_counter += 1

                if self.pokemon_counter <= 2:
                    control.move_pokemon_selection()
                else:
                    if not self.found_shiny:
                        control.reset_game()
                        self.reset_counter += 1
                        self.pokemon_counter = 0
                        print(f"Reset {self.reset_counter}")

