from pathlib import Path
from watchdog.events import FileSystemEventHandler
from services.image_service import copiar_imagem
from services.logging_service import get_app_logger

logger = get_app_logger()

class Handler(FileSystemEventHandler):
	def on_created(self, event):
		if not event.is_directory:
			logger.info(f"Novo arquivo detectado: {event.src_path}")
			copiar_imagem(Path(event.src_path))
