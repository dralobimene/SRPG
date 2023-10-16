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

        self.displayed = True
        self.focused = False

    # def set_focus(self, has_focus: bool):
    #     print(f"Setting focus for {self.__class__.__name__} to {has_focus}")
    #     self.focused = has_focus
    #     self._alpha = 100 if has_focus else 255
