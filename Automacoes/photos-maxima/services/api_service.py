import requests
from pathlib import Path
from config import API_BASE_URL, API_ENABLED, API_TIMEOUT
from services.logging_service import get_app_logger

logger = get_app_logger()

def enviar_imagem_api(caminho_imagem: Path):
	"""
	Atualiza via API usando o nome do arquivo (sem extensão) como product_id na URL
	"""
	if not API_ENABLED:
		return False

	product_id = caminho_imagem.stem
	url = f"{API_BASE_URL}/{product_id}/photo"

	try:
		response = requests.put(url, timeout=API_TIMEOUT)

		if response.status_code in (200, 201, 204):
			return True
		else:
			logger.error(f"Erro API p/ produto {product_id}: Status {response.status_code} - {response.text}")
			return False

	except Exception as e:
		logger.error(f"Erro ao tentar atualizar produto {product_id} na API: {e}")
		return False
