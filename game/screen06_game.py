# Fichier screen06_game.py

import pygame
import pygame_gui
import sys
import os

from client import WebSocketClient

from classes.utilitaires.utilitaires_01 import Utilitaires01

from logger_config import configure_logger
# méthodes du logger (debug(), info(), warning(), error(), critical())
logger = configure_logger(__name__, 'logs/screen06_game.log')

SOME_EVENT_TYPE = pygame.USEREVENT + 1


class Screen06Game:
    Utilitaires01.log_entry_message(logger,
                                    "debug",
                                    "screen06_game.py",
                                    "class: Screen06Game")

    print("=============================================================")
    print("File: screen06_game.py")
    print("=============================================================")
    print("")

    def __init__(self):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen06_game.py",
                                        "method: def __init__()")

        # Initialise tous les modules importés de Pygame.
        pygame.init()

        # Permettra l'instantiat° du client.
        self.websocket_client = None

        # Permettra ...
        result1 = None

        # Définit le titre de la fenêtre.
        pygame.display.set_caption('game/screen06_game.py')

        # Défini le nom du fichier json qui contient les
        # settings
        self.settings_file = "settings.json"

        # Définira les dimens° de la fenetre.
        self.window_width = None
        self.window_height = None

        # Définira les dimensions des tiles.
        self.tile_size = None

        # Récupèrera la valeur de la clé "mode" du fichier
        # settings.json
        self.mode = None

        # ---------------------------------------------------------------------

        # Vérifie si le fichier "settings.json" existe.
        if os.path.exists(self.settings_file):
            logger.info(f"Le fichier {self.settings_file} existe.")
        else:
            logger.error(f"Le fichier {self.settings_file} n'existe pas.")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen06_game.py",
                                           "method: def __init__()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen06_game.py",
                                           "class: Screen06Game")

            sys.exit()

        # ---------------------------------------------------------------------

        # Si le fichier est accessible en lecture,
        # Vérifier si le fichier est accessible en lecture.
        if os.access(self.settings_file, os.R_OK):
            logger.info(
                f"Le fichier {self.settings_file} est accessible en lecture.")

            # Définir si le moteur de jeu est en mode
            # monoplayer ou multiplayer
            self.mode = Utilitaires01.get_key_value_from_json(
                self.settings_file, "mode")

            # Définir les dimensions de la fenêtre grâce aux valeurs adéquates
            # du fichier settings.json.
            self.window_width = Utilitaires01.get_key_value_from_json(
                self.settings_file, "width_window")
            self.window_height = Utilitaires01.get_key_value_from_json(
                self.settings_file, "height_window")

            # Définir les dimens° des tiles.
            self.tile_size = Utilitaires01.get_key_value_from_json(
                self.settings_file, "tile_size")
        else:
            logger.error(
                f"Le fichier {self.settings_file} n'est pas accessible en lecture.")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen06_game.py",
                                           "method: def __init__()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen06_game.py",
                                           "class: Screen06Game")

            sys.exit()

        # ---------------------------------------------------------------------

        # Crée une fenêtre de 1200x800 pixels.
        self.screen = pygame.display.set_mode((self.window_width,
                                               self.window_height))

        # ---------------------------------------------------------------------

        # Condit°: en fonct° du mode du moteur de jeu:
        # monoplayer ou multiplayer, instantie le fichier client.py.
        if self.mode == "multiplayer":
            logger.info("Le moteur de jeu est en mode multiplayer.")

            # Instantiation du client avec l'adresse du serveur.
            self.websocket_client = WebSocketClient('192.168.1.210')

            # Connexion au serveur.
            self.websocket_client.connect()

            result1 = self.websocket_client.receive()

            # Reçu sur la machine cliente.
            # La variable result1 est définie sur le serveur.
            print("Depuis le fichier: screen06_game.py: ")
            print("qui transmet la variable définie sur le serveur.")
            print(f"'{result1}'")

        elif self.mode == "monoplayer":
            logger.info("Le moteur de jeu est en mode monoplayer.")
        else:
            logger.error("Une erreur est survenue à la lecture du")
            logger.error(f"fichier {self.settings_file} sur la clé")
            logger.error("'mode'.")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen06_game.py",
                                           "method: def __init__()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen06_game.py",
                                           "class: Screen06Game")

            sys.exit()

        # ---------------------------------------------------------------------

        # La fonction pygame.time.get_ticks() renvoie le nombre de
        # millisecondes écoulées depuis l'initialisation de Pygame.
        # Cette valeur est souvent utilisée pour contrôler le comportement du
        # jeu en fonction du temps écoulé.
        self.last_played = pygame.time.get_ticks()

        # Initialise le gestionnaire d'interface utilisateur de pygame_gui,
        # qui permet de gérer les éléments de l'interface utilisateur.
        self.manager = pygame_gui.UIManager((1200,
                                             800))

        # Crée un objet d'horloge qui peut être utilisé pour
        # contrôler le taux de rafraîchissement du jeu
        self.clock = pygame.time.Clock()

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen06_game.py",
                                       "method: def __init__()")

    # ========================================================================

    def handle_events(self):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen06_game.py",
                                        "method: def handle_events()")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen06_game.py",
                                               "method: def handle_events()")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen06_game.py",
                                               "class: Screen06Game")

                pygame.quit()
                exit()

            if event.type == SOME_EVENT_TYPE:
                self.q.put("some_command")

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen06_game.py",
                                       "method: def handle_events()")

    # ========================================================================

    def update(self, time_delta):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen06_game.py",
                                        "method: def update()")

        #
        self.manager.update(time_delta)

        #
        current_time = pygame.time.get_ticks()

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen06_game.py",
                                       "method: def update()")

    # ========================================================================

    def render(self):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen06_game.py",
                                        "method: def render()")

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen06_game.py",
                                       "method: def render()")

    # ========================================================================

    def run_game(self):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen06_game.py",
                                        "method: def run_game()")

        # Main loop.
        running = True
        while running:
            time_delta = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.update(time_delta)
            self.render()
            pygame.display.update()

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen06_game.py",
                                       "method: def run_game()")


if __name__ == '__main__':
    screen06_game = Screen06Game()
    screen06_game.run_game()
    Utilitaires01.log_exit_message(logger,
                                   "debug",
                                   "screen06_game.py",
                                   "class: Screen06Game")
