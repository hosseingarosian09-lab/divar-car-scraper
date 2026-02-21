import shutil
import os
import sys
from typing import List

def _check_browser(unix_names: List[str], win_paths: List[str], mac_paths: List[str]) -> bool:
    # 1. Try PATH lookup (works on Linux, macOS if symlinked, and sometimes Windows)
    for name in unix_names:
        if shutil.which(name):
            return True
    # 2. OS-specific fallbacks
    if sys.platform.startswith('win'):
        for path in win_paths:
            if os.path.exists(path):
                return True
    elif sys.platform == 'darwin':  # macOS
        for path in mac_paths:
            if os.path.exists(path):
                return True

    return False

def is_chrome_installed() -> bool:
    names = ["google-chrome", "chrome", "chromium", "chromium-browser"]
    # Windows-specific paths
    win_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
    ]
    # macOS-specific .app bundles
    mac_paths = [
        "/Applications/Google Chrome.app",
        "/Applications/Chromium.app",
    ]
    return _check_browser(names, win_paths, mac_paths)

def is_firefox_installed() -> bool:
    names = ["firefox", "firefox-developer-edition", "firefox-nightly"]
    win_paths = [
        r"C:\Program Files\Mozilla Firefox\firefox.exe",
        r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
        os.path.expanduser(r"~\AppData\Local\Mozilla Firefox\firefox.exe"),
    ]
    mac_paths = [
        "/Applications/Firefox.app",
    ]
    return _check_browser(names, win_paths, mac_paths)

def is_edge_installed() -> bool:
    names = ["microsoft-edge", "edge", "microsoft-edge-dev", "microsoft-edge-beta", "microsoft-edge-canary"]
    win_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\Application\msedge.exe"),
    ]
    mac_paths = [
        "/Applications/Microsoft Edge.app",
    ]
    return _check_browser(names, win_paths, mac_paths)


# Test
print("Chrome installed:", is_chrome_installed())
print("Firefox installed:", is_firefox_installed())
print("Edge installed:", is_edge_installed())
