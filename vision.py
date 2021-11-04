import cv2
import numpy as np
from deepgaze.color_classification import HistogramColorClassifier

class Vision:
    needle_img_path = None
    needle_w = 0
    needle_h = 0
    method = None

    def __init__(self, needle_img_path, method = cv2.TM_CCOEFF_NORMED):
        self.needle_img = cv2.imread(needle_img_path)    
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]
        self.method = method

    def findPosition(self, haystack_img, threshold = 0.5):
        pokemon_on_screen = False
        result = cv2.matchTemplate(haystack_img, self.needle_img, self.method)

        locations = np.where(result >= threshold)

        locations = list(zip(*locations[::-1]))

        rectangles = []

        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv2.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
        if len(rectangles) >= 1:
            pokemon_on_screen = True
        return rectangles, pokemon_on_screen

    def get_points(self, rectangles):
        points = []
    
        for (x, y, w, h) in rectangles:
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            points.append((center_x, center_y))
        
        return points

    def draw_rectangles(self, haystack_img, rectangles, pokemon_img):
        pokemon = None
        is_shiny = False
        line_color = (0, 0, 255)
        line_type = cv2.LINE_4

        for (x, y, w, h) in rectangles:

            top_left = (x, y)
            bottom_right = (x + w, y + h)

            cv2.rectangle(haystack_img, top_left, bottom_right, color=line_color, lineType=line_type)
            
            pokemon = haystack_img[y:y+h, x:x+w]
            break
        if len(rectangles) >= 1:
            is_shiny = self.compare(pokemon, pokemon_img)
        
        return haystack_img, is_shiny

    
    def draw_cross(self, haystack_img, points):

        marker_color = (0, 0, 255)
        marker_type = cv2.MARKER_CROSS

        for (center_x, center_y) in points:
            cv2.drawMarker(haystack_img, (center_x, center_y), marker_color, marker_type)
        
        return haystack_img

    def compare(self, pokemon, pokemon_img):
        my_classifier = HistogramColorClassifier(channels=[0, 1, 2],
                                         hist_size=[128, 128, 128], 
                                         hist_range=[0, 256, 0, 256, 0, 256], 
                                         hist_type='BGR')

        my_classifier.addModelHistogram(self.needle_img)
        pkm_shiny = cv2.imread(f"Sprites/Regular/{pokemon_img}.png")
        my_classifier.addModelHistogram(pkm_shiny)

        comparison_array = my_classifier.returnHistogramComparisonArray(pokemon, 
                                                                method="intersection")
        
        if comparison_array[1] > comparison_array[0]:
            return False
        else:
            return True

