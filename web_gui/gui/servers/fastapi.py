from .base import BaseServer


class FastAPIServer(BaseServer):
    def run(self):
        import uvicorn

        uvicorn.run(self.app, port=self.port)
