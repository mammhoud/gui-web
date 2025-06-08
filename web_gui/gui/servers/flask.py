from .base import BaseServer


class FlaskServer(BaseServer):
    def run(self):
        try:
            import waitress

            waitress.serve(self.app, port=self.port)
        except ImportError:
            self.app.run(port=self.port)


class FlaskSocketIOServer(BaseServer):
    def run(self):
        self.socketio.run(self.app, port=self.port)
