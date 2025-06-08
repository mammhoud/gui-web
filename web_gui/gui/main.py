from .servers import *  # noqa: F403


class WebServerManager:
    def __init__(self, server_type: str, app, port, socketio=None):
        server_map = {
            "flask": FlaskServer,  # noqa: F405
            "django": DjangoServer,  # noqa: F405
            "fastapi": FastAPIServer,  # noqa: F405
            "flask_socketio": FlaskSocketIOServer,  # noqa: F405
        }

        if server_type not in server_map:
            raise ValueError(f"Unsupported server type: {server_type}")

        self.server = server_map[server_type](app, port, socketio)

    def start(self):
        self.server.run()
