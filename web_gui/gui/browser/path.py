from . import OPERATING_SYSTEM, DEFAULT_BROWSER
from . import windows_browser_paths, linux_browser_paths, mac_browser_paths
import os


class BrowserPathFinder:
    @staticmethod
    def get_browser_path():
        dispatch = {
            "windows": windows_browser_paths,
            "linux": linux_browser_paths,
            "darwin": mac_browser_paths,
        }

        browser_paths = dispatch.get(OPERATING_SYSTEM, [])
        for path in browser_paths:
            if os.path.exists(path):
                if DEFAULT_BROWSER in path:
                    return path
        return next((p for p in browser_paths if os.path.exists(p)), None)
