# Fichier: classes/canvases/canvas02_droite.py


from classes.canvases.canvas00_base import BaseCanvas


class Right01Canvas(BaseCanvas):
    def __init__(self,
                 width: int,
                 height: int) -> None:

        super().__init__(width,
                         height,
                         color=(0, 255, 0),
                         x=800,
                         y=0,
                         alpha=255)

        self.is_displayed = True
        self.is_focused = False
