import tornado.ioloop
import tornado.web
import tornado.websocket

from logger_config_serveur_tornado import configure_logger_serveur_tornado
# méthodes du logger (debug(), info(), warning(), error(), critical())
lst = configure_logger_serveur_tornado(__name__, 'serveur_tornado.log')


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    # Variables de classe.

    # Le set des clients qui vont se connecter au serveur.
    clients = set()

    # stocker le prochain ID disponible
    next_ws_id = 1

    next_message_id = 1  # stocker le prochain ID de message disponible

    def __init__(self, *args, **kwargs):
        super(WebSocketHandler, self).__init__(*args, **kwargs)

        # Attribue un ID unique à cette instance
        self.ws_id = WebSocketHandler.next_ws_id

        # Incrémente la variable de classe pour le prochain ID
        WebSocketHandler.next_ws_id += 1

    # ========================================================================

    async def open(self):
        client_ip = self.request.remote_ip
        server_ip = self.request.host.split(':')[0]

        self.clients.add(self)

        lst.info("===========================================================")
        lst.info("> serveur_tornado.py")
        lst.info(f"Server IP: {server_ip}")
        lst.info(f"Client IP: {client_ip}")
        lst.info(
            f"Ouverture d'1 WebSocket. ID: {self.ws_id}. Connex° d'1 client.")
        lst.info("")

        print("===========================================================")
        print("> serveur_tornado.py")
        print(f"Server IP: {server_ip}")
        print(f"Client IP: {client_ip}")
        print(
            f"Ouverture d'1 WebSocket. ID: {self.ws_id}. Connex° d'1 client.")

        print("")

    # ========================================================================

    async def on_message(self, message):
        client_ip = self.request.remote_ip
        server_ip = self.request.host.split(':')[0]

        # Attribue un ID unique à ce message
        message_id = WebSocketHandler.next_message_id

        # Envoie un message en reponse.
        try:
            await self.write_message(f"""> serveur_tornado.py:\n
                                        Récept° d'1 message, redistribut°.""")
        except Exception as e:
            lst.error(f"Erreur lors de l'envoi du message: {e}")
            print(f"Erreur lors de l'envoi du message: {e}")

        # Envoie à ts les clients sauf au client expediteur
        # le message reçu.
        for client in self.clients:
            if client != self:
                try:
                    await client.write_message(message)
                except Exception as e:
                    lst.error(
                        f"Erreur lors de l'envoi du message au client {client.ws_id}: {e}")
                    print(
                        f"Erreur lors de l'envoi du message au client {client.ws_id}: {e}")

        # logs
        lst.info("> serveur_tornado.py")
        lst.info(f"Server IP: {server_ip}")
        lst.info(f"Expediteur: {client_ip}")
        lst.info(f"WebSocket ID: {self.ws_id}")
        lst.info(f"Récept° du message: {message_id}.")
        lst.info(f"{message}")

        # Imprime le message reçu depuis screen06_game.py.
        print("> serveur_tornado.py")
        print(f"Server IP: {server_ip}")
        print(f"Expediteur: {client_ip}")
        print(f"WebSocket ID: {self.ws_id}")
        print(f"Récept° du message: {message_id}.")
        print(f"{message}")

# Incrémente la variable pour le prochain ID
        WebSocketHandler.next_message_id += 1

    # ========================================================================

    def on_close(self):
        client_ip = self.request.remote_ip
        server_ip = self.request.host.split(':')[0]

        try:
            # Retire ce client du set des clients.
            self.clients.remove(self)
        except Exception as e:
            lst.error(f"Erreur lors de la suppression du client : {e}")
            print(f"Erreur lors de la suppression du client : {e}")

        print("> serveur_tornado.py")
        print(f"Server IP: {server_ip}")
        print(f"Client IP: {client_ip}")
        print(
            f"Fermeture WebSocket: déconnex° du client. WebSocket ID: {self.ws_id}")

        lst.info("> serveur_tornado.py")
        lst.info(f"Server IP: {server_ip}")
        lst.info(f"Client IP: {client_ip}")
        lst.info(
            f"Fermeture WebSocket: déconnex° du client. WebSocket ID: {self.ws_id}")

    # ========================================================================


def make_app():
    return tornado.web.Application([
        (r"/websocket", WebSocketHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)

    print("Server is running and listening (port 8888)...")

    lst.info("Server is running and listening (port 8888)...")

    try:

        #
        tornado.ioloop.IOLoop.current().start()

    # Capture du signal d'interruption manuelle
    except KeyboardInterrupt:

        # Message quand le serveur s'arrête
        print("Shutting down server...")

        lst.info("Shutting down server...")

        tornado.ioloop.IOLoop.current().stop()
