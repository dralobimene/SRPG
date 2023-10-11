# Fichier: screen05_generate_maps.py

import tkinter as tk
import os
import sys
import shutil
import json

from datetime import datetime

from classes.utilitaires.utilitaires_01 import Utilitaires01

from logger_config import configure_logger
# méthodes du logger (debug(), info(), warning(), error(), critical())
logger = configure_logger(__name__, 'logs/screen05_generate_maps.log')


class Screen05GenerateMaps:
    Utilitaires01.log_entry_message(logger,
                                    "debug",
                                    "screen05_generate_maps.py",
                                    "class: Screen05GenerateMaps")

    def __init__(self, root):
        """
        Initialize the screen for generating maps.

        This method sets up the Tkinter GUI for the screen to generate maps.
        It logs both the entry and exit of the method for debugging purposes.

        Parameters:
        - root (tk.Tk): The root Tkinter window object.

        Attributes:
        - self.root (tk.Tk): The root Tkinter window object.
        - self.frame (tk.Frame): The main frame where all widgets
          will be packed.
        - self.content (str): Will store the content of the file
          'game/temp_settings.txt'.
        - self.width (int): The width of the canvas for generating maps.
        - self.height (int): The height of the canvas for generating maps.
        - self.grid_width (int): The grid width for map generation.
        - self.grid_height (int): The grid height for map generation.
        - self.btn_generate_maps (tk.Button): Button to trigger map generation.
        - self.btn_quit (tk.Button): Button to quit the application.

        Side Effects:
        - Logs entry and exit of this method.
        - Initializes GUI elements.

        """

        print("==============================================================")
        print("file: screen05_generate_maps.py")
        print("==============================================================")
        print("")

        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen05_generate_maps.py",
                                        "method: def __init__()")

        self.root = root

        self.root.title("game/screen05_generate_maps.py")

        # Défini le nom du fichier json qui contient les
        # settings
        self.settings_file = "settings.json"

        # Définira les dimensios° de la fenetre.
        self.window_width = None
        self.window_height = None

        # Définira les dimensions des tiles.
        self.tile_size = None

        # ---------------------------------------------------------------------

        # Vérifier si le fichier existe
        if os.path.exists(self.settings_file):
            logger.info(f"Le fichier {self.settings_file} existe.")
        else:
            logger.error(f"Le fichier {self.settings_file} n'existe pas.")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen05_generate_maps.py",
                                           "method: def __init__()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen05_generate_maps.py",
                                           "class: Screen05GenerateMaps")

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

            # Définir les dimens° des tiles.
            self.tile_size = Utilitaires01.get_key_value_from_json(
                self.settings_file, "tile_size")
        else:
            logger.error(
                f"Le fichier {self.settings_file} n'est pas accessible en lecture.")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen05_generate_maps.py",
                                           "method: def __init__()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen05_generate_maps.py",
                                           "class: Screen05GenerateMaps")

            sys.exit()

        # ---------------------------------------------------------------------

        # Appliquer les dimensions à la fenêtre.
        self.root.geometry(str(self.window_width) +
                           "x" + str(self.window_height))

        self.frame = tk.Frame(root)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Recupérera le contenu du fichier game/temp_settings.txt.
        self.content = None

        # variables qui vont servir à la générat° des fichiers descriptifs.
        # (format des fichiers descriptif: txt).
        self.width = 800
        self.height = 600

        self.grid_width = self.width // 10
        self.grid_height = self.height // 10

        # ====================================================================
        # La GUI.

        self.btn_generate_maps = tk.Button(
            self.frame, text="Generate maps.", command=self.generate_txt_maps, width=20, height=2)
        self.btn_generate_maps.grid(row=0, column=0, sticky="w")

        self.btn_quit = tk.Button(
            self.frame, text="Quit", command=root.destroy, width=20, height=2)
        self.btn_quit.grid(row=2, column=0, sticky="w", pady=10)

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen05_generate_maps.py",
                                       "method: def __init__()")

    # ========================================================================

    def generate_txt_maps(self):
        """
        Generate text-based map files and handle associated operations.

        This method reads a settings file to determine the
        mode of the game
        (single-player or multi-player) and generates map files based
        on that.
        Various checks and operations are performed throughout the process.

        Attributes:
        - self.content (str): Content read from the settings file.
        - folder_name (str): Name of the folder that will contain
          generated text files.
        - json_folder_name (str): Name of the folder that will contain
          generated JSON files.

        Side Effects:
        - Reads game settings from 'temp_settings.txt'.
        - Creates folders for storing map files.
        - Generates map files.
        - Performs various checks on folders and files.
        - Logs various stages of the method for debugging.

        Raises:
        - SystemExit: If any critical condition is not met during
          the execution.
        """

        print("============================================================")
        print("Fichier: game/screen05_generate_maps.py.")
        print("methode: generate_txt_maps()")
        print("============================================================")

        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen05_generate_maps.py",
                                        "method: def generate_txt_maps()")

        #
        # self.btn_generate_maps.config(state=tk.DISABLED)

        # Récupère la valeur qui se trouve ds le fichier
        # "temp_settings.txt". Selon la valeur on stockera
        # les fichiers json sur le DD de l'utilisateur (monoplayer mode)
        # ou
        # on les stocke en DB (multiplayer mode).
        logger.info("> try: > appel Utilitaires01.read_file()")
        try:
            self.content = Utilitaires01.read_file(
                self.settings_file,
                "screen05_generate_maps.py",
                "generate_txt_maps",
                30
            )
        # Utilitaires01.read_file() will call sys.exit() on exception
        # If you reach this point, that means sys.exit()
        # was called and you can't really 'catch' it,
        # it will stop the script.
        except SystemExit:
            pass

        # Verificat° de self.content et de sa valeur.
        if self.content is None:
            logger.info(
                "============================================================")
            logger.info("PROBLEM 60")
            logger.info("Erreur : self.content est None.")
            logger.info("Fichier: screen05_generate_maps.py")
            logger.error("Erreur : self.content est None.")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen05_generate_maps.py",
                                           "method: def generate_txt_maps()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen05_generate_maps.py",
                                           "class: Screen05GenerateMaps")

            sys.exit()

        if os.path.exists(self.settings_file):
            # Vérifier si le fichier est accessible en lecture
            try:
                with open(self.settings_file, 'r') as f:
                    pass
            except IOError:
                logger.info(
                    f"Le fichier {self.settings_file} n'est pas accessible en lecture.")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen05_generate_maps.py",
                                               "method: def generate_txt_maps()")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen05_generate_maps.py",
                                               "class: Screen05GenerateMaps")

                sys.exit()

            else:
                # Fichier accessible en lecture, aller de l'avant pour lire la clé
                with open(self.settings_file, 'r') as f:
                    data = json.load(f)
                    mode_value = data.get('mode', 'Clé non trouvée')
                    if mode_value == 'Clé non trouvée':
                        logger.error(
                            f"La valeur de la clé 'mode' est: {mode_value}")

                        Utilitaires01.log_exit_message(logger,
                                                       "debug",
                                                       "screen05_generate_maps.py",
                                                       "method: def generate_txt_maps()")

                        Utilitaires01.log_exit_message(logger,
                                                       "debug",
                                                       "screen05_generate_maps.py",
                                                       "class: Screen05GenerateMaps")

                        sys.exit()

                    else:
                        logger.info(
                            f"def generate_txt_maps() 01: La valeur de la clé 'mode' est: {mode_value}")

        else:
            logger.info(f"Le fichier {self.settings_file} n'existe pas.")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen05_generate_maps.py",
                                           "method: def generate_txt_maps()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen05_generate_maps.py",
                                           "class: Screen05GenerateMaps")

            sys.exit()

        if mode_value == "monoplayer":
            logger.info(
                f"def generate_txt_maps() 02: La valeur de la clé 'mode' est: {mode_value}")
        elif mode_value == "multiplayer":
            logger.info(
                f"def generate_txt_maps() 02: La valeur de la clé 'mode' est: {mode_value}")
        else:
            logger.error(
                "============================================================")
            logger.error("PROBLEM 70")
            logger.error("Erreur : valeur inattendue de self.content.")
            logger.error("Fichier: screen05_generate_maps.py")
            logger.error("Méthode: generate_txt_maps()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen05_generate_maps.py",
                                           "method: def generate_txt_maps()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen05_generate_maps.py",
                                           "class: Screen05GenerateMaps")

            sys.exit()

        # Le nom du dossier qui contient les fichiers temporaires
        # descriptifs des donjons (au format txt).
        folder_name = "temp_txt_files"

        logger.info("> appel Utilitaires01.directory_exists()")
        if not Utilitaires01.directory_exists(folder_name):
            logger.warning(
                "============================================================")
            logger.warning("WARNING 01:")
            logger.info(f"Folder {folder_name} does not exist, it should.")
            logger.info("Creation ...")
            logger.info("Fichier: screen05_generate_maps.py")
            logger.info("Méthode: generate_txt_maps()")

            # Créer le dossier "temp_txt_files".
            logger.info("> appel Utilitaires01.create_folder()")
            Utilitaires01.create_folder(folder_name)

        logger.info("> appel Utilitaires01.is_folder_empty()")
        if Utilitaires01.is_folder_empty(folder_name):
            logger.info(
                "============================================================")
            logger.info("File: screen05_generate_maps.py")
            logger.info("Méthode: generate_txt_maps()")
            logger.info("Folder is empty, proceeding...")
        else:
            logger.info(
                "============================================================")
            logger.info("INFO 01:")
            logger.info("File: screen05_generate_maps.py")
            logger.info("Méthode: generate_txt_maps()")
            logger.info(f"Folder {folder_name} is not empty.")
            logger.info("We need to delete it's content.")

            # Vide le dossier "temp_txt_files".
            logger.info("> appel Utilitaires01.empty_folder()")
            Utilitaires01.empty_folder(folder_name)

        # Efface le dossier "temp_json_files".
        logger.info("> appel Utilitaires01.directory_exists()")
        if Utilitaires01.directory_exists('temp_json_files'):
            shutil.rmtree("temp_json_files")

        # Ajout d'une boucle for pour créer et traiter 20 fichiers
        for i in range(20):

            # Génère 20 fichiers descriptifs au format txt.
            # "i" pr donner un unique_id aux noms des fichiers.
            logger.info("> appel Utilitaires01.random_map_generation()")
            Utilitaires01.random_map_generation(
                self.grid_width, self.grid_height, (i + 1))

            # Vérifie si le dossier existe
            if os.path.exists(folder_name) and os.path.isdir(folder_name):
                # Liste tous les fichiers dans le dossier
                file_list = os.listdir(folder_name)

                # Boucle sur chaque fichier
                for file_name in file_list:
                    # Pr ne traiter que les fichiers dt le nom ne comporte pas
                    # le prefixe "processed_".
                    if not file_name.startswith('processed_'):
                        #
                        txt_file_path = os.path.join(folder_name, file_name)

                        # Vérifie si le fichier txt_file_path existe avant
                        # de l'ouvrir.
                        if os.path.exists(txt_file_path):
                            logger.info(
                                "> appel Utilitaires01.handle_file_operations()")
                            Utilitaires01.handle_file_operations(
                                txt_file_path, self.remove_empty_first_line)

                        # Effectuez vos opérations sur le fichier ici.
                        # Remplacer des caractéres par d'autres dans les
                        # fichiers qui st ds "temp_txt_files".
                        logger.info(
                            "> appel Utilitaires01.replace_adjacent_characters()")
                        Utilitaires01.replace_adjacent_characters(
                            txt_file_path)

                        # Défini un préfixe pour le prochain fichier traité.
                        new_name = 'processed_' + file_name

                        # Renomme le fichier traité avec le préfixe.
                        os.rename(txt_file_path, os.path.join(
                            folder_name, new_name))

            else:
                logger.error(
                    "========================================================")
                logger.error("PROBLEM 02")
                logger.error("Fichier: screen05_generate_maps.py")
                logger.error("Méthode: generate_txt_maps()")
                logger.error(f"Folder {folder_name} does not exist.")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen05_generate_maps.py",
                                               "method: def generate_txt_maps()")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen05_generate_maps.py",
                                               "class: Screen05GenerateMaps")

                sys.exit()

        # Créez le fichier JSON correspondant
        # Liste tous les fichiers dans le dossier "temp_txt_files"
        file_list = os.listdir("temp_txt_files")

        # Créer un répertoire pour les fichiers JSON s'il n'existe pas
        json_folder_name = "temp_json_files"
        if not os.path.exists(json_folder_name):
            logger.info("> appel Utilitaires01.create_directory()")
            Utilitaires01.create_directory(json_folder_name,
                                           "screen05_generate_maps.py",
                                           "generate_txt_maps()",
                                           5)

        # Parcourir chaque fichier txt dans le dossier "temp_txt_files"
        for file_name in file_list:
            # Ignorer les fichiers qui n'ont pas été traités
            if not file_name.startswith('processed_'):
                continue

            # Générer le chemin du fichier texte et du fichier JSON
            txt_file_path = os.path.join("temp_txt_files", file_name)
            json_file_name = file_name.replace(
                ".txt", ".json").replace("processed_", "")
            json_file_path = os.path.join(json_folder_name, json_file_name)

            # Appeler la méthode pour générer le fichier JSON
            # correspondant à son fichier txt.
            logger.info("> appel generate_json_from_txt()")
            self.generate_json_from_txt(txt_file_path, json_file_path)

        logger.info("> appel choose_place_to_store_maps()")
        self.choose_place_to_store_maps()

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen05_generate_maps.py",
                                       "method: def generate_txt_maps()")

    # ========================================================================

    def generate_json_from_txt(self,
                               txt_file_path,
                               json_file_path,
                               tile_size=None):
        """
        Generate a JSON file from a given text file to describe a map layout.

        This method reads a given text file and generates a JSON file that
        contains structured information about a game map, including the
        positions and types of different tiles.

        Parameters:
        - txt_file_path (str): The path to the input text file.
        - json_file_path (str): The path where the generated JSON file
          will be saved.
        - tile_size (int, optional): The size of each tile in pixels.
          Default is 10.

        Attributes:
        - lines (List[str]): The lines read from the text file.
        - total_tiles (List[Dict]): A list of dictionaries,
          each describing a tile.
        - floor_tiles (List[Dict]): A list of dictionaries
          describing floor tiles.
        - walls_tiles (List[Dict]): A list of dictionaries
          describing wall tiles.
        - json_data (Dict): The data to be saved as a JSON file.

        Side Effects:
        - Reads the text file from 'txt_file_path'.
        - Writes the generated JSON data to 'json_file_path'.
        - Logs various stages of the method for debugging.

        Raises:
        - SystemExit: If any critical condition is not met during execution.

        Returns:
        None
        """

        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen05_generate_maps.py",
                                        "method: def generate_json_from_txt()")

        # Utiliser la valeur de self.tile_size si aucune valeur
        # spécifique n'est fournie.
        if tile_size is None:
            tile_size = self.tile_size

        try:
            # Utilisez la méthode read_file pour lire
            # le contenu du fichier texte
            logger.info("> appel Utilitaires01.read_file()")
            lines = Utilitaires01.read_file(
                txt_file_path,
                "screen05_generate_maps.py",
                "generate_json_from_txt",
                40
            ).splitlines()

            # Initialise les listes
            total_tiles = []
            floor_tiles = []
            walls_tiles = []

            # Parcourir le fichier ligne par ligne et caractère par caractère
            for y, line in enumerate(lines):
                for x, char in enumerate(line.strip()):
                    # Coordonnées du tile en pixels
                    x_pixel = x * tile_size
                    y_pixel = y * tile_size

                    tile = {
                        "x": x_pixel,
                        "y": y_pixel,
                        "w": tile_size,
                        "h": tile_size,
                        "center": [x_pixel + tile_size / 2, y_pixel + tile_size / 2]
                    }

                    if char == "?":
                        tile["color"] = "white"
                        tile["walkable"] = True
                        floor_tiles.append(tile)
                    elif char == ".":
                        tile["color"] = "blue"
                        tile["walkable"] = False
                        walls_tiles.append(tile)

                    total_tiles.append(tile)

            if os.path.exists(self.settings_file):
                # Vérifier si le fichier est accessible en lecture
                try:
                    with open(self.settings_file, 'r') as f:
                        pass
                except IOError:
                    logger.info(
                        f"Le fichier {self.settings_file} n'est pas accessible en lecture.")

                    Utilitaires01.log_exit_message(logger,
                                                   "debug",
                                                   "screen05_generate_maps.py",
                                                   "method: def generate_json_from_txt()")

                    Utilitaires01.log_exit_message(logger,
                                                   "debug",
                                                   "screen05_generate_maps.py",
                                                   "class: Screen04CreateCharacter")

                    sys.exit()

                else:
                    # Fichier accessible en lecture, aller de l'avant pour lire la clé
                    with open(self.settings_file, 'r') as f:
                        data = json.load(f)
                        mode_value = data.get('mode', 'Clé non trouvée')
                        if mode_value == 'Clé non trouvée':
                            logger.error(
                                f"def generate_json_from_txt() 01: La valeur de la clé 'mode' est: {mode_value}")

                            Utilitaires01.log_exit_message(logger,
                                                           "debug",
                                                           "screen05_generate_maps.py",
                                                           "method: def generate_json_from_txt()")

                            Utilitaires01.log_exit_message(logger,
                                                           "debug",
                                                           "screen05_generate_maps.py",
                                                           "class: Screen05GenerateMaps")

                            sys.exit()
                        else:
                            logger.info(
                                f"def generate_json_from_txt() 01: La valeur de la clé 'mode' est: {mode_value}")
            else:
                logger.info(f"Le fichier {self.settings_file} n'existe pas.")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen05_generate_maps.py",
                                               "method: def generate_json_from_txt()")

                Utilitaires01.log_exit_message(logger,
                                               "debug",
                                               "screen05_generate_maps.py",
                                               "class: Screen05GenerateMaps")

                sys.exit()

            # Création du dictionnaire pour le fichier JSON
            json_data = {
                "file": os.path.basename(json_file_path).split('.')[0],
                "mode": mode_value,
                "total_tiles": total_tiles,
                "floor_tiles": floor_tiles,
                "walls_tiles": walls_tiles
            }

            # Écriture du fichier JSON
            logger.info("> appel Utilitaires01.write_json_file()")
            Utilitaires01.write_json_file(
                json_data,
                json_file_path,
                "screen05_generate_maps.py",
                "generate_json_from_txt",
                50
            )

        #
        except SystemExit:
            pass

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen05_generate_maps.py",
                                       "method: def generate_json_from_txt()")

    # ========================================================================

    def choose_place_to_store_maps(self):
        """
        Choose the appropriate directory to store generated map files
        based on the game mode.

        This method creates directories for storing generated map files
        and copies those files
        from a temporary location to the final destination. The method
        differentiates between
        monoplayer and multiplayer modes.

        Parameters:
        None

        Attributes:
        - monoplayer_path (str): The path to the monoplayer save directory.
        - multiplayer_path (str): The path to the multiplayer save directory.
        - current_date (str): The current date in YYYY_MM_DD_HH_MM_SS format.
        - new_folder_name (str): The name of the new folder created to store
          map files.
        - src_folder (str): The temporary folder containing JSON map files.
        - src_path (str): Source path for individual map files.
        - dst_path (str): Destination path for individual map files.

        Side Effects:
        - Creates directories if they do not exist.
        - Copies map files from a temporary location to their final location.
        - Logs various stages of the method for debugging.
        - May exit the application in case of a critical problem.

        Raises:
        - SystemExit: If the 'content' attribute is neither
          'mode: monoplayer' nor 'mode: multiplayer'.

        Returns:
        None
        """

        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen05_generate_maps.py",
                                        "method: def choose_place_to_store_maps()")

        # Créer le dossier "save" si nécessaire
        if not os.path.exists("save"):
            logger.info("> appel Utilitaires01.create_directory()")
            Utilitaires01.create_directory("save",
                                           "screen05_generate_maps.py",
                                           "method: choose_place_to_store_maps()",
                                           8)

        # ===
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
                # Fichier accessible en lecture, aller de l'avant pour
                # lire la clé
                with open(self.settings_file, 'r') as f:
                    data = json.load(f)
                    mode_value = data.get('mode', 'Clé non trouvée')
                    if mode_value == 'Clé non trouvée':
                        logger.error(
                            f"La valeur de la clé 'mode' est: {mode_value}")

                        Utilitaires01.log_exit_message(logger,
                                                       "debug",
                                                       "screen05_generate_maps.py",
                                                       "method: def choose_place_to_store_maps()")

                        Utilitaires01.log_exit_message(logger,
                                                       "debug",
                                                       "screen05_generate_maps.py",
                                                       "class: Screen05GenerateMaps")

                        sys.exit()

                    else:
                        logger.info(
                            f"La valeur de la clé 'mode' est: {mode_value}")
        else:
            logger.info(f"Le fichier {self.settings_file} n'existe pas.")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen05_generate_maps.py",
                                           "method: def choose_place_to_store_maps()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen05_generate_maps.py",
                                           "class: Screen05GenerateMaps")

            sys.exit()

        # ===
        if mode_value == "monoplayer":
            logger.info(
                "============================================================")
            logger.info("We need to store maps for a monoplayer mode game.")

            # Créer le dossier "monoplayer" dans "save" si nécessaire
            monoplayer_path = os.path.join("save", "monoplayer")
            if not os.path.exists(monoplayer_path):
                logger.info("> appel Utilitaires01.create_directory()")
                Utilitaires01.create_directory(monoplayer_path,
                                               "screen05_generate_maps.py",
                                               "choose_place_to_store_maps()",
                                               10)

            # Créer le nom du nouveau dossier avec la date courante
            current_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            new_folder_name = os.path.join(monoplayer_path, current_date)

            # Créer le nouveau dossier dans "monoplayer"
            logger.info("> appel Utilitaires01.create_directory()")
            Utilitaires01.create_directory(new_folder_name,
                                           "screen05_generate_maps.py",
                                           "choose_place_to_store_maps()",
                                           12)

        elif mode_value == "multiplayer":
            logger.info(
                "============================================================")
            logger.info("We need to store maps for a multiplayer mode game.")

            # Créer le dossier "multiplayer" dans "save" si nécessaire
            multiplayer_path = os.path.join("save", "multiplayer")
            if not os.path.exists(multiplayer_path):
                logger.info("> appel Utilitaires01.create_directory()")
                Utilitaires01.create_directory(multiplayer_path,
                                               "screen05_generate_maps.py",
                                               "choose_place_to_store_maps()",
                                               43)

            # Créer le nom du nouveau dossier avec la date courante
            current_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            new_folder_name = os.path.join(multiplayer_path, current_date)

            # Créer le nouveau dossier dans "multiplayer"
            logger.info("> appel Utilitaires01.create_directory()")
            Utilitaires01.create_directory(new_folder_name,
                                           "screen05_generate_maps.py",
                                           "choose_place_to_store_maps()",
                                           20)

        else:
            logger.error(
                "============================================================")
            logger.error("PROBLEM 01:")
            logger.error("Fichier: game/screen05_generate_maps.py")
            logger.error("Methode: choose_place_to_store_maps()")

            os.remove("temp_settings.txt")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen05_generate_maps.py",
                                           "method: def generate_json_from_txt()")

            Utilitaires01.log_exit_message(logger,
                                           "debug",
                                           "screen05_generate_maps.py",
                                           "class: Screen05GenerateMaps")

            sys.exit()

        # Copier le contenu du dossier "temp_json_files"
        # dans le nouveau dossier
        src_folder = "temp_json_files"
        for filename in os.listdir(src_folder):
            src_path = os.path.join(src_folder, filename)
            dst_path = os.path.join(new_folder_name, filename)
            shutil.copy2(src_path, dst_path)

        # Effacer les dossiers "temp_json_files" et "temp_txt_files"
        shutil.rmtree("temp_json_files")
        shutil.rmtree("temp_txt_files")

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen05_generate_maps.py",
                                       "method: def generate_txt_maps()")

        # Aller à la prochaine fenêtre.
        # TODO:
        # Ecrire des verifications.
        self.go_to_next_screen()

    # ========================================================================

    def remove_empty_first_line(self,
                                file):
        """
        Méthode qui sert de callback à la méthode implémentée
        ds classes/utilitaires/utilitaires_01.py
        méthode: handle_file_operations().

        Retire la 1° L des fichiers txt descriptifs des donjons qui
        st générés avec le BSP de type 1 (ou du type 2). L'1 de
        ces 2 BSPs crées une 1° L vide avt de générer la carte au
        format ASCII.
        """

        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen05_generate_maps.py",
                                        "method: def remove_empty_first_line()")

        lines = file.readlines()
        file.seek(0)
        file.truncate(0)
        if lines and lines[0].strip() == "":
            file.writelines(lines[1:])
        else:
            file.writelines(lines)

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen05_generate_maps.py",
                                       "method: def remove_empty_first_line()")

    # ========================================================================

    def go_to_next_screen(self):
        """
        """

        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "screen05_generate_maps.py",
                                        "method: def open_new_window()")

        logger.info("open new window")
        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen05_generate_maps.py",
                                       "method: def open_new_window()")

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "screen05_generate_maps.py",
                                       "class: Screen05GenerateMaps")

        import screen06_game
        self.root.destroy()
        instance = screen06_game.Screen06Game()
        instance.run_game()

    # ========================================================================


if __name__ == "__main__":
    root = tk.Tk()
    app = Screen05GenerateMaps(root)
    root.mainloop()
    Utilitaires01.log_exit_message(logger,
                                   "debug",
                                   "screen05_generate_maps.py",
                                   "class: Screen05GenerateMaps")
