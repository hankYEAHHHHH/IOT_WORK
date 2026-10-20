"""Start native Wi-Fi before MicroPython compiles/loads the application."""
from startup import reserve_wifi

try:
    reserve_wifi()
except (OSError, MemoryError):
    # startup records the failure. main will stop without loading the app.
    pass
