# Fichier: classes/canvases/WindowManager.py

from classes.canvases.canvas01_cartes import Maps01Canvas
from classes.canvases.canvas02_droite import Right01Canvas
from classes.canvases.canvas03_informations import InformationsCanvas
from classes.canvases.canvas_aide import HelpCanvas
from classes.canvases.canvas_inventaire import InventoryCanvas


class WindowManager:
    def __init__(self):

        # Liste des canvas dans l'ordre de leur z-index
        self.canvas_list = []

        #
        self.focused_canvas = None

    def add_canvas(self, canvas):
        self.canvas_list.append(canvas)

    def remove_canvas(self, canvas):
        self.canvas_list.remove(canvas)

    def bring_to_front(self, canvas):
        self.remove_canvas(canvas)
        self.add_canvas(canvas)

    def set_focus(self, canvas):
        if self.focused_canvas:
            self.focused_canvas.is_focused = False
        self.focused_canvas = canvas
        self.focused_canvas.is_focused = True

    def set_focus_to_maps(self):
        for canvas in self.canvas_list:
            if isinstance(canvas, Maps01Canvas):
                self.set_focus(canvas)
                return

    def show_canvas(self, canvas_type):
        for canvas in self.canvas_list:
            if isinstance(canvas, canvas_type):
                canvas.is_displayed = True
                self.set_focus(canvas)
                return

    def hide_canvas(self, canvas_type):
        for canvas in self.canvas_list:
            if isinstance(canvas, canvas_type):
                canvas.is_displayed = False
                canvas.is_focused = False
                break

    def is_additional_canvas_displayed(self, canvas_type):
        for canvas in self.canvas_list:
            if canvas.is_displayed and isinstance(canvas, canvas_type):
                return True
        return False

    def hide_all_additional_canvases(self):
        additional_canvases = [HelpCanvas, InventoryCanvas]
        for canvas in self.canvas_list:
            if type(canvas) in additional_canvases:
                canvas.is_displayed = False
                canvas.is_focused = False

    def is_any_additional_canvas_displayed(self):
        additional_canvases = [HelpCanvas, InventoryCanvas]
        for canvas in self.canvas_list:
            if type(canvas) in additional_canvases and canvas.is_displayed:
                return True
        return False

    def render_all(self, screen):
        for canvas in self.canvas_list:
            if canvas.is_displayed:
                if canvas.is_focused:
                    canvas.alpha = 255
                else:
                    canvas.alpha = 100
                canvas.draw(screen)

    def process_events(self, event):
        pass
