from .base import BaseServer
import structlog

log = structlog.get_logger()


class DjangoServer(BaseServer):
    def run(self):
        from whitenoise import WhiteNoise  # type: ignore
        import waitress  # type: ignore

        if not self.app:
            raise ValueError("No WSGI application provided for Django server.")

        log.info(f"[DjangoServer] Serving on http://127.0.0.1:{self.port}")

        # Wrap Django app with WhiteNoise middleware for static file support
        wrapped_app = WhiteNoise(self.app)

        # Run the app with waitress
        waitress.serve(wrapped_app, threads=100, port=self.port)
