from pathlib import Path
import os
from dotenv import load_dotenv

# Carrega variáveis do .env (se existir)
load_dotenv()

EXTS = {
	".jpg", ".jpeg", ".png", ".gif", ".bmp",
	".tiff", ".tif", ".webp", ".heic", ".heif",
	".raw", ".cr2", ".nef", ".orf", ".sr2", ".ico"
}

BASE_DIR = Path(__file__).parent
PROJECT_ROOT = BASE_DIR

# Diretório de origem e destino vindos do .env
# IMPORTANTE: Configure SOURCE_DIR e DEST_DIR no arquivo .env
SOURCE_DIR = Path(os.getenv("SOURCE_DIR", "")).expanduser()
if not SOURCE_DIR or str(SOURCE_DIR) == ".":
	raise ValueError("SOURCE_DIR não configurado. Configure no arquivo .env")

DESTINO = Path(os.getenv("DEST_DIR", ""))
if not DESTINO or str(DESTINO) == ".":
	raise ValueError("DEST_DIR não configurado. Configure no arquivo .env")

DESTINO.mkdir(exist_ok=True, parents=True)

# API externa
API_BASE_URL = os.getenv("API_BASE_URL", "")
API_ENABLED = os.getenv("API_ENABLED", "true").strip().lower() in {"1", "true", "yes", "on"}
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "15"))

# Logging
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True, parents=True)
APP_LOG_PATH = LOG_DIR / os.getenv("APP_LOG_FILE", "app.log")
PHOTOS_LOG_PATH = LOG_DIR / os.getenv("PHOTOS_LOG_FILE", "photos.log")
LOG_MAX_BYTES = int(os.getenv("LOG_MAX_BYTES", "2097152"))  # 2 MB
LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "3"))

# Telegram Bot
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
TELEGRAM_ENABLED = os.getenv("TELEGRAM_ENABLED", "true").strip().lower() in {"1", "true", "yes", "on"}
TELEGRAM_TIMEOUT = int(os.getenv("TELEGRAM_TIMEOUT", "10"))

# Configurações de Processamento de Imagens
IMAGE_MAX_WIDTH = int(os.getenv("IMAGE_MAX_WIDTH", "225"))
IMAGE_QUALITY_INITIAL = int(os.getenv("IMAGE_QUALITY_INITIAL", "50"))
IMAGE_QUALITY_MIN = int(os.getenv("IMAGE_QUALITY_MIN", "10"))
IMAGE_MAX_SIZE_KB = int(os.getenv("IMAGE_MAX_SIZE_KB", "100"))
IMAGE_COMPRESSION_STEP = int(os.getenv("IMAGE_COMPRESSION_STEP", "5"))
IMAGE_MAX_ITERATIONS = int(os.getenv("IMAGE_MAX_ITERATIONS", "12"))

# Configurações de Lock File
LOCK_TIMEOUT = int(os.getenv("LOCK_TIMEOUT", "5"))