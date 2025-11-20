from pathlib import Path
from PIL import Image
from config import EXTS

def eh_imagem(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.suffix.lower() in EXTS:
        return True
    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except Exception:
        return False
