# Fichier: classes/canvases/canvas_inventaire.py


from classes.canvases.canvas00_base import BaseCanvas


class InventoryCanvas(BaseCanvas):
    def __init__(self,
                 width: int,
                 height: int) -> None:

        super().__init__(width,
                         height,
                         color=(255, 0, 0),
                         x=0,
                         y=0,
                         alpha=255)

        self.is_displayed = False
        self.is_focused = False
