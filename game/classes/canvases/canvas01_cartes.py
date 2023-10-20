# Fichier: classes/canvases/canvas01_cartes.py


from classes.canvases.canvas00_base import BaseCanvas


class Maps01Canvas(BaseCanvas):
    def __init__(self,
                 width: int,
                 height: int) -> None:

        super().__init__(width,
                         height,
                         color=(255, 255, 0),
                         x=0,
                         y=0,
                         alpha=255)

        self.is_displayed = True
        self.is_focused = False
