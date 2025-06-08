class BaseServer:
    def __init__(self, app, port, socketio=None):
        self.app = app
        self.port = port
        self.socketio = socketio

    def get_kwargs(self):
        return {"app": self.app, "port": self.port}

    def run(self):
        raise NotImplementedError()
