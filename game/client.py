# client.py

from datetime import datetime
import socket

from websocket import create_connection
from websocket import WebSocketTimeoutException
from websocket import WebSocketBadStatusException
from websocket import WebSocketConnectionClosedException
from websocket import WebSocketException

from classes.utilitaires.utilitaires_01 import Utilitaires01

from logger_config import configure_logger
# méthodes du logger (debug(), info(), warning(), error(), critical())
logger = configure_logger(__name__, 'logs/client.log')


class WebSocketClient:
    """
    WebSocketClient class for connecting, receiving and sending messages
    to a WebSocket server.
    """

    Utilitaires01.log_entry_message(logger,
                                    "debug",
                                    "client.py",
                                    "class: WebSocketClient")

    def __init__(self, target):
        """
        Initialize the WebSocketClient.

        :param target: The target WebSocket server to connect to.
        """

        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "client.py",
                                        "methode: def __init__()")

        self.target = target
        self.ws = None
        self.is_connected = False
        self.closed = False

        Utilitaires01.log_exit_message(logger,
                                       "debug",
                                       "client.py",
                                       "methode: def __init__()")

    # ========================================================================

    def get_local_ip_address(self):
        """
        Get the local IP address of the client.

        :return: Local IP address as a string.
        """

        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "client.py",
                                        "methode: def get_local_ip_address()")

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if sock.fileno() == -1:

            logger.error("File: client.py")
            logger.error("methode: get_local_ip_address()")
            logger.error(
                "Erreur 01 : le socket n'a pas été correctement initialisé.")

            return '127.0.0.1'

        try:
            sock.connect((self.target, 1))
            IP = sock.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            sock.close()
        return IP

    # ========================================================================

    def connect(self):
        """
        Connect to the WebSocket server and initialize the socket.

        :raises: WebSocketTimeoutException, WebSocketBadStatusException,
        WebSocketException
        :return: None
        """

        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "client.py",
                                        "methode: def connect()")

        try:
            self.ws = create_connection(f"ws://{self.target}:8888/websocket")
            self.is_connected = True
            client_ip = self.get_local_ip_address()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Reçu sur le serveur.
            self.ws.send(
                f"Depuis le fichier client.py: {current_time}, adresse IP: {client_ip}")
        except (WebSocketTimeoutException, WebSocketBadStatusException, WebSocketException) as e:

            logger.error("File: client.py")
            logger.error("Methode: connect()")
            logger.error(f"erreur 02 lors de la connex°: {e}")

            self.is_connected = False
        except Exception as e:

            logger.error("File: client.py")
            logger.error("Methode: connect()")
            logger.error(
                f"1 erreur (erreur 03) inattendue s'est produite: {e}")

            self.is_connected = False

    # ========================================================================

    def receive(self):
        """
        Receive a message from the WebSocket server.

        :raises: WebSocketConnectionClosedException, WebSocketTimeoutException,
                 WebSocketBadStatusException, WebSocketException
        :return: Message as a string if successful, None otherwise.
        """

        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "client.py",
                                        "methode: def receive()")

        if not self.is_connected:
            logger.error("File: client.py")
            logger.error("Méthode: receive()")
            logger.error("Erreur 04 : WebSocket non initialisé ou fermé.")

            self.ws.close()

        try:
            return self.ws.recv()
        except WebSocketConnectionClosedException:
            logger.warning("File: client.py")
            logger.warning("Méthode: receive()")
            logger.warning("La connexion WebSocket est fermée.")

            self.close()

        except (WebSocketTimeoutException, WebSocketBadStatusException, WebSocketException) as e:
            logger.warning("File: client.py")
            logger.warning("méthode: receive()")
            logger.warning(f"Erreur 05 lors de la réception du message: {e}")

            self.close()

        except Exception as e:
            logger.error("File: client.py")
            logger.error("Méthode: receive()")
            logger.error(
                f"Une erreur (erreur 06) inattendue s'est produite: {e}")

            self.close()

    # ========================================================================

    def listen(self):
        """
        Listen for messages from the WebSocket server in a loop.

        :raises: WebSocketConnectionClosedException, WebSocketTimeoutException,
                 WebSocketBadStatusException, WebSocketException
        :return: None
        """

        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "client.py",
                                        "methode: def listen()")

        while self.is_connected:
            try:
                message = self.ws.recv()

                logger.info("File:client.py")
                logger.info("Méthode: listen()")
                logger.info(f"Message reçu : {message}")

            except WebSocketConnectionClosedException:
                logger.warning("File: client.py")
                logger.warning("Méthode: listen()")
                logger.warning("La connexion WebSocket est fermée.")

                # Ferme la connx°.
                self.close()

                # Sort de la boucle
                break

            except (WebSocketTimeoutException, WebSocketBadStatusException, WebSocketException) as e:
                logger.error("File: client.py")
                logger.error("Méthode: listen()")
                logger.error(f"Erreur 07 lors de l'écoute: {e}")

                # Ferme la connex°
                self.close()

                # Sort de la boucle.
                break

            except Exception as e:
                logger.error("File: client.py")
                logger.error("Méthode: listen()")
                logger.error(
                    f"Une erreur (erreur 08) inattendue s'est produite: {e}")

                # Ferme la connex°
                self.close()

                # Sort de la boucle.
                break

    # ========================================================================

    def close(self):
        """
        Close the WebSocket connection.

        :return: None
        """

        Utilitaires01.log_entry_message(logger,
                                        "debug",
                                        "client.py",
                                        "methode: def close()")

        try:
            if self.ws:
                self.ws.close()
            self.is_connected = False
        except Exception as e:
            logger.error("file: client.py")
            logger.error("Methode: close()")
            logger.error(
                f"Erreur 09 lors de la fermeture de la connexion: {e}")
