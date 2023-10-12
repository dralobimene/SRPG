# Fichier: screen04_create_character.py

import tkinter as tk
import tkinter.messagebox
import secrets
import os
import re
import sys
import json
import ipaddress

from typing import Union

from classes.utilitaires.utilitaires_01 import Utilitaires01
from client import WebSocketClient


from logger_config import configure_logger
# méthodes du logger (debug(), info(), warning(), error(), critical())
logger = configure_logger(__name__, 'logs/screen04_create_character.log')


class Screen04CreateCharacter:
    Utilitaires01.log_entry_message(logger,
                                    "debug",
                                    "screen04_create_character.py",
                                    "class: Screen04CreateCharacter")

    def __init__(self, root):
        print("=============================")
        print("file: screen04_create_character.py")
        print("")

        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen04_create_character.py",
                                        "method: def __init__()")

        self.root = root

        # Configuration de la fenêtre
        self.root.title("screen04_create_character.py")

        # Défini le nom du fichier json qui contient les
        # settings
        self.settings_file = "settings.json"

        #
        self.window_width = None
        self.window_height = None

        # Récupèrera la valeur de la clé "mode" du fichier
        # settings.json
        self.mode = None

        # ---------------------------------------------------------------------

        # Vérifier si le fichier existe
        if os.path.exists(self.settings_file):
            logger.info(f"Le fichier {self.settings_file} existe.")
        else:
            logger.error(f"Le fichier {self.settings_file} n'existe pas.")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen04_create_character.py",
                                           "method: def __init__()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen04_create_character.py",
                                           "class: Screen04CreateCharacter")

            sys.exit()

        # ---------------------------------------------------------------------

        # Si le fichier est accessible en lecture,
        # Vérifier si le fichier est accessible en lecture.
        if os.access(self.settings_file, os.R_OK):
            logger.info(
                f"Le fichier {self.settings_file} est accessible en lecture.")

            # Définir si le mode de jeu est monoplayer ou multiplayer.
            self.mode = Utilitaires01.get_key_value_from_json(
                self.settings_file, "mode")

            # Définir les dimensions de la fenêtre grâce aux valeurs adéquates
            # du fichier settings.json.
            self.window_width = Utilitaires01.get_key_value_from_json(
                self.settings_file, "width_window")
            self.window_height = Utilitaires01.get_key_value_from_json(
                self.settings_file, "height_window")

        else:
            logger.error(
                f"Le fichier {self.settings_file} n'est pas accessible en lecture.")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen04_create_character.py",
                                           "method: def __init__()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen04_create_character.py",
                                           "class: Screen04CreateCharacter")

            sys.exit()

        # ---------------------------------------------------------------------

        # Appliquer les dimensions à la fenêtre.
        self.root.geometry(str(self.window_width) +
                           "x" + str(self.window_height))

        # Recupére le contenu du fichier game/settings.json.
        self.content = None

        # Initialisation des variables
        self.character_name = tk.StringVar()
        self.attack = tk.StringVar()
        self.defense = tk.StringVar()
        self.life = tk.StringVar()

        # =====================================================================
        # La GUI pr créer son personnage.

        # Création du frame
        self.frame = tk.Frame(root)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Ajout du bouton Quit
        self.btn_quit = tk.Button(
            self.frame, text="Quit.", command=root.destroy, width=20, height=2)
        self.btn_quit.grid(row=2, column=0, sticky="w", pady=10)

        # Ajout des labels et des entrées de texte
        self.label_create_character = tk.Label(
            self.frame, text='Create your character')
        self.label_create_character.grid(row=2, column=1, padx=15, sticky='w')

        self.label_enter_name = tk.Label(
            self.frame, text='Please enter the name of your character')
        self.label_enter_name.grid(row=3, column=1, padx=15, sticky='w')

        self.entry_name = tk.Entry(
            self.frame, textvariable=self.character_name)
        self.entry_name.grid(row=4, column=1, padx=15, sticky='w')
        self.entry_name.bind('<KeyRelease>', self.check_and_update_button)

        self.label_guideline = tk.Label(
            self.frame, text='Only letters and or numbers, min 5 and max 15')
        self.label_guideline.grid(row=5, column=1, padx=15, sticky='w')

        self.roll_dice_button = tk.Button(
            self.frame, text="Please roll dice to define your skills", command=self.roll_dice)
        self.roll_dice_button.grid(row=6, column=1, padx=15, sticky='w')

        self.label_life = tk.Label(
            self.frame, text='The life of your character will be: ')
        self.label_life.grid(row=7, column=1, padx=15, sticky='w')

        self.label_life_value = tk.Label(
            self.frame, textvariable=self.life)
        self.label_life_value.grid(row=7, column=2, padx=15, sticky='w')

        self.label_attack = tk.Label(
            self.frame, text='The attack of your character will be: ')
        self.label_attack.grid(row=8, column=1, padx=15, sticky='w')

        self.label_attack_value = tk.Label(
            self.frame, textvariable=self.attack)
        self.label_attack_value.grid(row=8, column=2, padx=15, sticky='w')

        self.label_defense = tk.Label(
            self.frame, text='The defense of your character will be: ')
        self.label_defense.grid(row=9, column=1, padx=15, sticky='w')

        self.label_defense_value = tk.Label(
            self.frame, textvariable=self.defense)
        self.label_defense_value.grid(row=9, column=2, padx=15, sticky='w')

        # Boutons cachés
        self.btn_start_monoplayer_game = tk.Button(
            self.frame, text="Start monoplayer game.", command=self.monoplayer_game, width=20, height=2)
        self.btn_start_monoplayer_game.grid(
            row=10, column=1, padx=15, sticky="w")
        self.btn_start_monoplayer_game.grid_remove()

        self.btn_start_multiplayer_game = tk.Button(
            self.frame, text="Start multiplayer game.", command=self.multiplayer_game, width=20, height=2)
        self.btn_start_multiplayer_game.grid(
            row=10, column=1, padx=15, sticky="w")
        self.btn_start_multiplayer_game.grid_remove()

        # ========================================================================
        # la GUI pr parametrer le network.

        # la variable pr renseigner l'IP du serveur
        # self.ip_address = tk.StringVar()

        # ========================================================================
        # Appels de méthodes.

        # Verifie si a chaque release de touche le pattern
        # est respecté.
        self.entry_name.bind('<KeyRelease>', self.is_character_valid)

        self.read_temp_settings_file()

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen04_create_character.py",
                                       "method: def __init__()")

    # ========================================================================

    def is_character_valid(self, event=None):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen04_create_character.py",
                                        "method: def is_character_valid()")

        valid_name = re.match(
            r'^[a-zA-Z0-9]{5,15}$', self.character_name.get())

        if valid_name and self.attack.get() and self.defense.get() and self.life.get():
            self.update_ui(True)
            return True

        self.update_ui(False)

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen04_create_character.py",
                                       "method: def is_character_valid()")

        return False

    # ========================================================================

    def roll_dice(self):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen04_create_character.py",
                                        "method: def roll_dice()")

        self.life.set(secrets.randbelow(100) + 1)
        self.attack.set(secrets.randbelow(100) + 1)
        self.defense.set(secrets.randbelow(100) + 1)

        self.is_character_valid()

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen04_create_character.py",
                                       "method: def roll_dice()")

    # ========================================================================

    def update_ui(self, is_valid):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen04_create_character.py",
                                        "method: def update_ui()")

        if is_valid:
            if os.path.exists(self.settings_file):
                # Vérifier si le fichier est accessible en lecture
                try:
                    with open(self.settings_file, 'r') as f:
                        pass
                except IOError:
                    logger.error(
                        f"Le fichier {self.settings_file} n'est pas accessible en lecture.")

                    Utilitaires01.log_exit_message(logger,
                                                   "debug",
                                                   "screen04_create_character.py",
                                                   "method: def update_ui()")

                    Utilitaires01.log_exit_message(logger,
                                                   "debug",
                                                   "screen04_create_character.py",
                                                   "class: Screen04CreateCharacter")

                    sys.exit()

                else:
                    # Fichier accessible en lecture, aller de l'avant pour lire la clé
                    with open(self.settings_file, 'r') as f:
                        data = json.load(f)
                        mode_value = data.get('mode', 'Clé non trouvée')
                        logger.info(
                            f"La valeur de la clé 'mode' est : {mode_value}")
            else:
                logger.error(f"Le fichier {self.settings_file} n'existe pas.")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen04_create_character.py",
                                               "method: def update_ui()")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen04_create_character.py",
                                               "class: Screen04CreateCharacter")

                exit()

            if mode_value == "monoplayer":
                self.btn_start_monoplayer_game.grid()
            elif mode_value == "multiplayer":
                self.btn_start_multiplayer_game.grid()
            else:
                logger.error("Problem 01:")
                logger.error("Fichier: game/screen04_create_character.py")
                logger.error("Methode: update_ui()")

                os.remove(self.settings_file)
                sys.exit()
        else:
            self.btn_start_monoplayer_game.grid_remove()
            self.btn_start_multiplayer_game.grid_remove()

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen04_create_character.py",
                                       "method: def update_ui()")

    # ========================================================================

    # Méthode pour vérifier et mettre à jour le bouton
    def check_and_update_button(self, event=None):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen04_create_character",
                                        "method: def check_and_update_button()")

        valid_name = re.match(
            r'^[a-zA-Z0-9]{5,15}$', self.character_name.get())

        if valid_name and self.attack.get() and self.defense.get() and self.life.get():
            return True

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen04_create_character.py",
                                       "method: def check_and_update_button()")

        return False

    # ========================================================================

    def read_temp_settings_file(self):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen04_create_character.py",
                                        "method: def read_temp_settings_file()")

        if os.path.exists(self.settings_file):
            try:
                self.content = Utilitaires01.read_file(
                    self.settings_file,
                    "screen04_create_character.py",
                    "read_temp_settings_file",
                    30
                )

            except SystemExit:
                pass

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen04_create_character.py",
                                       "method: def read_temp_settings_file()")

    # ========================================================================

    def monoplayer_game(self):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen04_create_character.py",
                                        "method: def monoplayer_game()")

        logger.info("Player starts the monoplayer game mode.")

        self.open_new_window_to_generate_maps()

    # ========================================================================

    def multiplayer_game(self):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen04_create_character.py",
                                        "method: def multiplayer_game()")

        logger.info("Player starts the multiplayer game mode.")

        # Création du bouton Connect
        self.connect_button = tk.Button(
            self.frame, text="Connect", command=self.connect_to_server)
        self.connect_button.grid(row=13, column=1, padx=15, sticky='w')

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen04_create_character.py",
                                       "method: def multiplayer_game()")

    # ========================================================================

    def open_new_window_to_generate_maps(self):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen04_create_character.py",
                                        "method: def open_new_window_to_generate_maps()")

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen04_create_character.py",
                                       "method: def open_new_window_to_generate_maps()")

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen04_create_character.py",
                                       "class: Screen04CreateCharacter")

        import screen05_generate_maps
        self.root.destroy()
        new_root = tk.Tk()
        screen05_generate_maps.Screen05GenerateMaps(new_root)
        new_root.mainloop()

