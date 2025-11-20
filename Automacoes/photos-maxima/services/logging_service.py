import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from config import APP_LOG_PATH, PHOTOS_LOG_PATH, LOG_MAX_BYTES, LOG_BACKUP_COUNT

# Adiciona nível SUCCESS customizado
SUCCESS_LEVEL = 25
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")

def success(self, message, *args, **kwargs):
	if self.isEnabledFor(SUCCESS_LEVEL):
		self._log(SUCCESS_LEVEL, message, args, **kwargs)

logging.Logger.success = success

_configured = False

def _build_rotating_handler(log_path):
	handler = RotatingFileHandler(log_path, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT, encoding="utf-8")
	formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
	handler.setFormatter(formatter)
	return handler



def setup_loggers():
	global _configured
	if _configured:
		return

	root_logger = logging.getLogger()
	root_logger.setLevel(logging.INFO)

	# File handler (app.log)
	has_file_handler = any(isinstance(h, RotatingFileHandler) for h in root_logger.handlers)
	if not has_file_handler:
		root_logger.addHandler(_build_rotating_handler(APP_LOG_PATH))

	# Console handler (stdout)
	has_console_handler = any(isinstance(h, StreamHandler) for h in root_logger.handlers)
	if not has_console_handler:
		console_handler = StreamHandler()
		console_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
		root_logger.addHandler(console_handler)

	photos_logger = logging.getLogger("photos")
	if not photos_logger.handlers:
		photos_logger.setLevel(logging.INFO)
		photos_logger.addHandler(_build_rotating_handler(PHOTOS_LOG_PATH))
		photos_logger.propagate = False

	_configured = True

def get_app_logger():
	setup_loggers()
	return logging.getLogger("app")

def get_photos_logger():
	setup_loggers()
	return logging.getLogger("photos")

