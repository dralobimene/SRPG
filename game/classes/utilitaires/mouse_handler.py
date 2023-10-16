# Fichier: classes/utilitaires/mouse_handler.py


class MouseHandler:
    def __init__(self,
                 screen,
                 window_manager):

        self.screen = screen
        self.window_manager = window_manager
        self.current_focused_canvas = None

    # ========================================================================

    def detect_and_display(self,
                           mouse_x,
                           mouse_y,
                           canvas_maps_rect,
                           canvas_droite_rect,
                           canvas_informations_rect,
                           canvas_aide):

        print("=================================================")

        # Coordonnées absolues
        print(f"Absolute Mouse coordinates X: {mouse_x}, Y: {mouse_y}")

        for canvas_rect, canvas_name in [(canvas_maps_rect, 'canvas01_maps'),
                                         (canvas_droite_rect, 'canvas02_droite'),
                                         (canvas_informations_rect, 'canvas03_informations'),
                                         (canvas_aide, 'canvas_aide')]:

            # Affiche le nom du canvas sur lequel est la souris.
            if canvas_rect.collidepoint(mouse_x, mouse_y):
                # Coordonnées relatives
                relative_x = mouse_x - canvas_rect.x
                relative_y = mouse_y - canvas_rect.y

                print(f"Mouse is over {canvas_name}")

                # Permet...
                # Parcourir dans l'ordre inverse pour accorder le focus au canvas du dessus
                for canvas in reversed(self.window_manager.canvas_list):
                    rect = canvas.get_rect(topleft=(canvas.x, canvas.y))
                    if rect.collidepoint(mouse_x, mouse_y):
                        if canvas != self.current_focused_canvas:
                            print(
                                f"Changing focus to {canvas.__class__.__name__}")
                            self.window_manager.set_focus(canvas)
                            self.current_focused_canvas = canvas
                            print(
                                f"Current focused canvas: {self.current_focused_canvas.__class__.__name__}")

                print(
                    f"Relative Mouse Coordinates: ({relative_x}, {relative_y})")

                print("=================================================")

                return
