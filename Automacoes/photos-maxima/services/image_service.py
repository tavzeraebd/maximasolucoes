import time
from pathlib import Path
from PIL import Image
from config import (
	DESTINO, IMAGE_MAX_WIDTH, IMAGE_QUALITY_INITIAL, IMAGE_QUALITY_MIN,
	IMAGE_MAX_SIZE_KB, IMAGE_COMPRESSION_STEP, IMAGE_MAX_ITERATIONS
)
from utils.file_utils import eh_imagem
from services.api_service import enviar_imagem_api
from services.logging_service import get_app_logger, get_photos_logger

logger = get_app_logger()
photos_logger = get_photos_logger()

def esperar_arquivo_liberado(path: Path, tentativas=10, intervalo=0.5) -> bool:
	"""Tenta acessar o arquivo para leitura até que esteja liberado (usado em rede)."""
	for _ in range(tentativas):
		try:
			with open(path, "rb") as f:
				f.read(1)
			return True
		except (PermissionError, OSError):
			time.sleep(intervalo)
	return False

def copiar_imagem(path: Path):
	if not eh_imagem(path):
		return

	if not esperar_arquivo_liberado(path):
		logger.error(f"Arquivo em uso após várias tentativas: {path.name}")
		raise Exception(f"Arquivo em uso: {path.name}")

	dest_file = DESTINO / (path.stem + ".jpg")

	# Backup se já existir
	if dest_file.exists():
		backup_file = dest_file.with_suffix(".bkp.jpg")
		try:
			# Tentar remover backup antigo se existir
			if backup_file.exists():
				try:
					backup_file.unlink()
				except (PermissionError, OSError):
					pass  # Ignora se não conseguir remover backup antigo
			
			# Tentar renomear arquivo existente para backup
			try:
				dest_file.rename(backup_file)
			except (PermissionError, OSError) as e:
				# Se não conseguir renomear, tentar deletar o arquivo antigo
				logger.warning(f"Não foi possível criar backup de {path.name}. Tentando deletar arquivo antigo...")
				try:
					dest_file.unlink()
				except (PermissionError, OSError) as e2:
					# Se não conseguir deletar, tentar sobrescrever diretamente
					logger.warning(f"Não foi possível deletar arquivo antigo {path.name}. Tentando sobrescrever...")
					# Continua para tentar sobrescrever
		except Exception as e:
			logger.warning(f"Erro ao processar backup de {path.name}: {e}. Continuando...")
			# Não faz raise, continua o processamento

	try:
		with Image.open(path) as img:
			img = img.convert("RGB")

			if img.width > IMAGE_MAX_WIDTH:
				proporcao = IMAGE_MAX_WIDTH / img.width
				nova_altura = int(img.height * proporcao)
				img = img.resize((IMAGE_MAX_WIDTH, nova_altura), Image.LANCZOS)

			qualidade = IMAGE_QUALITY_INITIAL
			salvar_kwargs = {
				"optimize": True,
				"progressive": True,
				"quality": qualidade,
			}

			# Tentar salvar a imagem
			for tentativa in range(IMAGE_MAX_ITERATIONS):
				try:
					img.save(dest_file, format="JPEG", **salvar_kwargs)
					size_kb = dest_file.stat().st_size / 1024

					if size_kb <= IMAGE_MAX_SIZE_KB:
						break
					elif qualidade > IMAGE_QUALITY_MIN:
						qualidade -= IMAGE_COMPRESSION_STEP
						salvar_kwargs["quality"] = qualidade
					else:
						break
				except (PermissionError, OSError) as e:
					# Se não conseguir salvar por permissão, tenta novamente após um delay
					if tentativa < 11:
						logger.warning(f"Erro de acesso ao salvar {path.name} (tentativa {tentativa + 1}/12). Aguardando...")
						time.sleep(1)
						continue
					else:
						logger.error(f"Falha ao salvar {path.name} após 12 tentativas: {e}")
						raise

		size_kb_final = round(dest_file.stat().st_size / 1024)
		photos_logger.info(dest_file.name)

		# Envia notificação para API externa (opcional, conforme configuração)
		enviar_imagem_api(dest_file)

	except (PermissionError, OSError) as e:
		logger.error(f"Erro de acesso ao processar {path.name}: {e}")
		raise
	except Exception as e:
		logger.error(f"Erro ao processar {path.name}: {e}")
		raise

