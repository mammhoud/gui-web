import subprocess
import structlog


from ..actions import Controller
from .path import BrowserPathFinder
from security import safe_command

log = structlog.get_logger()

class BrowserManager:
    def __init__(
        self,
        url: str,
        profile_dir: str,
        browser_path=None,
        fullscreen=True,
        width=None,
        height=None,
        extra_flags=None,
        app_mode=True,
        on_close=None,
        exit_after=None,
    ):
        self.url = url  # http://127.0.0.1:3003/admin
        self.profile_dir = profile_dir
        self.browser_path = browser_path or BrowserPathFinder.get_browser_path()
        self.fullscreen = fullscreen
        self.width = width
        self.height = height
        self.extra_flags = extra_flags or []
        self.app_mode = app_mode
        self.browser_process = None
        self.browser_pid = None
        self.on_close = on_close
        self.timeout = exit_after or 15

    def build_command(self):
        flags = [
            self.browser_path,
            f"--user-data-dir={self.profile_dir}",
            "--new-window",
            "--no-default-browser-check",
            "--allow-insecure-localhost",
            "--ignore-certificate-errors",
            "--no-first-run",
            "--disable-sync",
            # "--search-provider-logo-url=https://user-images.githubusercontent.com/1134620/154389398-b6b58a26-0089-40ff-9fc7-1f821f703952.svg",
            " --enable-logging",
            "--v=1",
            "--material-hybrid",
            "--memlog",
            "--enable-fast-unload",
            "--kiosk",
            "--kiosk-printing",  ## printer
            "--rtl",
        ]

        if self.width and self.height and self.app_mode:
            flags.append(f"--window-size={self.width},{self.height}")
        elif self.fullscreen:
            flags.append("--start-maximized")

        flags += self.extra_flags

        if self.app_mode:
            flags.append(f"--app={self.url}")
        else:
            flags += ["--guest", self.url]

        return flags

    def start(self):
        cmd = self.build_command()
        log.info("Launching browser:", cmd=" ".join(cmd))
        self.browser_process = safe_command.run(subprocess.Popen, cmd, stderr=subprocess.DEVNULL)
        self.browser_pid = self.browser_process.pid
        # log.info("Browser PID:", self.browser_pid)

        try:
            self.browser_process.wait()
        except KeyboardInterrupt:
            log.warning("[INFO] KeyboardInterrupt received. Terminating browser.")
            self.terminate()
        finally:
            log.info("[INFO] Closing -> Loading")
            if self.on_close:
                self.on_close(self.timeout)

    def terminate(self):
        if not self.browser_process:
            return

        log.info("[SHUTDOWN] Terminating browser process.")
        try:
            Controller.terminate(self.browser_process.pid)
        except Exception as e:
            log.warning("[ERROR] Failed to terminate browser process:", e)

        self.browser_process = None
        self.browser_pid = None
