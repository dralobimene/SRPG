# classes/utilitaires/utilitaires_02_reseau.py

from client import WebSocketClient

from logger_config import configure_logger
# méthodes du logger (debug(), info(), warning(), error(), critical())
logger = configure_logger(__name__, 'logs/utilitaires_02_reseau.log')


class Utilitaires02Reseau:
    """
        pydoc de Utilitaires02Reseau:

        NOTES:
            01:
                PAS DE def __init__() ???
    """

    @staticmethod
    def send_message(websocket_client: WebSocketClient, message):
        logger.info(">>> Fichier classes/utilitaires/utilitaires_02_reseau.py")
        logger.info("méthode: send_message()")

        if websocket_client:
            websocket_client.ws.send(message)

        logger.info("Fichier classes/utilitaires/utilitaires_02_reseau.py")
        logger.info("methode: send_message() <<<")
