import logging

# === Твой основной логгер Pixora ===
logger = logging.getLogger("pixora")
logger.setLevel(logging.INFO)

pixora_handler = logging.StreamHandler()
pixora_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
pixora_handler.setFormatter(pixora_formatter)
logger.addHandler(pixora_handler)

# === Aiogram события (например: Update is handled...) ===
aiogram_event_logger = logging.getLogger("aiogram.event")
aiogram_event_logger.setLevel(logging.INFO)
aiogram_event_logger.addHandler(pixora_handler)