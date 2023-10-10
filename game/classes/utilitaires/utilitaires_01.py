# classes/utilitaires/utilitaires_01.py

from bsps.bsp02.DungeonFileGenerator import DungeonFileGenerator
from bsps.bsp01.GameMap import GameMap
from typing import Any, Optional, List, Callable, IO
from PIL import Image, ImageTk
from datetime import datetime
import pygame
import os
import sys
import shutil
import json
import subprocess
import tcod
import random

from logger_config import configure_logger
# méthodes du logger (debug(), info(), warning(), error(), critical())
logger = configure_logger(__name__, 'logs/utilitaires_01.log')


# from classes.Tiles.Exit import Exit
# from classes.Tiles.Entry import Entry


"""
N'oubliez pas que lorsque vous utilisez des méthodes statiques,
vous n'aurez pas accès aux variables
d'instance ou aux autres méthodes d'instance de la classe dans ces méthodes.
Si vous avez besoin
d'accéder à des données spécifiques à l'instance, vous devez envisager
d'utiliser des méthodes
d'instance à la place.
"""


class Utilitaires01:
    """
    pydoc de Utilitaires01:

    NOTES:
        01:
            PAS DE def __init__() ???
    """

    # constantes
    TILE_SIZE = 16

    # =========================================================================

    @staticmethod
    def directory_exists(dir_path: str) -> bool:
        """
        Checks if the provided directory exists.

        Args:
            dir_path (str): The path to the directory.

        Returns:
            bool: True if the directory exists, False otherwise.
        usage:
            if directory_exists("/path/to/directory"):
                print("Directory exists.")
            else:
                print("Directory does not exist.")
        """

        # Marquer le début de la méthode
        Utilitaires01.log_entry_message(logger,
                                        "info",
                                        "classes/utilitaires/utilitaires_01.py",
                                        "method: directory_exists()")

        # Marquer la fin de la méthode
        Utilitaires01.log_exit_message(logger,
                                       "info",
                                       "classes/utilitaires/utilitaires_01.py",
                                       "method: directory_exists()")

        return os.path.isdir(dir_path)

    # =========================================================================

    @staticmethod
    def create_folder(path: str) -> None:
        """
        Creates a folder at the specified path.

        :param path: The path where the folder should be created
        :type path: str
        :raises FileExistsError: If the folder already exists
        :raises Exception: If any other exception occurs

        Usage
        path = 'my_folder'
        Utilitaires01.create_folder(path)
        """

        # Marquer le début de la méthode
        Utilitaires01.log_entry_message(logger,
                                        "info",
                                        "classes/utilitaires/utilitaires_01.py",
                                        "method: create_folder()")

        try:
            os.makedirs(path)
            logger.info(
                "==============================================================")
            logger.info("File: classes/utilitaires/utilitaires_01.py")
            logger.info("méthode: create_folder()")
            logger.info(f"Folder '{path}' created successfully")
        except FileExistsError as error1:
            logger.warning(
                "==============================================================")
            logger.warning("File: classes/utilitaires/utilitaires_01.py")
            logger.warning("Méthode: create_folder()")
            logger.warning(f"Folder '{path}' already exists")
            raise error1
        except Exception as error2:
            logger.info(
                "==============================================================")
            logger.info("File: classes/utilitaires/utilitaires_01.py")
            logger.info("Méthode: create_folder()")
            logger.error(
                f"An error occurred while creating the folder: {error2}")

            # Marquer la fin de la méthode
            Utilitaires01.log_exit_message(logger,
                                           "info",
                                           "classes/utilitaires/utilitaires_01.py",
                                           "method: create_folder()")

            sys.exit()

        # Marquer la fin de la méthode
        Utilitaires01.log_exit_message(logger,
                                       "info",
                                       "classes/utilitaires/utilitaires_01.py",
                                       "method: create_folder()")

    # =========================================================================

    @staticmethod
    def is_folder_empty(folder_path: str) -> bool:
        """
        Checks whether the specified folder is empty or not.

        :param folder_path: Path to the directory to be checked.
        :type folder_path: str
        :return: True if the folder is empty, False otherwise.
        :rtype: bool
        :raises FileNotFoundError: If the specified folder does not exist.

        usage:
        if Utilitaires01.is_folder_empty("/path/to/folder"):
            print("The folder is empty")
        else:
            print("The folder is not empty")
        """

        # Marquer le début de la méthode
        Utilitaires01.log_entry_message(logger,
                                        "info",
                                        "classes/utilitaires/utilitaires_01.py",
                                        "method: is_folder_empty()")

        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder {folder_path} does not exist.")

        # Marquer la fin de la méthode
        Utilitaires01.log_exit_message(logger,
                                       "info",
                                       "classes/utilitaires/utilitaires_01.py",
                                       "method: is_folder_empty()")

        return not bool(os.listdir(folder_path))

    # =========================================================================

    @staticmethod
    def empty_folder(path: str) -> None:
        """
        Empties the contents of the specified folder.

        This function will remove all files and subdirectories inside the given
        folder without deleting the folder itself.

        :param path: The path to the folder that should be emptied.
        :type path: str
        :raises ValueError: If the path does not exist or is not a directory.
        :raises PermissionError: If the permissions on the file system
        do not allow deletion.

        usage
        Utilitaires01.empty_folder('/path/to/folder')
        """

        # Marquer le début de la méthode
        Utilitaires01.log_entry_message(logger,
                                        "info",
                                        "classes/utilitaires/utilitaires_01.py",
                                        "method: empty_folder()")

        if not os.path.exists(path):
            raise ValueError("Path does not exist: " + path)

            logger.info("File: classes/utilitaires/utilitaires_01.py")
            logger.info("Methode: empty_folder()")
            logger.error("Error 01: Path does not exist")

            # Marquer la fin de la méthode
            Utilitaires01.log_exit_message(logger,
                                           "info",
                                           "classes/utilitaires/utilitaires_01.py",
                                           "method: empty_folder()")

            sys.exit()

        if not os.path.isdir(path):
            raise ValueError("Path is not a directory: " + path)

            logger.info("File: classes/utilitaires/utilitaires_01.py")
            logger.info("Methode: empty_folder()")
            logger.error("Error 02: Path is not a directory")

            # Marquer la fin de la méthode
            Utilitaires01.log_exit_message(logger,
                                           "info",
                                           "classes/utilitaires/utilitaires_01.py",
                                           "method: empty_folder()")

            sys.exit()

        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    logger.info(
                        "==============================================================")
                    logger.info("File: classes/utilitaires/utilitaires_01.py")
                    logger.info("Méthode: empty_folder()")
                    logger.info("File deleted:", file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    logger.info(
                        "==============================================================")
                    logger.info("File: classes/utilitaires/utilitaires_01.py")
                    logger.info("Methode: empty_folder()")
                    logger.info("Directory deleted:", file_path)
            except Exception as error1:
                logger.error(
                    "==============================================================")
                logger.info("File: classes/utilitaires/utilitaires_01.py")
                logger.info("Méthode: empty_folder()")
                logger.error('Failed to delete %s. Reason: %s' %
                             (file_path, error1))

                # Marquer la fin de la méthode
                Utilitaires01.log_exit_message(logger,
                                               "info",
                                               "classes/utilitaires/utilitaires_01.py",
                                               "method: empty_folder()")

                sys.exit()

        # Marquer la fin de la méthode
        Utilitaires01.log_exit_message(logger,
                                       "info",
                                       "classes/utilitaires/utilitaires_01.py",
                                       "method: empty_folder()")

    # =========================================================================

    @staticmethod
    def create_directory(directory_name: str,
                         file_name: str,
                         method_name: str,
                         problem_number: int) -> None:
        """
        Crée un nouveau répertoire avec le nom spécifié.

        Parameters:
        directory_name (str): Le nom du répertoire à créer.
        file_name (str): Le nom du fichier où la méthode est appelée,
        utilisé pour le logging.
        method_name (str): Le nom de la méthode où cette fonction
        est appelée, utilisé pour le logging.
        problem_number (int): Le numéro du problème à afficher en
        cas d'erreur, utilisé pour le logging.

        Returns:
        None: Cette méthode ne retourne rien.

        Side Effects:
        - Un nouveau répertoire peut être créé.
        - Des messages de log sont générés pour indiquer le
          déroulement de la méthode.
        - Le programme peut sortir en cas d'erreur de permission
          ou d'autres exceptions.

        Example:
        >>> Utilitaires01.create_directory("new_folder",
                                            "example_file.py",
                                            "example_method",
                                            1)

        Note:
        Cette méthode utilise des méthodes de logging pour marquer
        le début et la fin de son exécution.
        """

        # Marquer le début de la méthode
        Utilitaires01.log_entry_message(logger,
                                        "info",
                                        "classes/utilitaires/utilitaires_01.py",
                                        "method: create_directory()")

        try:
            os.mkdir(directory_name)
            logger.info(
                "==============================================================")
            logger.info("File: classes/utilitaires/utilitaires_01.py")
            logger.info("Méthode: create_directory()")
            logger.info(f"Le dossier {directory_name} a été créé.")
        except FileExistsError:
            logger.warning(
                "==============================================================")
            logger.warning("File: classes/utilitaires/utilitaires_01.py")
            logger.warning("Méthode: create_directory()")
            logger.warning(
                f"Folder {directory_name} already exists, we continue.")
        except PermissionError:
            logger.info(
                "==============================================================")
            logger.info(f"PROBLEM {problem_number}")
            logger.info(f"File: {file_name}")
            logger.info(f"Méthode: {method_name}")
            logger.error("Permission refused")

            # Marquer la fin de la méthode
            Utilitaires01.log_exit_message(logger,
                                           "info",
                                           "classes/utilitaires/utilitaires_01.py",
                                           "method: create_directory()")

            sys.exit()
        except Exception as error:
            logger.info(
                "==============================================================")
            logger.info(f"PROBLEM {problem_number + 1}")
            logger.error(f"Une erreur s'est produite: {error}")
            logger.info(f"File: {file_name}")
            logger.info(f"Méthode: {method_name}")

            # Marquer la fin de la méthode
            Utilitaires01.log_exit_message(logger,
                                           "info",
                                           "classes/utilitaires/utilitaires_01.py",
                                           "method: create_directory()")

            sys.exit()

        # Marquer la fin de la méthode
        Utilitaires01.log_exit_message(logger,
                                       "info",
                                       "classes/utilitaires/utilitaires_01.py",
                                       "method: create_directory()")

    # =========================================================================

    @staticmethod
    def read_file(file_path: str,
                  file_name: str,
                  method_name: str,
                  problem_number: int) -> str:
        """
        Lit le contenu d'un fichier texte et retourne son contenu sous
        forme de chaîne de caractères.

        Parameters:
        file_path (str): Le chemin vers le fichier à lire.
        file_name (str): Le nom du fichier où la méthode est appelée,
        utilisé pour le logging.
        method_name (str): Le nom de la méthode où cette fonction est
        appelée, utilisé pour le logging.
        problem_number (int): Le numéro du problème à afficher en cas
        d'erreur, utilisé pour le logging.

        Returns:
        str: Le contenu du fichier lu, retourné comme une chaîne de caractères.

        Side Effects:
        - Des messages de log sont générés pour indiquer le
          déroulement de la méthode.
        - Le programme peut sortir en cas de FileNotFoundError,
          PermissionError ou d'autres exceptions.

        Example:
        >>> content = Utilitaires01.read_file("/path/to/file.txt",
                                                "example_file.py",
                                                "example_method",
                                                1)

        Note:
        Cette méthode utilise des méthodes de logging pour marquer
        le début et la fin de son exécution.
        """

        # Marquer le début de la méthode
        Utilitaires01.log_entry_message(logger,
                                        "info",
                                        "classes/utilitaires/utilitaires_01.py",
                                        "method: read_file()")

        try:
            if os.path.exists(file_path):
                # A REMPLACER
                with open(file_path, "r") as f:
                    content = f.read()
                    return content
        except FileNotFoundError:
            logger.error(
                "==============================================================")
            logger.error(f"PROBLEM {problem_number}")
            logger.error(f"File: {file_name}")
            logger.error(f"Méthode: {method_name}")
            logger.error(f"Fichier {file_path} non trouvé.")

            # Marquer la fin de la méthode
            Utilitaires01.log_exit_message(logger,
                                           "info",
                                           "classes/utilitaires/utilitaires_01.py",
                                           "method: read_file()")

            sys.exit()
        except PermissionError:
            logger.error(
                "==============================================================")
            logger.error(f"PROBLEM {problem_number + 1}")
            logger.error(f"File: {file_name}")
            logger.error(f"Méthode: {method_name}")
            logger.error("Permission refusée pour lire le fichier.")

            # Marquer la fin de la méthode
            Utilitaires01.log_exit_message(logger,
                                           "info",
                                           "classes/utilitaires/utilitaires_01.py",
                                           "method: read_file()")

            sys.exit()
        except Exception as error:
            logger.error(
                "==============================================================")
            logger.error(f"PROBLEM {problem_number + 2}")
            logger.error(f"File: {file_name}")
            logger.error(f"Méthode: {method_name}")
            logger.error(f"Une erreur s'est produite: {error}")

            # Marquer la fin de la méthode
            Utilitaires01.log_exit_message(logger,
                                           "info",
                                           "classes/utilitaires/utilitaires_01.py",
                                           "method: read_file()")

            sys.exit()

        # Marquer la fin de la méthode
        Utilitaires01.log_exit_message(logger,
                                       "info",
                                       "classes/utilitaires/utilitaires_01.py",
                                       "method: read_file()")

    # =========================================================================

    @staticmethod
    def write_json_file(json_data: dict,
                        json_file_path: str,
                        file_name: str,
                        method_name: str,
                        problem_number: int) -> None:
        """
        Écrit un dictionnaire Python dans un fichier JSON.

        Parameters:
        json_data (dict): Le dictionnaire à écrire dans le fichier JSON.
        json_file_path (str): Le chemin vers le fichier JSON à écrire.
        file_name (str): Le nom du fichier où la méthode est appelée,
        utilisé pour le logging.
        method_name (str): Le nom de la méthode où cette fonction est
        appelée, utilisé pour le logging.
        problem_number (int): Le numéro du problème à afficher en cas
        d'erreur, utilisé pour le logging.

        Returns:
        None

        Side Effects:
        - Des messages de log sont générés pour indiquer le déroulement
          de la méthode.
        - Un fichier JSON est créé ou écrasé.
        - Le programme peut sortir en cas de PermissionError ou
          d'autres exceptions.

        Example:
        >>> Utilitaires01.write_json_file({"key": "value"},
                                            "/path/to/file.json",
                                            "example_file.py",
                                            "example_method",
                                            1)

        Note:
        Cette méthode utilise des méthodes de logging pour marquer
        le début et la fin de son exécution.
        """
        # Marquer le début de la méthode
        Utilitaires01.log_entry_message(logger,
                                        "info",
                                        "classes/utilitaires/utilitaires_01.py",
                                        "method: write_json_file()")
        try:
            # A REMPLACER
            with open(json_file_path, 'w') as f:
                json.dump(json_data, f, indent=4)
            logger.info(
                "============================================================")
            logger.info("File: classes/utilitaires/utilitaires_01.py")
            logger.info("Méthode: write_json_file()")
            logger.info(f"Fichier JSON {json_file_path} écrit avec succès.")
        except PermissionError:
            logger.error(
                "============================================================")
            logger.error(f"PROBLEM {problem_number}")
            logger.error(f"File: {file_name}")
            logger.error(f"Méthode: {method_name}")
            logger.error("Permission refusée pour écrire le fichier.")

            # Marquer la fin de la méthode
            Utilitaires01.log_exit_message(logger,
                                           "info",
                                           "classes/utilitaires/utilitaires_01.py",
                                           "method: write_json_file()")

            sys.exit()
        except Exception as error:
            logger.error(
                "============================================================")
            logger.error(f"PROBLEM {problem_number + 1}")
            logger.error(f"File: {file_name}")
            logger.error(f"Méthode: {method_name}")
            logger.error(f"Une erreur s'est produite: {error}")

            # Marquer la fin de la méthode
            Utilitaires01.log_exit_message(logger,
                                           "info",
                                           "classes/utilitaires/utilitaires_01.py",
                                           "method: write_json_file()")

            sys.exit()

        # Marquer la fin de la méthode
        Utilitaires01.log_exit_message(logger,
                                       "info",
                                       "classes/utilitaires/utilitaires_01.py",
                                       "method: write_json_file()")

    # =========================================================================

    @staticmethod
    def log_entry_message(logger: logger,
                          log_type: str,
                          file_name: str,
                          method_name: str) -> None:
        """
        Log l'entrée dans une méthode donnée.

        Parameters:
        logger (logging.Logger): Instance du logger utilisée pour
        loguer les informations.
        log_type (str): Le type de message à loguer
        (e.g., "info", "warning", "error").
        file_name (str): Le nom du fichier où la méthode est appelée,
        utilisé pour le logging.
        method_name (str): Le nom de la méthode où cette fonction est appelée.

        Returns:
        None
        """

        log_header = "========================================================"
        log_file = f"File: {file_name}"
        log_method = f">>> {method_name}"

        logger_method = getattr(logger, log_type, None)
        if logger_method is not None:
            logger_method(log_header)
            logger_method(log_file)
            logger_method(log_method)

    @staticmethod
    def log_exit_message(logger: logger,
                         log_type: str,
                         file_name: str,
                         method_name: str) -> None:
        """
        Log la sortie d'une méthode donnée.

        Parameters:
        logger (logging.Logger): Instance du logger utilisée pour loguer
        les informations.
        log_type (str): Le type de message à loguer
        (e.g., "info", "warning", "error").
        file_name (str): Le nom du fichier où la méthode est appelée,
        utilisé pour le logging.
        method_name (str): Le nom de la méthode où cette fonction est appelée.

        Returns:
        None
        """

        log_espace = ""
        log_file = f"File: {file_name}"
        log_method = f"Fin de la {method_name} <<<"
        log_footer = "========================================================"

        logger_method = getattr(logger, log_type, None)
        if logger_method is not None:
            logger_method(log_espace)
            logger_method(log_file)
            logger_method(log_method)
            logger_method(log_footer)

    # =========================================================================

    # @staticmethod
    # def draw_map_from_json(file_path: str,
    #                        canvas) -> None:
    #     """
    #     Dessine une carte à partir d'un fichier JSON.
    #
    #     :param file_path: Le chemin du fichier JSON à lire.
    #     :param canvas: Le canvas sur lequel dessiner la carte.
    #     """
    #
    #     """
    #     Cette méthode dessine une carte à partir d'un fichier JSON.
    #     Elle vérifie d'abord si le dossier et le fichier spécifiés existent.
    #     Si ce n'est pas le cas, elle affiche un message d'erreur et quitte
    #     le programme. Ensuite, elle lit les données du fichier JSON et les
    #     dessine sur le canvas.
    #
    #     - Dessine les tiles blanches et bleues.
    #     - Dessine la tile de sortie (classes/Tiles/Exit.py)
    #     - Affiche un fichier png qui represente une dalle.
    #     """
    #
    #     folder_path = os.path.dirname(file_path)
    #
    #     if not os.path.exists(folder_path):
    #         print("")
    #         print(f"The folder '{folder_path}' does not exist.")
    #         print("14101: Exit program")
    #
    #         pygame.quit()
    #         sys.exit()
    #
    #     if not os.path.exists(file_path):
    #         print("")
    #         print(f"The file '{file_path}' does not exist.")
    #         print("14050: Exit program")
    #
    #         pygame.quit()
    #         sys.exit()
    #
    #     with open(file_path, 'r') as file:
    #         data = json.load(file)
    #
    #     #
    #     self.total_tiles_array = data["total_tiles_array"]
    #
    #     for tile in self.total_tiles_array:
    #         x = tile['x']
    #         y = tile['y']
    #         w = tile['w']
    #         h = tile['h']
    #         if tile['color'] == 'white':
    #             pygame.draw.rect(canvas, self.WHITE, pygame.Rect(x, y, w, h))
    #         elif tile['color'] == 'blue':
    #             pygame.draw.rect(canvas, self.BLUE, pygame.Rect(x, y, w, h))
    #
    #         # [REPERE 7 - 2]
    #         # Affiche le fichier .png de la dalle.
    #         # IL n'a y a pas de preload de l'image ce qui entraine
    #         # 1 ralentissement
    #         # Check if there's a 'image_path' key for the tile
    #         if 'dalle_png_path' in tile and os.path.exists(tile['dalle_png_path']):
    #             image = pygame.image.load(tile['dalle_png_path'])
    #             # Rescale the image if it doesn't match the tile's dimensions
    #             if image.get_width() != w or image.get_height() != h:
    #                 image = pygame.transform.scale(image, (w, h))
    #             canvas.blit(image, (x, y))
    #
    #     # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #     # definir des tiles particulieres
    #
    #     # tile sortie qui permet de passer au prochain stair
    #     # Check if "exit_tile" is in "data" variable
    #     if "exit_tile" in data:
    #         # Extract 'x' and 'y' from JSON
    #         x = data['exit_tile']['x']
    #         y = data['exit_tile']['y']
    #
    #         # Create a Sortie instance
    #         sortie = Exit((x, y))
    #
    #         # Draw sortie
    #         sortie.draw()
    #         canvas.blit(sortie.surface, sortie.position)
    #     else:
    #         print("")
    #         print("no exit_tile found in stair json file")
    #         print("13451: Exit program")
    #
    #         pygame.quit()
    #         sys.exit()
    #
    #     # tile entry qui permet de revenir au précédent stair
    #     # Check if "entry_tile" is in the data
    #     if "entry_tile" in data:
    #         # Extract 'x' and 'y' from JSON
    #         x = data['entry_tile']['x']
    #         y = data['entry_tile']['y']
    #
    #         # Create a Entree instance
    #         entree = Entry((x, y))
    #
    #         # Draw entree
    #         entree.draw()
    #         canvas.blit(entree.surface, entree.position)
    #     else:
    #         print("")
    #         print("no entry_tile found in stair json file")
    #         print("13452: Exit program")
    #
    #         pygame.quit()
    #         sys.exit()
    #     # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # =========================================================================

    # @staticmethod
    # def load_image(path: str,
    #                size: tuple) -> ImageTk.PhotoImage:
    #     """
    #     Load and resize an image.
    #
    #     Parameters:
    #         path (str): Path to the image file.
    #         size (tuple): Desired size of the image.
    #
    #     Returns:
    #         ImageTk.PhotoImage: The resized image.
    #     """
    #     image = Image.open(path)
    #     image_resized = image.resize(size)
    #     photo = ImageTk.PhotoImage(image_resized)
    #     return photo

    # =========================================================================

    @staticmethod
    def get_key_value_from_json(file_path: str,
                                key: str) -> Optional[Any]:
        """
        Lit un fichier json et en extrait toutes les valeurs
        comprises ds la clé spécifiée.

        usage:
            file_path = "monoplayer/save/stairs_json/stair_10.json"
            key = "attributes_rooms_array"

            value = Utilitaires.get_key_value_from_json(file_path, key)

            print(value)
        """

        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get(key, None)

    # =========================================================================

    @staticmethod
    def list_files(directory: str) -> List[str]:
        """
        Cette méthode renvoie une liste des fichiers dans un répertoire.

        Paramètre:
        - directory: Le chemin du répertoire dont lister les fichiers.

        Renvoie une liste des noms des fichiers dans le répertoire,
        triés par la partie numérique de leur nom.
        """

        # Marquer le début de la méthode
        Utilitaires01.log_entry_message(logger,
                                        "info",
                                        "classes/utilitaires/utilitaires_01.py",
                                        "method: list_files()")

        file_paths = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                # Ignore directories, only consider files
                if os.path.isfile(os.path.join(root, file)):
                    # Extract the filename without path
                    filename = os.path.basename(file)
                    file_paths.append(filename)

        ordered_file_paths = sorted(file_paths,
                                    key=Utilitaires01.sort_by_numeric_part)

        # Marquer la fin de la méthode
        Utilitaires01.log_exit_message(logger,
                                       "info",
                                       "classes/utilitaires/utilitaires_01.py",
                                       "method: list_files()")

        return ordered_file_paths

    # =========================================================================

    @staticmethod
    def sort_by_numeric_part(filename: str) -> int:
        """
        Cette méthode extrait la partie numérique d'un nom de
        fichier et la renvoie.

        Paramètre:
        - filename: Le nom de fichier à partir duquel extraire
        la partie numérique.

        Renvoie la partie numérique du nom de fichier en tant qu'entier.
        """

        # Marquer le début de la méthode
        Utilitaires01.log_entry_message(logger,
                                        "info",
                                        "classes/utilitaires/utilitaires_01.py",
                                        "method: sort_by_numeric_part()")

        # Extract the numeric part from the file name
        numeric_part = int(filename.split("_")[1].split(".")[0])

        # Marquer la fin de la méthode
        Utilitaires01.log_exit_message(logger,
                                       "info",
                                       "classes/utilitaires/utilitaires_01.py",
                                       "method: sort_by_numeric_part()")

        return numeric_part

    # =========================================================================

    # @staticmethod
    # def update_json_file_player(self,
    #                             key,
    #                             new_value) -> None:
    #     """
    #     Met à jour une clé dans le fichier "save_player.json"
    #     avec une nouvelle valeur.
    #
    #     :param key: La clé à mettre à jour.
    #     :param new_value: La nouvelle valeur à définir.
    #
    #     Cette méthode met à jour une clé dans le fichier "player.json" avec
    #     une nouvelle valeur. Elle vérifie d'abord si la clé existe dans le
    #     fichier. Si c'est le cas, elle met à jour la valeur de la clé et
    #     sauvegarde le fichier. Si la clé n'existe pas, elle affiche un message
    #     indiquant que la clé n'existe pas.
    #     """
    #
    #     # Lire le fichier 'save_player.json'
    #     with open('monoplayer/save/save_player.json', 'r') as file:
    #         data = json.load(file)
    #
    #     # Vérifier si la clé existe
    #     if key in data:
    #         # Mettre à jour la valeur de la clé
    #         data[key] = new_value
    #
    #         # Réécrire le fichier 'save_player.json' avec la nouvelle valeur
    #         with open('monoplayer/save/save_player.json', 'w') as file:
    #             json.dump(data,
    #                       file,
    #                       indent=4)
    #             # print(f"'{key}' a été mis à jour avec la nouvelle valeur : {new_value}")
    #     else:
    #         print(f"La clé '{key}' n'existe pas dans 'save_player.json'.")
    #         print("On quitte le programme")
    #         pygame.quit()
    #         sys.exit()

    # =========================================================================

    # @staticmethod
    # def update_json_file_player_multiple_keys(key_value_pairs: dict) -> None:
    #     """
    #     Met à jour toutes clés dans le fichier "save_player.json"
    #     avec de nouvelles valeurs.
    #
    #     :param key_value_pairs: Dictionnaire contenant les clés à mettre
    #     à jour et leurs nouvelles valeurs.
    #
    #     Usage:
    #         Utilitaires01.update_multiple_keys(
    #                 {'key1': 'new_value1',
    #                  'key2': 'new_value2'}
    #                 )
    #     """
    #
    #     # Lire le fichier 'save_player.json'
    #     with open('monoplayer/save/save_player.json', 'r') as file:
    #         data = json.load(file)
    #
    #     updated_keys = []
    #     missing_keys = []
    #
    #     for key, new_value in key_value_pairs.items():
    #         # Vérifier si la clé existe
    #         if key in data:
    #             # Mettre à jour la valeur de la clé
    #             data[key] = new_value
    #             updated_keys.append(key)
    #         else:
    #             missing_keys.append(key)
    #
    #     # Réécrire le fichier 'save_player.json' avec les nouvelles valeurs
    #     with open('monoplayer/save/save_player.json', 'w') as file:
    #         json.dump(data,
    #                   file,
    #                   indent=4)
    #
    #     # Print update summary
    #     if updated_keys:
    #         # print(f"Les clés suivantes ont été mises à jour: {', '.join(updated_keys)}")
    #         pass
    #     if missing_keys:
    #         # print(f"Les clés suivantes n'existent pas: {', '.join(missing_keys)}")
    #
    #         pygame.quit()
    #         sys.exit()

    # =========================================================================

    """
    def exit_and_run_script(script_name):
        print(f"Exécution du script : {script_name}")
        self.running = False
        pygame.quit()

        python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
        subprocess.run([python_version, script_name], check=True)

        sys.exit()
    """

    # =========================================================================

    """
    @staticmethod
    def fov_implementation(transparent, player_pos, FOV_RADIUS):
        return tcod.map.compute_fov(
            transparency=transparent,
            pov=(player_pos[1], player_pos[0]),
            radius=FOV_RADIUS,
            light_walls=True,
            algorithm=0
        )
    """

    # =========================================================================

    @staticmethod
    def generate_map_using_DungeonFileGenerator(unique_id: int) -> None:
        """
        Permet de générer un donjon dans un fichier texte avec des
        caracteres ASCII: "#" pour les mûrs et "." pour les tiles.
        bsp02 utilisé.
        Les fichiers générés sont au format txt.
        """

        # Marquer le début de la méthode
        Utilitaires01.log_entry_message(logger,
                                        "info",
                                        "classes/utilitaires/utilitaires_01.py",
                                        "method: generate_map_using_DungeonFileGenerator()")

        # print("carte generee avec bsp02")
        # print("adresse:")
        # print("https://github.com/fsd66/py-dungeon")

        file_generator = DungeonFileGenerator()
        file_generator.generate_map_file(unique_id)

        # Marquer la fin de la méthode
        Utilitaires01.log_exit_message(logger,
                                       "info",
                                       "classes/utilitaires/utilitaires_01.py",
                                       "method: generate_map_using_DungeonFileGenerator()")

    # =========================================================================

    @staticmethod
    def generate_map_using_GameMap(grid_width: int,
                                   grid_height: int,
                                   unique_id: int) -> None:
        """
        Permet de générer un donjon dans un fichier texte avec des
        caracteres ASCII: "#" pour les murs et "." pour les tiles.
        bsp01 utilisé.
        Les fichiers générés sont au format txt.
        Les fichiers générés sont stockés dans le repertoire: "temp_txt_files".

        Permet de générer un donjon dans un fichier texte avec des
        caractères ASCII.
        Utilise "bsp01" pour la génération du donjon.
        Les fichiers sont au format txt et sont stockés dans le répertoire
        "temp_txt_files".

        Parameters:
        grid_width (int): La largeur de la grille sur laquelle
        le donjon sera généré.
        grid_height (int): La hauteur de la grille sur laquelle
        le donjon sera généré.
        unique_id (Any): Un identifiant unique pour la carte générée.

        Returns:
        None

        Side Effects:
        Génère un fichier texte représentant un donjon et le sauvegarde dans
        le répertoire "temp_txt_files".

        Exceptions:
        FileExistsError: Si le répertoire "temp_txt_files" existe déjà.
        """

        # Marquer le début de la méthode
        Utilitaires01.log_entry_message(logger,
                                        "info",
                                        "classes/utilitaires/utilitaires_01.py",
                                        "method: generate_map_using_GameMap()")

        # Obtention de la date et l'heure actuelles
        current_time = datetime.now()

        # Formatage de la date et l'heure
        formatted_time = current_time.strftime("%Y_%m_%d_%H_%M_%S")

        # Création du nom de fichier
        # NE FAUT IL PAS AJOUTER UN BLO TRY
        file_name = f"{formatted_time}_{unique_id}.txt"

        # Nom du dossier qui va contenir les fichiers txt temporaires.
        folder_name = "temp_txt_files/"

        # Chemin complet vers le fichier
        full_file_path = os.path.join(folder_name, file_name)

        #
        if os.path.exists(folder_name) and os.path.isdir(folder_name):
            logger.info(
                "==============================================================")
            logger.info("File: classes/utilitaires/utilitaires_01.py")
            logger.info("Méthode: generate_map_using_GameMap()")
            logger.info("'temp_txt_files' path exists")
        else:
            logger.info(
                "==============================================================")
            logger.info("File: classes/utilitaires/utilitaires_01.py")
            logger.info("Méthode: generate_map_using_GameMap()")
            logger.info("temp_txt_files does not exist")
            logger.info("We need to create it")

            try:
                os.mkdir(folder_name)
            except FileExistsError:
                logger.info(
                    "==============================================================")
                logger.info("Fichier: classes/utilitaires/utilitaires_01.py")
                logger.info("Méthode: generate_map_using_GameMap()")
                logger.info(f"Le répertoire {folder_name} existe déjà.")

        # logger.info("==============================================================")
        # logger.info("carte generee avec bsp01")
        # logger.info("adresse:")
        # logger.info("???")

        game_map = GameMap(width=grid_width, height=grid_height)
        game_map.make_map(max_rooms=30, room_min_size=6, room_max_size=10)
        game_map.save_map_to_file(full_file_path)

        # Les donjons crées ici sont tous forcément accessibles.
        # C'est une des particularité du bsp01
        print(f"Le donjon crée avec le bsp01: {unique_id} est accessible!")

        # Marquer la fin de la méthode
        Utilitaires01.log_exit_message(logger,
                                       "info",
                                       "classes/utilitaires/utilitaires_01.py",
                                       "method: generate_map_using_GameMap()")

    # =========================================================================

    @ staticmethod
    def random_map_generation(grid_width: int,
                              grid_height: int,
                              unique_id: int) -> None:
        """
        Fais un choix aléatoire pr utiliser bsp01 ou bsp02
        en vue de generer un donjon aléatoire et l'ecrire dans un
        fichier texte.

        Fait un choix aléatoire entre différentes méthodes de génération
        de carte pour créer un donjon aléatoire et l'écrire dans
        un fichier texte.

        Parameters:
        grid_width (int): La largeur de la grille sur laquelle le
        donjon sera généré.
        grid_height (int): La hauteur de la grille sur laquelle le
        donjon sera généré.
        unique_id (int): Un identifiant unique pour la carte générée.

        Returns:
        None

        Side Effects:
        Génère un donjon aléatoire et l'écrit dans un fichier texte.

        Exceptions:
        N/A
        """

        # Marquer le début de la méthode
        Utilitaires01.log_entry_message(logger,
                                        "info",
                                        "classes/utilitaires/utilitaires_01.py",
                                        "method: random_map_generation()")

        map_generation_methods = [
            # bsp01
            lambda: Utilitaires01.generate_map_using_GameMap(
                grid_width, grid_height, unique_id),
            # bsp02
            lambda: Utilitaires01.generate_map_using_DungeonFileGenerator(
                unique_id)
        ]

        #
        chosen_method = random.choice(map_generation_methods)

        # DEMANDER CE QU'EST CETTE SYNTAXE
        chosen_method()

        # Marquer la fin de la méthode
        Utilitaires01.log_exit_message(logger,
                                       "info",
                                       "classes/utilitaires/utilitaires_01.py",
                                       "method: random_map_generation()")

    # =========================================================================

    """
    @staticmethod
    def draw_walls(game_map, transparent, walkable):
        for y, row in enumerate(game_map):
            for x, cell in enumerate(row):
                if cell == "#":
                    transparent[y, x] = False
                    walkable[y, x] = False

    # =========================================================================

    @staticmethod
    def load_map_from_file(filename):
        with open(filename, 'r') as file:
            map_data = file.readlines()
        return [list(line.strip()) for line in map_data]
    """

    # =========================================================================

    @staticmethod
    def replace_adjacent_characters(file_path: str) -> None:
        """
        Ouvre le fichier txt descriptif du donjon.
        Remplace ts les caracteres "#" qui sont adjacents
        aux caractères "." par des caractères "?".
        Cela permettra de définir les murs du donjon généré.

        Ouvre le fichier txt descriptif du donjon et remplace
        tous les caractères "#" 
        adjacents aux caractères "." par des caractères "?".

        Parameters:
        file_path (str): Le chemin complet du fichier txt contenant
        la description du donjon.

        Returns:
        None

        Side Effects:
        Modifie le fichier txt en place en remplaçant certains caractères
        "#" par "?".

        Exceptions:
        OSError: Levée si des problèmes se produisent lors de l'ouverture
        ou de la manipulation du fichier.
        """

        # Marquer le début de la méthode
        Utilitaires01.log_entry_message(logger,
                                        "info",
                                        "classes/utilitaires/utilitaires_01.py",
                                        "method: replace_adjacent_characters()")

        # A REMPLACER
        with open(file_path, 'r') as f:
            lines = f.read().splitlines()
        # print(f"Original lines: {lines}")

        new_lines = []
        total_lines = len(lines)
        if total_lines == 0:
            return

        # Trouver la première ligne non vide
        line_length = 0
        for line in lines:
            if line:
                line_length = len(line)
                break

        if line_length == 0:
            return  # Tout le fichier est vide

        for y in range(total_lines):
            new_line = ''
            for x in range(line_length):
                # Ajouté pour éviter l'erreur IndexError
                if y < len(lines) and x < len(lines[y]):
                    if lines[y][x] == '#':
                        adjacent_dots = False
                        for dx in [-1, 0, 1]:
                            for dy in [-1, 0, 1]:
                                nx, ny = x + dx, y + dy
                                if 0 <= nx < line_length and 0 <= ny < total_lines:
                                    if ny < len(lines) and nx < len(lines[ny]) and lines[ny][nx] == '.':
                                        adjacent_dots = True
                                        break
                            if adjacent_dots:
                                break
                        new_line += '?' if adjacent_dots else '#'
                    else:
                        new_line += lines[y][x]
            new_lines.append(new_line)
        # print(f"New lines: {new_lines}")

        # A REMPLACER
        with open(file_path, 'w') as f:
            for line in new_lines:
                f.write(line + "\n")

        # Marquer la fin de la méthode
        Utilitaires01.log_exit_message(logger,
                                       "info",
                                       "classes/utilitaires/utilitaires_01.py",
                                       "method: replace_adjacent_characters()")

    # =========================================================================

    @staticmethod
    def handle_file_operations(file_path: str,
                               callback: Callable[[IO], None]) -> None:
        """
        Gère les opérations sur un fichier en utilisant un callback.

        Parameters:
        file_path (str): Le chemin complet du fichier à manipuler.
        callback (Callable[[IO], None]): La fonction de rappel à exécuter
        avec le fichier ouvert.

        Returns:
        None

        Exceptions:
        IOError: Levée lorsque des erreurs d'E/S se produisent.
        Exception: Levée pour toutes les autres exceptions.
        """

        # Marquer le début de la méthode
        Utilitaires01.log_entry_message(logger,
                                        "info",
                                        "classes/utilitaires/utilitaires_01.py",
                                        "method: handle_file_operations()")

        try:
            # A REMPLACER
            with open(file_path, "r+") as f:
                callback(f)
        except IOError as error:
            logger.error(
                "============================================================")
            logger.error("File: classes/utilitaires/utilitaires_01.py")
            logger.error("Méthode: handle_file_operations()")
            logger.error(f"Erreur d'IO: {error}")
        except Exception as error:
            logger.error(
                "============================================================")
            logger.error("File: classes/utilitaires/utilitaires_01.py")
            logger.error("Méthode: handle_file_operations()")
            logger.error(f"Une autre erreur s'est produite: {error}")

        # Marquer la fin de la méthode
        Utilitaires01.log_exit_message(logger,
                                       "info",
                                       "classes/utilitaires/utilitaires_01.py",
                                       "method: handle_file_operations()")