# ========================================================================

    def connect_to_server(self):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen04_create_character.py",
                                        "method: def connect_to_server()")

        # ---------------------------------------------------------------------

        # Condit°: en fonct° du mode du moteur de jeu:
        # monoplayer ou multiplayer, instantie le fichier client.py.
        if self.mode == "multiplayer":
            logger.info("Le moteur de jeu est en mode multiplayer.")

            # Instantiation du client avec l'adresse du serveur.
            self.websocket_client = WebSocketClient('192.168.1.210')

            # Connexion au serveur.
            self.websocket_client.connect()

            # Récupérer l'adresse IP locale de la machine cliente.
            client_ip = self.websocket_client.get_local_ip_address()

            result1 = self.websocket_client.receive()

            # Reçu sur la machine cliente.
            # La variable result1 est définie sur le serveur.
            print("Depuis le fichier: screen04_create_character.py: ")
            print("qui transmet la variable définie sur le serveur.")
            print(f"'{result1}'")

        elif self.mode == "monoplayer":
            logger.error("Le moteur de jeu est en mode monoplayer.")
            logger.error("Alors que l'utilisateur a lancé un multiplayer.")
        else:
            logger.error("Une erreur est survenue à la lecture du")
            logger.error(f"fichier {self.settings_file} sur la clé")
            logger.error("'mode'.")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen04_create_character.py",
                                           "method: def connect_to_server()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen04_create_character.py",
                                           "class: Screen04CreateCharacter")

            sys.exit()

        # ---------------------------------------------------------------------

        # Ecrire la clé qui contient l'adresse IP du client
        # ds le fichier "settings.json".
        # Verifier que le fichier settings.json existe.
        logger.info(f"Vérificat° du fichier {self.settings_file}")
        file_network = self.settings_file
        file_writable = True
        if file_network:
            logger.info(f"Le fichier {file_network} existe")
            file_writable = os.access(file_network, os.W_OK)
        else:
            logger.info(f"Le fichier {file_network} n'existe pas")
            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen04_create_character.py",
                                           "method: def connect_to_server()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen04_create_character.py",
                                           "class: Screen04CreateCharacter")

            sys.exit()

        # Si le fichier settings.json existe ET s'il est accessible
        # en ecriture alors:
        # Ajouter en fin de fichier la valeur de client_ip.
        if file_network and file_writable:
            actual_ip = client_ip
            ip_type = self.check_ip_type(actual_ip)

            logger.info(f"Le fichier {file_network} est inscriptible")
            logger.info(f"Définition Type de l'IP (IP4 ou IP6): : {ip_type}")
            logger.info(f"Ecriture de l'IP: {str(actual_ip)}")

            # Vérifier si le fichier existe
            if os.path.exists(file_network):
                # Charger les données existantes
                with open(file_network, 'r') as f:
                    data = json.load(f)

                # Ajouter la nouvelle paire clé => valeur
                new_key = "IP_user_adress"
                new_value = actual_ip
                data[new_key] = new_value

                # Réecrire le fichier avec les anciennes et nvelles
                # clés.
                with open(file_network, "w") as file:
                    json.dump(data, file, indent=4)

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen04_create_character.py",
                                               "method: def connect_to_server()")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen04_create_character.py",
                                               "class: Screen04CreateCharacter")

                # Aller au prochain ecran.
                self.root.destroy()
                import screen05_generate_maps
                new_root = tk.Tk()
                screen05_generate_maps.Screen05GenerateMaps(new_root)
                new_root.mainloop()

            else:
                logger.error(f"Le fichier {file_network} n'existe pas.")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen04_create_character.py",
                                               "method: def connect_to_server()")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen04_create_character.py",
                                               "class: Screen04CreateCharacter")

                sys.exit()

        else:
            logger.error(
                f"Le fichier {file_network} n'est pas inscriptible")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen04_create_character.py",
                                           "method: def connect_to_server()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen04_create_character.py",
                                           "class: Screen04CreateCharacter")

            sys.exit()

        # ---------------------------------------------------------------------

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen04_create_character.py",
                                       "method: def connect_to_server()")

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen04_create_character.py",
                                       "class: Screen04CreateCharacter")

    # ========================================================================

    def check_ip_type(self, ip_str: str) -> Union[str, None]:
        try:
            ip = ipaddress.ip_address(ip_str)
            if isinstance(ip, ipaddress.IPv4Address):
                return 'IPv4'
            elif isinstance(ip, ipaddress.IPv6Address):
                return 'IPv6'
        except ValueError:
            return None


if __name__ == "__main__":
    root = tk.Tk()
    app = Screen04CreateCharacter(root)
    root.mainloop()
    Utilitaires01.log_exit_message(logger,
                                   "debug",
                                   "screen04_create_character.py",
                                   "class: Screen04CreateCharacter")
