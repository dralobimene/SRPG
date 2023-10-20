# Fichier: classes/utilitaires/key_handler.py

import pygame
import sys

from datetime import datetime

from classes.utilitaires.utilitaires_01 import Utilitaires01
from classes.utilitaires.utilitaires_02_reseau import Utilitaires02Reseau

from classes.canvases.canvas_aide import HelpCanvas
from classes.canvases.canvas_inventaire import InventoryCanvas


class KeyHandler:
    def __init__(self,
                 websocket_client=None,
                 ip_client=None,
                 file_messages=None,
                 game_screen=None):

        # --------------------------------------------------------------------

        #
        self.game_screen = game_screen

        # Lire le fichier settings.json et obtenir la valeur de la clé "mode"
        self.settings_file = "settings.json"

        #
        self.mode = Utilitaires01.get_key_value_from_json(
            self.settings_file, "mode")

        # --------------------------------------------------------------------

        # Initialize the dictionaries
        self.global_dictionary = {
            pygame.K_F1: [self.handle_F1_pressed, self.handle_F1_released],
            pygame.K_ESCAPE: [self.handle_Esc_pressed, self.handle_Esc_released],
            pygame.K_s: [self.handle_s_pressed, self.handle_s_released],
            pygame.K_F2: [self.handle_F2_pressed, self.handle_F2_released],
            pygame.K_F3: [self.handle_F3_pressed, self.handle_F3_released],
            pygame.K_F4: [self.handle_F4_pressed, self.handle_F4_released]
        }

        self.help_dictionary = {
            pygame.K_F1: [self.handle_F1_pressed, self.handle_F1_released],
            pygame.K_ESCAPE: [self.handle_Esc_pressed, self.handle_Esc_released],
            pygame.K_F2: [None, self.handle_F2_released_help],
            pygame.K_F3: [None, self.handle_F3_released_help],
            pygame.K_F4: [None, self.handle_F4_released_help]
        }

        self.inventory_dictionary = {
            pygame.K_F1: [self.handle_F1_pressed, self.handle_F1_released],
            pygame.K_ESCAPE: [self.handle_Esc_pressed, self.handle_Esc_released],
            pygame.K_F2: [None, self.handle_F2_released_inventory],
            pygame.K_F3: [None, self.handle_F3_released_inventory],
            pygame.K_F4: [None, self.handle_F4_released_inventory]
        }

        self.states = {
            "default": self.global_dictionary,
            "help_canvas": self.help_dictionary,
            "inventory_canvas": self.inventory_dictionary
        }

        # --------------------------------------------------------------------

        if self.mode == "multiplayer":
            # Initialise les variables nécessaires pour l'envoi de messages
            self.websocket_client = websocket_client
            self.ip_client = ip_client
            self.file_messages = file_messages

        elif self.mode == "monoplayer":
            # Faire quelque chose si nécessaire
            pass

        else:
            print("Mode inconnu.")
            # Ou vous pouvez lancer une exception
            raise ValueError("Mode inconnu dans settings.json")

        # --------------------------------------------------------------------

    # ========================================================================

    def get_current_state(self):
        # from screen06_game import Screen06Game
        #
        # if isinstance(self.game_screen, Screen06Game):
        #     if self.game_screen.window_manager.is_additional_canvas_displayed(HelpCanvas):
        #         return "help_canvas"
        #     elif self.game_screen.window_manager.is_additional_canvas_displayed(InventoryCanvas):
        #         return "inventory_canvas"
        #     else:
        #         return "default"
        # else:
        #     print("Probleme:")
        #     print("Fichier: classes/utilitaires/key_handler.py")
        #     print("methode: get_current_state()")

        if self.game_screen.window_manager.is_additional_canvas_displayed(HelpCanvas):
            return "help_canvas"
        elif self.game_screen.window_manager.is_additional_canvas_displayed(InventoryCanvas):
            return "inventory_canvas"
        else:
            return "default"

    # ========================================================================

    def execute_method(self, key, is_key_down):
        current_state = self.get_current_state()
        if key in self.states[current_state]:
            method = self.states[current_state][key][is_key_down]
            if method is not None:
                method()

    # ========================================================================

    def handle_key_up(self, key):
        self.execute_method(key, 1)

    def handle_key_down(self, key):
        self.execute_method(key, 0)

    # ========================================================================
    # ========================================================================
    # Méthodes communes a tous les dictionnaires.

    def handle_F1_pressed(self):
        print("F1 pressed")

    def handle_F1_released(self):
        print("F1 released")
        self.game_screen.window_manager.hide_all_additional_canvases()
        self.game_screen.window_manager.set_focus(
            self.game_screen.canvas01_maps)

    def handle_Esc_pressed(self):
        print("Esc key pressed")

    def handle_Esc_released(self):
        print("Esc key released and quit program")

        pygame.quit()
        sys.exit()

    # ========================================================================
    # ========================================================================
    # Methodes pour le global_dictionary.

    def handle_s_pressed(self):

        if self.mode == "multiplayer":
            print("Mode multiplayer, 's' key pressed, global_dictionary")

        elif self.mode == "monoplayer":
            print("Mode monoplayer, 's' key pressed, global_dictionary")

        else:
            print("Mode inconnu, 's' key pressed, global_dictionary")

    # ------------------------------------------------------------------------

    def handle_F2_pressed(self):
        print("'F2' pressed, global_dictionary")

    # ------------------------------------------------------------------------

    def handle_F3_pressed(self):
        print("'F3' pressed, global_dictionary")

    # ------------------------------------------------------------------------

    def handle_F4_pressed(self):
        print("'F4' pressed, global_dictionary")

    # ------------------------------------------------------------------------

    def handle_s_released(self):

        # Définit° date et heure.
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if self.mode == "multiplayer":

            # Placer CE message dans la file_messages.
            self.file_messages.put(
                f"""
05: >
Fichier: key_handler.py.
{current_time}.
de IP: {self.ip_client}.
Contenu:
- msg de la file_messages
"""
            )

            try:
                Utilitaires02Reseau.send_message(
                    self.websocket_client,
                    f"""
04: >
Fichier: key_handler.py.
{current_time}
de IP: {self.ip_client}.
<"""
                )

                print("Mode multiplayer, 's' released, global_dictionary")

            except Exception as e:
                # logger.error(f"Failed to send WebSocket message: {e}")
                print(f"exception: {e}")

        elif self.mode == "monoplayer":
            print("Mode monoplayer, 's' released, global_dictionary")

        else:
            print("Mode inconnu, 's' released, global_dictionary")

    # ------------------------------------------------------------------------

    def handle_F2_released(self):
        print("'F2' released, global_dictionary")
        self.game_screen.window_manager.show_canvas(HelpCanvas)

    # ------------------------------------------------------------------------

    def handle_F3_released(self):
        print("'F3' released, global_dictionary")
        self.game_screen.window_manager.show_canvas(InventoryCanvas)

    # ------------------------------------------------------------------------

    def handle_F4_released(self):
        print("'F4' released, global_dictionary")

    # ========================================================================
    # ========================================================================
    # Méthodes pour le help_dictionary.

    def handle_F2_released_help(self):
        print("'F2' released, help_dictionary")

    # ------------------------------------------------------------------------

    def handle_F3_released_help(self):
        print("'F3' released, help_dictionary")

    # ------------------------------------------------------------------------

    def handle_F4_released_help(self):
        print("'F4' released, help_dictionary")

    # ========================================================================
    # ========================================================================
    # Méthodes pour le inventory_dictionary.

    def handle_F2_released_inventory(self):
        print("'F2' released, inventory_dictionary")

    # ------------------------------------------------------------------------

    def handle_F3_released_inventory(self):
        print("'F3' released, inventory_dictionary")

    # ------------------------------------------------------------------------

    def handle_F4_released_inventory(self):
        print("'F4' released, inventory_dictionary")
