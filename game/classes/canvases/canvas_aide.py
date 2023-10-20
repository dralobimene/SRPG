# Fichier: classes/canvases/canvas_help.py


from classes.canvases.canvas00_base import BaseCanvas


class HelpCanvas(BaseCanvas):
    def __init__(self,
                 width: int,
                 height: int) -> None:

        super().__init__(width,
                         height,
                         color=(0, 255, 0),
                         x=100,
                         y=100,
                         alpha=255)

        self.is_displayed = False
        self.is_focused = False
