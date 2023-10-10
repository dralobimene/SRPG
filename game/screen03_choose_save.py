# Fichier: screen03_choose_save.py

import tkinter as tk
import sys
import os

from classes.utilitaires.utilitaires_01 import Utilitaires01

from logger_config import configure_logger
# méthodes du logger (debug(), info(), warning(), error(), critical())
logger = configure_logger(__name__, 'logs/screen03_choose_save.log')


class Screen03ChooseSave:
    Utilitaires01.log_entry_message(logger,
                                    "debug",
                                    "screen03_choose_save.py",
                                    "class: Screen03ChooseSave")

    def __init__(self, root):
        print("=============================")
        print("file: screen03_choose_save.py")
        print("")

        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen03_choose_save.py",
                                        "method: def __init__()")

        self.root = root

        # Définir le titre de la fenêtre
        self.root.title("screen03_choose_save.py")

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
                                           "screen03_choose_save.py",
                                           "method: def __init__()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen03_choose_save.py",
                                           "class: Screen03ChooseSave")

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
                                           "screen03_choose_save.py",
                                           "method: def __init__()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen03_choose_save.py",
                                           "class: Screen03ChooseSave")

            sys.exit()

        # ---------------------------------------------------------------------

        # Appliquer les dimensions à la fenêtre.
        self.root.geometry(str(self.window_width) +
                           "x" + str(self.window_height))

        # Créer un frame pour le bouton
        self.frame = tk.Frame(root)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Ajouter un bouton avec le label "Choose a save."
        self.btn_choose_save = tk.Button(
            self.frame, text="Choose a save", command=self.choose_save, width=20, height=2)
        self.btn_choose_save.grid(row=0, column=0, sticky="w", pady=10)

        # Ajouter un bouton pour quitter l'application
        self.btn_quit = tk.Button(
            self.frame, text="Quit", command=root.destroy, width=20, height=2)
        self.btn_quit.grid(row=1, column=0, sticky="w", pady=10)

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen03_choose_save.py",
                                       "method: def __init__()")

    # ========================================================================

    # Méthode qui sera appelée lorsque le bouton "Choose a save" est cliqué
    def choose_save(self):
        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen03_choose_save.py",
                                        "method: def choose_save()")

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen03_choose_save.py",
                                       "method: def choose_save()")


if __name__ == "__main__":
    root = tk.Tk()
    app = Screen03ChooseSave(root)
    root.mainloop()
    Utilitaires01.log_exit_message(logger,
                                   "debug",
                                   "screen03_choose_save.py",
                                   "class: Screen03ChooseSave")
