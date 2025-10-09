import platform

SCROLL_PAUSE_TIME = 0.5
MAX_SCROLL_ATTEMPTS = 10
IMPLICIT_WAIT = 1
PAGE_LOAD_TIMEOUT = 8

# Chrome binary path (auto-detected on Windows, configurable for Linux)
if platform.system() == 'Windows':
    CHROME_BINARY_PATH = None  # Auto-detect on Windows
else:
    CHROME_BINARY_PATH = '/opt/google/chrome/chrome'

# Performance settings
MAX_PLACES_PER_CITY = None  # No limit
EXTRACT_WAIT_TIME = 0.3
