import logging

logging.basicConfig(
    filename="app.log",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(process)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

a = 5
b = 0

try:
    c = a / b
except Exception:
    logging.exception("Exception occurred")
