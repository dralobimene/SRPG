# Fichier: screen02_play_or_run_save.py

import tkinter as tk
import sys
import os
import json

from classes.utilitaires.utilitaires_01 import Utilitaires01

from logger_config import configure_logger
# méthodes du logger (debug(), info(), warning(), error(), critical())
logger = configure_logger(__name__, 'logs/screen02_play_or_run_save.log')


class Screen02PlayOrRunSave:
    Utilitaires01.log_entry_message(logger,
                                    "debug",
                                    "screen02_play_or_run_save.py",
                                    "class: Screen02PlayOrRunSave")

    def __init__(self, root):
        print("=============================")
        print("file: screen02_play_or_run_save.py")
        print("")

        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen02_play_or_run_save.py",
                                        "method: def __init__()")

        self.root = root
        self.root.title("game/screen02_play_or_run_save.py")

        # contient le nom du fichier json qui contient les
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
                                           "screen02_play_or_run_save.py",
                                           "method: def __init__()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen02_play_or_run_save.py",
                                           "class: Screen02PlayOrRunSave")

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
                                           "screen02_play_or_run_save.py",
                                           "method: def __init__()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen02_play_or_run_save.py",
                                           "class: Screen02PlayOrRunSave")

            sys.exit()

        # ---------------------------------------------------------------------

        # Appliquer les dimensions à la fenêtre.
        self.root.geometry(str(self.window_width) +
                           "x" + str(self.window_height))

        self.frame = tk.Frame(root)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.btn_play_new_game = tk.Button(
            self.frame, text="Play new game.", command=self.play_new_game, width=20, height=2)
        self.btn_play_new_game.grid(row=0, column=0, sticky="w")

        self.btn_run_save = tk.Button(
            self.frame, text="Run a save.", command=self.run_save, width=20, height=2)
        self.btn_run_save.grid(row=1, column=0, sticky="w", pady=10)

        self.btn_quit = tk.Button(
            self.frame, text="Quit", command=root.destroy, width=20, height=2)
        self.btn_quit.grid(row=2, column=0, sticky="w", pady=10)

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen02_play_or_run_save.py",
                                       "method: def __init__()")

    # ========================================================================

    def play_new_game(self):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen02_play_or_run_save",
                                        "method: def play_new_game()")

        logger.info("player wants to play new game")

        # --------------------------------------------------------------------
        # Ecrire la clé qui contient le type de partie (new game or save)
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
        # Ajouter en fin de fichier la valeur qui défini si
        # l'utilisateur démarre une nvelle partie ou 1 partie sauvegardée.
        if file_network and file_writable:
            logger.info(f"Le fichier {file_network} est inscriptible")
            logger.info("Ecriture du type de partie (new game or save)")

            # Vérifier si le fichier existe
            if os.path.exists(file_network):
                # Charger les données existantes
                with open(file_network, 'r') as f:
                    data = json.load(f)

                # Ajouter la nouvelle paire clé => valeur
                new_key = "type_game"
                new_value = "new_game"
                data[new_key] = new_value

                # Réecrire le fichier avec les anciennes et nvelles
                # clés.
                with open(file_network, "w") as file:
                    json.dump(data, file, indent=4)

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen02_play_or_run_save.py",
                                               "method: def play_new_game()")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen02_play_or_run_save.py",
                                               "class: Screen02PlayOrRunSave")

                # Aller au prochain ecran.
                self.root.destroy()
                new_root = tk.Tk()
                import screen04_create_character
                screen04_create_character.Screen04CreateCharacter(new_root)
                new_root.mainloop()

            else:
                logger.error(f"Le fichier {file_network} n'existe pas.")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen02_play_or_run_save.py",
                                               "method: def play_new_game()")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen02_play_or_run_save",
                                               "class: Screen02PlayOrRunSave")

                sys.exit()

        else:
            logger.error(
                f"Le fichier {file_network} n'est pas inscriptible")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen02_play_or_run_save",
                                           "method: def play_new_game()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen02_play_or_run_save.py",
                                           "class: Screen02PlayOrRunSave")

            sys.exit()

        # ---------------------------------------------------------------------

    # ========================================================================

    def run_save(self):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen02_play_or_run_save.py",
                                        "method: def run_save()")

        logger.info("player wants to run a save")

        # --------------------------------------------------------------------
        # Ecrire la clé qui contient le type de partie (new game or save)
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
                                           "screen02_play_or_run_save.py",
                                           "method: def run_save()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen02_play_or_run_save.py",
                                           "class: Screen02PlayOrRunSave")

            sys.exit()

        # Si le fichier settings.json existe ET s'il est accessible
        # en ecriture alors:
        # Ajouter en fin de fichier la valeur qui défini si
        # l'utilisateur démarre une nvelle partie ou 1 partie sauvegardée.
        if file_network and file_writable:
            logger.info(f"Le fichier {file_network} est inscriptible")
            logger.info("Ecriture du type de partie (new game or save)")

            # Vérifier si le fichier existe
            if os.path.exists(file_network):
                # Charger les données existantes
                with open(file_network, 'r') as f:
                    data = json.load(f)

                # Ajouter la nouvelle paire clé => valeur
                new_key = "type_game"
                new_value = "saved_game"
                data[new_key] = new_value

                # Réecrire le fichier avec les anciennes et nvelles
                # clés.
                with open(file_network, "w") as file:
                    json.dump(data, file, indent=4)

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen02_play_or_run_save.py",
                                               "method: def run_save()")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen02_play_or_run_save.py",
                                               "class: Screen02PlayOrRunSave")

                # Aller au prochain ecran.
                self.root.destroy()
                new_root = tk.Tk()
                import screen04_create_character
                screen04_create_character.Screen04CreateCharacter(new_root)
                new_root.mainloop()

            else:
                logger.error(f"Le fichier {file_network} n'existe pas.")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen02_play_or_run_save.py",
                                               "method: def run_save()")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen02_play_or_run_save",
                                               "class: Screen02PlayOrRunSave")

                sys.exit()

        else:
            logger.error(
                f"Le fichier {file_network} n'est pas inscriptible")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen02_play_or_run_save",
                                           "method: def run_save()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen02_play_or_run_save.py",
                                           "class: Screen02PlayOrRunSave")

            sys.exit()


if __name__ == "__main__":
    root = tk.Tk()
    app = Screen02PlayOrRunSave(root)
    root.mainloop()
    Utilitaires01.log_exit_message(logger,
                                   "debug",
                                   "screen02_play_or_run_save.py",
                                   "class: Screen02PlayOrRunSave")
