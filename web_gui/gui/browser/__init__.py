
import webbrowser
import platform

# WEBGUI_USED_PORT = None
# WEBGUI_BROWSER_PROCESS = None

DEFAULT_BROWSER = webbrowser.get().name
OPERATING_SYSTEM = platform.system().lower()
PY = "python3" if OPERATING_SYSTEM in ["linux", "darwin"] else "python"


linux_browser_paths = [
    r"/usr/bin/google-chrome",
    r"/usr/bin/microsoft-edge",
    r"/usr/bin/brave-browser",
    r"/usr/bin/chromium",
    # Web browsers installed via flatpak portals
    r"/run/host/usr/bin/google-chrome",
    r"/run/host/usr/bin/microsoft-edge",
    r"/run/host/usr/bin/brave-browser",
    r"/run/host/usr/bin/chromium",
    # Web browsers installed via snap
    r"/snap/bin/chromium",
    r"/snap/bin/brave-browser",
    r"/snap/bin/google-chrome",
    r"/snap/bin/microsoft-edge",
]

mac_browser_paths = [
    r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    r"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    r"/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]

windows_browser_paths = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
]
