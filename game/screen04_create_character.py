# Fichier: screen04_create_character.py

import tkinter as tk
import tkinter.messagebox
import secrets
import os
import re
import sys
import time
import json

from classes.utilitaires.utilitaires_01 import Utilitaires01

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
        self.start_monoplayer_game = tk.Button(
            self.frame, text="Start monoplayer game.", command=self.monoplayer_game, width=20, height=2)
        self.start_monoplayer_game.grid(row=10, column=1, padx=15, sticky="w")
        self.start_monoplayer_game.grid_remove()

        self.set_network_settings = tk.Button(
            self.frame, text="Set network settings.", command=self.set_network_settings, width=20, height=2)
        self.set_network_settings.grid(row=10, column=1, padx=15, sticky="w")
        self.set_network_settings.grid_remove()

        # ========================================================================
        # la GUI pr parametrer le network.

        # la variable pr renseigner l'IP du serveur
        self.ip_address = tk.StringVar()

        # Les variables pr créer ensuite les widgets.
        self.label_ip_address = None
        self.entry_ip_address = None
        self.connect_button = None

        # ========================================================================
        # Appels de méthodes.

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
                    logger.info(
                        f"Le fichier {self.settings_file} n'est pas accessible en lecture.")
                    sys.exit()
                else:
                    # Fichier accessible en lecture, aller de l'avant pour lire la clé
                    with open(self.settings_file, 'r') as f:
                        data = json.load(f)
                        mode_value = data.get('mode', 'Clé non trouvée')
                        logger.info(
                            f"La valeur de la clé 'mode' est : {mode_value}")
            else:
                logger.info(f"Le fichier {self.settings_file} n'existe pas.")

            if mode_value == "monoplayer":
                self.start_monoplayer_game.grid()
            elif mode_value == "multiplayer":
                self.set_network_settings.grid()
            else:
                logger.error("Problem 01:")
                logger.error("Fichier: game/screen04_create_character.py")
                logger.error("Methode: update_ui()")

                os.remove(self.settings_file)
                sys.exit()
        else:
            self.start_monoplayer_game.grid_remove()
            self.set_network_settings.grid_remove()

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

    def set_network_settings(self):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen04_create_character.py",
                                        "method: def set_network_settings()")

        logger.info("Player wants to set network settings.")
        logger.info("We need to set GUI and settings.")

        # Création du Label pour l'adresse IP
        self.label_ip_address = tk.Label(
            self.frame, text="Please enter Server IP address:")
        self.label_ip_address.grid(
            row=11, column=1, padx=15, pady=15, sticky='w')

        # Création du champ de saisie pour l'adresse IP
        self.entry_ip_address = tk.Entry(
            self.frame, textvariable=self.ip_address)
        self.entry_ip_address.grid(row=12, column=1, padx=15, sticky='w')

        # Création du bouton Connect
        self.connect_button = tk.Button(
            self.frame, text="Connect", command=self.connect_to_server)
        self.connect_button.grid(row=13, column=1, padx=15, sticky='w')

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen04_create_character.py",
                                       "method: def set_network_settings()")

    # ========================================================================

    def open_new_window_to_generate_maps(self):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen04_create_character.py",
                                        "method: def open_new_window_to_generate_maps()")

        import screen05_generate_maps
        self.root.destroy()
        new_root = tk.Tk()
        screen05_generate_maps.Screen05GenerateMaps(new_root)
        new_root.mainloop()

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen04_create_character.py",
                                       "method: def open_new_window_to_generate_maps()")

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen04_create_character.py",
                                       "class: Screen04CreateCharacter")

    # ========================================================================

    def connect_to_server(self):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen04_create_character.py",
                                        "method: def connect_to_server()")

        # Validation de l'adresse IP
        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"

        if not re.match(ip_pattern, self.ip_address.get()):
            tkinter.messagebox.showerror("Erreur", "Adresse IP invalide")
            return

        #
        self.actual_connect()

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen04_create_character.py",
                                       "method: def connect_to_server()")

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen04_create_character.py",
                                       "class: Screen04CreateCharacter")

    # ========================================================================

    def actual_connect(self):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen04_create_character.py",
                                        "method: def actual_connect()")

        # Ici, vous ajoutez votre code pour établir la connexion.
        # Pour l'instant, utilisons un sleep pour simuler un délai.
        # Simule le temps pris pour la connexion
        time.sleep(2)

        # Ici, ajoutez le code pour vérifier si le serveur répond.
        # Mettez ceci à False si le serveur ne répond pas
        server_responds = True

        if server_responds:
            logger.info("Connection to server is running...")

            tkinter.messagebox.showinfo("Succès", "Connexion réussie")

            # Verifier que le fichier settings.json existe.
            logger.info(f"Vérificat° du fichier {self.settings_file}")
            file_network = self.settings_file
            file_writable = False
            if file_network:
                logger.info(f"Le fichier {file_network} existe")
                file_writable = os.access(file_network, os.W_OK)
            else:
                logger.info(f"Le fichier {file_network} n'existe pas")
                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen04_create_character.py",
                                               "method: def actual_connect()")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen04_create_character.py",
                                               "class: Screen04CreateCharacter")

                sys.exit()

            # Si le fichier settings.json existe ET s'il est accessible
            # en ecriture alors:
            # Ajouter en fin de fichier la valeur de self.ip_address.
            if file_network and file_writable:
                actual_ip = self.ip_address.get()
                logger.info(f"Le fichier {file_network} est inscriptible")
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
                else:
                    print(f"Le fichier {file_network} n'existe pas.")
            else:
                logger.info(
                    f"Le fichier {file_network} n'est pas inscriptible")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen04_create_character.py",
                                               "method: def actual_connect()")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen04_create_character.py",
                                               "class: Screen04CreateCharacter")

                sys.exit()

            self.root.destroy()
            import screen05_generate_maps
            new_root = tk.Tk()
            screen05_generate_maps.Screen05GenerateMaps(new_root)
            new_root.mainloop()

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen04_create_character.py",
                                           "method: def actual_connect")

        else:
            logger.info("Connection failed...")

            tkinter.messagebox.showinfo("Échec", "Connexion échouée")
            self.root.destroy()
            import screen01_choose_mode
            new_root = tk.Tk()
            screen01_choose_mode.Screen01ChooseMode(new_root)
            new_root.mainloop()

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen04_create_character.py",
                                           "method: def actual_connect()")


if __name__ == "__main__":
    root = tk.Tk()
    app = Screen04CreateCharacter(root)
    root.mainloop()
    Utilitaires01.log_exit_message(logger,
                                   "debug",
                                   "screen04_create_character.py",
                                   "class: Screen04CreateCharacter")
