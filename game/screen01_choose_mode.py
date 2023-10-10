# Fichier: screen01_choose_mode.py

# Commande pour executer le programme:
# PYTHONPATH="/home/sambano/Documents/python/jeu02/v07/game" python3.11 /home/sambano/Documents/python/jeu02/v07/game/screen01_choose_mode.py

import tkinter as tk
import os
import json
import sys

from classes.utilitaires.utilitaires_01 import Utilitaires01

from logger_config import configure_logger
# méthodes du logger (debug(), info(), warning(), error(), critical())
logger = configure_logger(__name__, 'logs/screen01_choose_mode.log')


class Screen01ChooseMode:
    Utilitaires01.log_entry_message(logger,
                                    "debug",
                                    "screen01_choose_mode.py",
                                    "class: Screen01ChooseMode")

    # =========================================================================

    def __init__(self, root):
        print("==============================================================")
        print("file: screen01_choose_mode.py")
        print("==============================================================")
        print("")

        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen01_choose_mode.py",
                                        "method: def __init__()")

        self.root = root
        self.root.title("game/screen01_choose_mode.py")

        # contient le nom du fichier json qui contient les
        # settings
        self.settings_file = "settings.json"

        # ---------------------------------------------------------------------

        #
        self.file_writable = True

        # Vérifier si le fichier existe
        if os.path.exists(self.settings_file):
            logger.info(f"Le fichier {self.settings_file} existe.")
        else:
            logger.warning(f"Le fichier {self.settings_file} n'existe pas.")
            logger.info("Création ...")

        # Vérifier si le fichier est inscriptible.
        if self.settings_file and self.file_writable:
            logger.info(f"Le fichier {self.settings_file} est inscriptible")

            # Défini width et height pour les fenetres du programmme.
            self.json_dict = {
                "width_window": 1200,
                "height_window": 800,
                "tile_size": 10
            }

            with open(self.settings_file, 'w') as f:
                # Écrire le dictionnaire en JSON dans le fichier
                json.dump(self.json_dict, f)

        # ---------------------------------------------------------------------

        # Appliquer les dimensions à la fenêtre.
        self.root.geometry("1200x800")

        self.frame = tk.Frame(root)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.btn_monoplayer = tk.Button(
            self.frame, text="Monoplayer mode.", command=self.monoplayer_mode, width=20, height=2)
        self.btn_monoplayer.grid(row=0, column=0, sticky="w")

        self.btn_multiplayer = tk.Button(
            self.frame, text="Multiplayer mode.", command=self.multiplayer_mode, width=20, height=2)
        self.btn_multiplayer.grid(row=1, column=0, sticky="w", pady=10)

        self.btn_quit = tk.Button(
            self.frame, text="Quit", command=root.destroy, width=20, height=2)
        self.btn_quit.grid(row=2, column=0, sticky="w", pady=10)

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen01_choose_mode.py",
                                       "method: def __init__()")

    # =========================================================================

    def monoplayer_mode(self):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen01_choose_mode.py",
                                        "method: def monoplayer_mode()")
        #
        try:
            with open(self.settings_file, "r") as file:

                # Charger les données existantes
                data = json.load(file)

                # Ajouter la nouvelle paire clé => valeur
                new_key = "mode"
                new_value = "monoplayer"
                data[new_key] = new_value

                # Réecrire le fichier avec les anciennes et nvelles
                # clés.
                with open(self.settings_file, "w") as file:
                    json.dump(data, file, indent=4)

            if os.path.exists(self.settings_file):
                logger.info(
                    "=======================================================")
                logger.info("File: screen01_choose_mode.py")
                logger.info("Méthode: monoplayer_mode()")
                logger.info(
                    f"01: Le fichier {self.settings_file} a été créé avec succès.")
                logger.info("")
            else:
                logger.info(
                    "=======================================================")
                logger.info("File: screen01_choose_mode.py")
                logger.info("Méthode: monoplayer_mode()")
                logger.error(
                    f"01: Le fichier {self.settings_file} est introuvable.")
                logger.info("")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen01_choose_mode.py",
                                               "method: def monoplayer_mode()")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen01_choose_mode.py",
                                               "class: Screen01ChooseMode")

                sys.exit()

        except Exception as error:
            logger.info(
                "=======================================================")
            logger.info("File: screen01_choose_mode.py")
            logger.info("Méthode: monoplayer_mode()")
            logger.error(f"02: Une erreur est survenue: {error}")
            logger.info("")

        #
        self.open_new_window()

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen01_choose_mode.py",
                                       "method: def monoplayer_mode()")

    # =========================================================================

    def multiplayer_mode(self):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen01_choose_mode.py",
                                        "method: def multiplayer_mode()")

        try:
            with open(self.settings_file, "r") as file:

                # Charger les données existantes
                data = json.load(file)

                # Ajouter la nouvelle paire clé => valeur
                new_key = "mode"
                new_value = "multiplayer"
                data[new_key] = new_value

                # Réecrire le fichier avec les anciennes et nvelles
                # clés.
                with open(self.settings_file, "w") as file:
                    json.dump(data, file, indent=4)

            if os.path.exists(self.settings_file):
                logger.info(
                    "=======================================================")
                logger.info("File: screen01_choose_mode.py")
                logger.info("Méthode: monoplayer_mode()")
                logger.info(
                    f"01: Le fichier {self.settings_file} a été créé avec succès.")
                logger.info("")

            else:
                logger.info(
                    "=======================================================")
                logger.info("File: screen01_choose_mode.py")
                logger.info("Méthode: monoplayer_mode()")
                logger.error(
                    f"01: Le fichier {self.settings_file} n'a pas été créé.")
                logger.info("")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen01_choose_mode.py",
                                               "method: def multiplayer_mode()")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen01_choose_mode.py",
                                               "class: Screen01ChooseMode")

                sys.exit()

        except Exception as error:
            logger.info(
                "=======================================================")
            logger.info("File: screen01_choose_mode.py")
            logger.info("Méthode: monoplayer_mode()")
            logger.error(f"02: Une erreur est survenue: {error}")
            logger.info("")

        #
        self.open_new_window()

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen01_choose_mode.py",
                                       "method: def multiplayer_mode()")

    # =========================================================================

    def open_new_window(self):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen01_choose_mode.py",
                                        "method: def open_new_window()")

        import screen02_play_or_run_save
        self.root.destroy()
        new_root = tk.Tk()
        screen02_play_or_run_save.Screen02PlayOrRunSave(new_root)
        new_root.mainloop()

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen01_choose_mode.py",
                                       "method: def open_new_window()")


if __name__ == "__main__":
    root = tk.Tk()
    app = Screen01ChooseMode(root)
    root.mainloop()
    Utilitaires01.log_exit_message(logger,
                                   "debug",
                                   "screen01_choose_mode.py",
                                   "class: Screen01ChooseMode")
