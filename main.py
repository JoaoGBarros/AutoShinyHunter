import cv2
import numpy as np
import os
import pyautogui
import time
from windowcapture import WindowCapture
from vision import Vision
import json
from config import Configuration
from Starter import StarterReset
from wildEncounter import WildEncounter


def Opcoes():
    print("--------- Auto Shiny Hunter Pokemon HGSS ---------")
    print("1 - Johto Starter SoftReset\n2 - Wild Encounter\n3 - Headbutt\n4 - Static Encounter Soft Reset")
    option = int(input())
    return option
    

if __name__ == '__main__':
    configuration_file = json.load(open("controls.json")) 
    configuration = Configuration(configuration_file)
    option = Opcoes()
    wincap = WindowCapture(configuration.window)
    if option == 1:
        s = StarterReset()
        s.Start_Hunting(wincap, configuration)
    elif option == 2:
        route = input()
        pokemon_on_route = json.load(open("wildEncounters.json"))
        w = WildEncounter(route, pokemon_on_route[route])
        w.startWildHunting(wincap, configuration)
    elif option == 3:
        NotImplemented
    elif option == 4:
        NotImplemented
    else:
        print("Opcao invalida")