import multiprocessing
import os
import shutil
import sys
import tempfile
from threading import Thread
import uuid
from .browser.main import BrowserManager
from .actions import Controller
from .main import WebServerManager
import structlog

log = structlog.get_logger()


from .browser import OPERATING_SYSTEM


class WebGUIApp:
    def __init__(
        self,
        app,
        server_type="django",
        port=None,
        width=None,
        height=None,
        fullscreen=True,
        app_mode=True,
        socketio=None,
        on_startup=None,
        on_shutdown=None,
        browser_path=None,
        extra_flags=None,
        profile_dir=None,
        exit_after=None,
    ):
        self.app = app
        self.server_type = server_type
        self.port = port or Controller.get_free_port()
        self.width = width
        self.height = height
        self.fullscreen = fullscreen
        self.app_mode = app_mode
        self.socketio = socketio
        self.on_startup = on_startup
        self.on_shutdown = on_shutdown
        self.browser_path = browser_path
        self.extra_flags = extra_flags
        self.server_type = server_type
        self.exit_after = exit_after or 15
        self.profile_dir = profile_dir or os.path.join(
            tempfile.gettempdir(), "WEBGUI_" + uuid.uuid4().hex
        )
        self.url = f"http://127.0.0.1:{self.port}"

        self.browser = BrowserManager(
            self.url,
            self.profile_dir,
            width=self.width,
            height=self.height,
            extra_flags=self.extra_flags,
            fullscreen=self.fullscreen,
            app_mode=self.app_mode,
            browser_path=self.browser_path,
            exit_after=self.exit_after,  # ⏱️ مهم: تمرير timeout
            on_close=self.shutdown,  # ✅ هنا الميزة الأساسية
        )
        self.server = WebServerManager(
            self.server_type, self.app, self.port, self.socketio
        )

    def run(self):
        if self.on_startup:
            self.on_startup()

        if OPERATING_SYSTEM == "darwin":
            multiprocessing.set_start_method("fork")

        self.server_process = multiprocessing.Process(target=self.server.start)
        self.browser_thread = Thread(target=self.browser.start)

        try:
            self.server_process.start()
            # log.info(f"[INFO] Server started with PID: {self.server_process.pid}")

            self.browser_thread.start()

            self.server_process.join()
            self.browser_thread.join()

        except KeyboardInterrupt:
            log.warning("\n[INFO] KeyboardInterrupt detected. Shutting down.")
            self.shutdown()

        except Exception as e:
            log.warning(f"[ERROR] Unexpected error: {e}")
            self.shutdown()

    def shutdown(self, timeout=None):
        if not timeout:
            timeout = self.exit_after
        log.info("[SHUTDOWN] Cleaning up.")

        if self.on_shutdown:
            log.info("[SHUTDOWN] on_shutdown callback (before cleanup).")

        if hasattr(self, "browser") and self.browser:
            try:
                self.browser.terminate()
                log.info("[SHUTDOWN] Browser process terminated.")
            except Exception as e:
                log.warning(f"[WARN] Failed to terminate browser: {e}")

        if hasattr(self, "server_process") and self.server_process.is_alive():
            Controller.shutdown(self.server_process.pid, timeout=self.exit_after)

            # if self.server_process.is_alive():
            #     try:
            #         self.server_process.terminate()
            #         self.server_process.join(timeout=self.exit_after)
            #     except Exception as e:
            #         log.warning(
            #             f"[WARN] Server process (PID={self.server_process.pid}) did not terminate cleanly.\n{str(e)}"
            #         )
            # else:
            #     log.info("[SHUTDOWN] Server process terminated.")

        shutil.rmtree(self.profile_dir, ignore_errors=True)
        Controller.kill_port(self.port)

        log.info("[SHUTDOWN] Shutdown complete.")
        sys.exit(0)
