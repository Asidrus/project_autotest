from dotenv import load_dotenv
import os

load_dotenv()

"""
config for autotest default

BROWSER: "Chrome" (default) | "Firefox" | "Edge"
REMOTE: "true" (default) | "false"
INTERACTIVE_MODE: "true" | "false" (default)

WEBDRIVER_PATH: "/webdriver/path" | None (default)
WEBDRIVER_IP: "127.0.0.1" (default)
WEBDRIVER_PORT: "4444" (default)
"""
BROWSER = os.getenv("BROWSER", "Chrome")
REMOTE = not os.getenv("REMOTE", "true") == "false"
INTERACTIVE_MODE = not os.getenv("INTERACTIVE_MODE", "false") == "false"

WEBDRIVER_PATH = os.getenv("WEBDRIVER_PATH", None)
WEBDRIVER_IP = os.getenv("WEBDRIVER_IP", "127.0.0.1")
WEBDRIVER_PORT = os.getenv("WEBDRIVER_PORT", "4444")

""" """
WEBSITE_IP = os.getenv("WEBSITE_IP")
WEBSITE_PORT = os.getenv("WEBSITE_PORT")
WEBSITE_URL = f"http://{WEBSITE_IP}:{WEBSITE_PORT}"





