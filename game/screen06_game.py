# Fichier screen06_game.py

import pygame
import pygame_gui
import sys
import os

from queue import Queue
from threading import Thread

from client import WebSocketClient
from classes.utilitaires.utilitaires_01 import Utilitaires01
from classes.utilitaires.utilitaires_02_reseau import Utilitaires02Reseau

from classes.utilitaires.mouse_handler import MouseHandler
from classes.utilitaires.key_handler import KeyHandler

from classes.canvases.WindowManager import WindowManager
from classes.canvases.canvas01_cartes import Maps01Canvas
from classes.canvases.canvas02_droite import Right01Canvas
from classes.canvases.canvas03_informations import InformationsCanvas
from classes.canvases.canvas_inventaire import InventoryCanvas
from classes.canvases.canvas_magie import MagicalCanvas
from classes.canvases.canvas_aide import HelpCanvas
from classes.windowsChat.ChatBox import ChatBox

from logger_config import configure_logger
# méthodes du logger (debug(), info(), warning(), error(), critical())
logger = configure_logger(__name__, 'logs/screen06_game.log')


class Screen06Game:

    # constantes:
    # SOME_EVENT_TYPE = pygame.USEREVENT + 1
    # ACCEDER à la constante: Screen06Game.SOME_EVENT_TYPE
    # Utilisat°: constante partagée entre toutes les instances de la classe.

    Utilitaires01.log_entry_message(logger,
                                    "debug",
                                    "screen06_game.py",
                                    "class: Screen06Game")

    # Constantes.

    # Colors.
    TRANSPARENT = pygame.Color(0, 0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    BLACK = pygame.Color(0, 0, 0)
    GREEN = pygame.Color(0, 255, 0)
    BLUE = pygame.Color(0, 0, 255)
    YELLOW = pygame.Color(255, 255, 0)
    RED = pygame.Color(255, 0, 0)
    ROUGE_FONCE_01 = pygame.Color(121, 77, 77)
    GREY = pygame.Color(128, 128, 128)
    GREY_LIGHT_01 = pygame.Color(224, 224, 224, 0)
    GREY_LIGHT_02 = pygame.Color(220, 220, 220, 0)

    # Dimens° des canvas.
    CANVASES_PRINCIPAUX_WIDTH = 800
    CANVASES_PRINCIPAUX_HEIGHT = 600

    print("=============================================================")
    print("File: screen06_game.py")
    print("=============================================================")
    print("")

    def __init__(self):

        # self.SOME_EVENT_TYPE = pygame.USEREVENT + 1
        # ACCEDER à la variable: self.SOME_EVENT_TYPE = pygame.USEREVENT + 1
        # Utilisat°: chaque instance de la classe doit avoir sa
        #       propre valeur pour cette variable.

        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen06_game.py",
                                        "method: def __init__()")

        # Initialise tous les modules importés de Pygame.
        pygame.init()

        # Définira les dimens° de la fenetre.
        # Définies ds le fichier settings.json.
        self.window_width = None
        self.window_height = None

        # Défini le nom du fichier json qui contient les
        # settings
        self.settings_file = "settings.json"

        # Définira les dimensions des tiles.
        # Définies ds le fichier "settings.json".
        self.tile_size = None

        # Récupèrera la valeur de la clé "mode" du fichier
        # settings.json. Le mode est "monoplayer" ou "multiplayer".
        self.mode = None

        # --------------------------------------------------------------------

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

        # --------------------------------------------------------------------

        # Vérifie si le fichier settings.json est accessible en lecture,
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

        # --------------------------------------------------------------------

        # Crée une fenêtre de 1200x800 pixels.
        self.screen = pygame.display.set_mode((self.window_width,
                                               self.window_height))

        # Initialise le gestionnaire d'interface utilisateur de pygame_gui,
        # qui permet de gérer les éléments de l'interface utilisateur.
        self.manager = pygame_gui.UIManager((1200, 800))

        # --------------------------------------------------------------------
        # Définit° des variables reseau.

        # Permettra l'instantiat° du client.
        self.websocket_client = None

        # Définira un élément de type Queue pour les
        # messages.
        self.file_messages = None

        # Recevra la valeur envoyée par le serveur.
        # self.result1 = None

        # Récuperera l'ip du fichier client.py.
        self.ip_client = None

        # Recuperera la valeur de la cle "client_name".
        self.client_name = None

        # --------------------------------------------------------------------

        # Défini le titre de la fenêtre.
        pygame.display.set_caption('game/screen06_game.py')

        # ---------------------------------------------------------------------

        # definit le canvas chargé d'afficher la carte
        self.canvas01_maps = Maps01Canvas(self.CANVASES_PRINCIPAUX_WIDTH,
                                          self.CANVASES_PRINCIPAUX_HEIGHT)

        # Définit le canvas de droite.
        # Ajuste la hauteur de canvas02_droite pour qu'elle soit
        # égale à self.window_height.
        self.canvas02_droite = Right01Canvas(
            (self.window_width - self.CANVASES_PRINCIPAUX_WIDTH), self.window_height)

        # Créer une instance de InventoryCanvas
        # largeur - hauteur
        self.canvas_inventaire = InventoryCanvas(self.CANVASES_PRINCIPAUX_WIDTH,
                                                 self.CANVASES_PRINCIPAUX_HEIGHT)

        # Créer une instance de MagicalCanvas
        # largeur - hauteur
        self.canvas_magie = MagicalCanvas(
            (self.window_width - self.CANVASES_PRINCIPAUX_WIDTH), self.window_height)

        # Créer une instance de HelpCanvas
        # largeur - hauteur
        self.canvas_aide = HelpCanvas(900, 550)

        # Définit le canvas chargé d'afficher les informat°.
        # largeur - hauteur
        self.canvas03_informations = InformationsCanvas(self.CANVASES_PRINCIPAUX_WIDTH,
                                                        (self.window_height - self.CANVASES_PRINCIPAUX_HEIGHT))

        #
        self.window_manager = WindowManager()

        if self.mode == "multiplayer":
            #     # Instantiation de la chatbox.
            #     # largeur - hauteur.
            self.canvas = pygame.Surface((400, 400))
            self.canvas.fill((128, 128, 128))
            self.canvas_position = (800, 0)
            self.chat_box = ChatBox(self.manager, self.canvas_position)

        # Ajout des canvases au WindowManager.
        self.window_manager.add_canvas(self.canvas01_maps)
        self.window_manager.add_canvas(self.canvas02_droite)
        self.window_manager.add_canvas(self.canvas03_informations)
        self.window_manager.add_canvas(self.canvas_inventaire)
        # self.window_manager.add_canvas(self.canvas_magie)
        self.window_manager.add_canvas(self.canvas_aide)

        # Mettre le focus sur le canvas souhaité
        self.window_manager.set_focus(self.canvas01_maps)

        # ---------------------------------------------------------------------

        # Condit°: en fonct° du mode du moteur de jeu:
        # monoplayer ou multiplayer, instantie le fichier client.py.
        if self.mode == "multiplayer":
            logger.info("Le moteur de jeu est en mode multiplayer.")

            # Instantiation du client avec l'adresse du serveur.
            self.websocket_client = WebSocketClient(self, '192.168.1.210')

            # Connexion au serveur.
            self.websocket_client.connect()

            # Défini la variable en tant qu'objet de type Queue.
            self.file_messages = Queue()

            # Reçoit la valeur envoyée par le serveur.
            # self.result1 = self.websocket_client.receive()

            # Récupere l'ip du fichier client.py.
            self.ip_client = self.websocket_client.ip_client

            # Définir la variable self.client_name.
            self.client_name = Utilitaires01.get_key_value_from_json(
                self.settings_file, "client_name")

            # Reçu sur la machine cliente.
            # La variable result1 est la valeur du message
            # défini sur le serveur.
            # print("> screen06_game.py: ")
            # print("Affiche la variable définie sur le serveur.")
            # print(f">>>>>> {self.result1}")

            #
            Thread(target=self.websocket_client.listen).start()

            # Envoyer un message au démarrage de l'appli
            Utilitaires02Reseau.send_message(
                self.websocket_client,
                f"""
03: >
Connex°: {self.client_name}.
<
"""
            )

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

        # Initialise le manager clavier.
        # initialise une instance de classes/KeyHandler.py
        # pour la gest° d'evenements clavier qui ne st pas rattachés
        # à l'instance de classes/Player.py.
        self.key_handler = KeyHandler(
            self.websocket_client, self.ip_client, self.file_messages, self)

        # La fonction pygame.time.get_ticks() renvoie le nombre de
        # millisecondes écoulées depuis l'initialisation de Pygame.
        # Cette valeur est souvent utilisée pour contrôler le comportement du
        # jeu en fonction du temps écoulé.
        self.last_played = pygame.time.get_ticks()

        # Initialise le manager de la souris.
        # initialise une instance de classes/MouseHandler.py
        # pour la gest° de la souris
        self.mouse_handler = MouseHandler(self.screen, self.window_manager)

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

        # mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                logger.info("event: pygame.QUIT")
                logger.info("Close window, and program.")
                if self.websocket_client:
                    logger.info("mulitplayer mode, closing websocket.")
                    self.websocket_client.close()

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

            # Indique le canvas qui est au-dessous du pointeur de la souris.
            # elif event.type == pygame.MOUSEMOTION:
            #     canvas_maps_rect = self.canvas01_maps.get_rect(topleft=(0, 0))
            #     canvas_droite_rect = self.canvas02_droite.get_rect(
            #         topleft=(self.CANVASES_PRINCIPAUX_WIDTH, 0))
            #     canvas_informations_rect = self.canvas03_informations.get_rect(
            #         topleft=(0, self.CANVASES_PRINCIPAUX_HEIGHT))
            #     canvas_aide_rect = self.canvas_aide.get_rect(
            #         topleft=(100, 100))
            #
            #     print(f"canvas_maps_rect: {canvas_maps_rect}")
            #     print(f"canvas_droite_rect: {canvas_droite_rect}")
            #     print(f"canvas_informations_rect: {canvas_informations_rect}")
            #     print(f"canvas_aide_rect: {canvas_aide_rect}")
            #
            #     self.mouse_handler.detect_and_display(
            #         mouse_x,
            #         mouse_y,
            #         canvas_maps_rect,
            #         canvas_droite_rect,
            #         canvas_informations_rect,
            #         canvas_aide_rect,)

            if event.type == pygame.KEYDOWN:
                self.key_handler.handle_key_down(event.key)
            elif event.type == pygame.KEYUP:
                self.key_handler.handle_key_up(event.key)

            # Active le manager de la ChatBox.
            if self.mode == "multiplayer":
                if not self.chat_box.process_events(event, self.manager, self.websocket_client):
                    self.manager.process_events(event)

            #
            self.window_manager.process_events(event)

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen06_game.py",
                                       "method: def handle_events()")

    # ========================================================================

    def update(self, time_delta):

        #
        self.manager.update(time_delta)

        #
        current_time = pygame.time.get_ticks()

        # [REPERE 1 - 1]
        # MAJ de la ChatBox.
        # MAJ le widget: self.text_box de la classe
        # ChatBox (fichier: classes/utilitaires/windowsChat.py).
        # [REPERE 1 - 2] dans le fichier classes/windowsChat/ChatBox.py.
        if self.mode == "multiplayer":
            if not self.file_messages.empty():
                new_message = self.file_messages.get()
                self.chat_box.update_messages(new_message)

    # ========================================================================

    def render(self):
        """
        Pydoc de la methode render()
        """

        # afficher l'ecran
        self.screen.fill(self.GREY_LIGHT_01)

        # Affiche la ChatBox.
        if self.mode == "multiplayer":
            self.screen.blit(self.canvas, self.canvas_position)
            # self.manager.draw_ui(self.canvas)
            self.manager.draw_ui(self.screen)

        # Dessine tous les canvas.
        self.window_manager.render_all(self.screen)

    # ========================================================================

    def run_game(self):

        # Main loop.
        running = True
        while running:
            time_delta = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.update(time_delta)
            self.render()

            # On peut aussi envoyer un message ici.
            # avec une condit° qui est vérifiée à chaque tour de boucle.
            # Ou on peut le faire depuis les méthodes update() & render().
            # if SOME_CONDITION:
            #     self.send_message(
            #           self.websocket_client,
            #           "Bonjour, je suis la machine cliente1.")

            pygame.display.update()


if __name__ == '__main__':
    screen06_game = Screen06Game()
    screen06_game.run_game()
    Utilitaires01.log_exit_message(logger,
                                   "debug",
                                   "screen06_game.py",
                                   "class: Screen06Game")
