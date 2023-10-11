import tornado.ioloop
import tornado.web
import tornado.websocket

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    async def open(self):
        client_ip = self.request.remote_ip
        server_ip = self.request.host.split(':')[0]
        print("WebSocket ouvert.")
        print(f"Client IP: {client_ip}")
        print(f"Server IP: {server_ip}")

    async def on_message(self, message):
        print(f"Message reçu: {message}")
        await self.write_message("Salut, je suis le sieur serveur.")

    def on_close(self):
        print("WebSocket fermé")

def make_app():
    return tornado.web.Application([
        (r"/websocket", WebSocketHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
