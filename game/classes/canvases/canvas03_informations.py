# Fichier: classes/canvases/canvas03_informations.py


from classes.canvases.canvas00_base import BaseCanvas


class InformationsCanvas(BaseCanvas):
    def __init__(self,
                 width: int,
                 height: int) -> None:

        super().__init__(width,
                         height,
                         color=(128, 128, 128),
                         x=0,
                         y=600,
                         alpha=255)

        self.is_displayed = True
        self.is_focused = False
