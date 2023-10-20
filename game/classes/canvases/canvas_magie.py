# Fichier: classes/canvases/canvas_magie.py


from classes.canvases.canvas00_base import BaseCanvas


class MagicalCanvas(BaseCanvas):
    def __init__(self,
                 width: int,
                 height: int) -> None:

        super().__init__(width,
                         height,
                         color=(0, 255, 255),
                         x=800,
                         y=0,
                         alpha=255)

        self.is_displayed = False
        self.is_focused = False
