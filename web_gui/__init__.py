import sys
import importlib
from .gui import WebGUIApp as web_app
from django.utils.timezone import datetime
from dynaconf import Dynaconf
import structlog

log = structlog.get_logger()

def main(*args, **kwargs):
    # --- Dynaconf Settings ---
    settings = Dynaconf(
        envvar_prefix="SETTINGS",
        environments=True,
        env="default",
        settings_files=["settings.yaml", ".secrets.yaml"],
    )

    # --- Callback ---
    def callbacks():
        log.info("server_shutdown", message="Shutting down server.")
        sys.exit(0)

    # --- Resolve APP as dotted path ---
    def resolve_app(app_path: str):
        module_path, attr = app_path.rsplit(".", 1)
        mod = importlib.import_module(module_path)
        return getattr(mod, attr)

    # --- Profile dir ---
    profile_dir = settings.get("PROFILE_DIR") or f"./.temp/{datetime.now().date()}"

    # --- Log Configuration ---
    log.info("launch_config", config=settings.as_dict())

    # --- Start GUI Web App ---
    obj = web_app(
        app=resolve_app(settings.get("APP")),
        port=settings.get("PORT"),
        width=settings.get("WIDTH"),
        height=settings.get("HEIGHT"),
        profile_dir=profile_dir,
        extra_flags=settings.get("EXTRA_FLAGS"),
        on_shutdown=callbacks,
        server_type=settings.get("SERVER_TYPE", "django"),
        exit_after=settings.get("EXIT_AFTER"),
        browser_path=settings.get("BROWSER_PATH"),
        fullscreen=settings.get("FULLSCREEN", True),
        app_mode=settings.get("APP_MODE", True),
        socketio=settings.get("SOCKETIO"),
        on_startup=settings.get("ON_STARTUP"),
    )

    log.info("server_starting", port=settings.get("PORT"))
    obj.run()

# CLI entry point
if __name__ == "__main__":
    main()
