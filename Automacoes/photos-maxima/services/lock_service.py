"""
Serviço para gerenciar lock file e garantir execução única do script.
"""
import os
import sys
import time
import signal
from pathlib import Path
from typing import Optional

from config import LOG_DIR
from services.logging_service import get_app_logger

logger = get_app_logger()
LOCK_FILE = LOG_DIR / "photos_maxima.lock"


def _obter_pid_do_lock() -> Optional[int]:
	"""Lê o PID do arquivo de lock."""
	if not LOCK_FILE.exists():
		return None
	
	try:
		pid_str = LOCK_FILE.read_text(encoding="utf-8").strip()
		return int(pid_str)
	except (ValueError, OSError):
		return None


def _processo_esta_rodando(pid: int) -> bool:
	"""Verifica se um processo com o PID especificado está rodando."""
	try:
		if sys.platform == "win32":
			# Windows
			import subprocess
			result = subprocess.run(
				["tasklist", "/FI", f"PID eq {pid}"],
				capture_output=True,
				text=True,
				timeout=5
			)
			return str(pid) in result.stdout
		else:
			# Linux/Unix
			os.kill(pid, 0)
			return True
	except Exception:
		return False


def _matar_processo(pid: int) -> bool:
	"""Tenta matar um processo pelo PID."""
	try:
		if sys.platform == "win32":
			# Windows
			import subprocess
			subprocess.run(
				["taskkill", "/F", "/PID", str(pid)],
				capture_output=True,
				timeout=10
			)
			time.sleep(1)  # Aguarda o processo terminar
			return not _processo_esta_rodando(pid)
		else:
			# Linux/Unix
			os.kill(pid, signal.SIGTERM)
			time.sleep(1)
			if _processo_esta_rodando(pid):
				os.kill(pid, signal.SIGKILL)
				time.sleep(1)
			return not _processo_esta_rodando(pid)
	except Exception as exc:
		logger.error(f"Erro ao tentar matar processo {pid}: {exc}")
		return False


def criar_lock() -> bool:
	"""
	Cria um arquivo de lock com o PID do processo atual.
	Se já existir um lock de um processo rodando, mata o processo anterior.
	
	Returns:
		True se conseguiu criar o lock, False caso contrário
	"""
	pid_atual = os.getpid()
	
	# Verificar se já existe um lock
	pid_anterior = _obter_pid_do_lock()
	
	if pid_anterior is not None:
		if pid_anterior == pid_atual:
			# É o mesmo processo, já tem o lock
			return True
		
		# Verificar se o processo anterior ainda está rodando
		if _processo_esta_rodando(pid_anterior):
			logger.warning(f"Processo anterior ainda está rodando (PID: {pid_anterior}). Encerrando...")
			if _matar_processo(pid_anterior):
				logger.info(f"Processo anterior (PID: {pid_anterior}) encerrado com sucesso.")
			else:
				logger.error(f"Falha ao encerrar processo anterior (PID: {pid_anterior}).")
				return False
		else:
			logger.info(f"Lock file encontrado, mas processo anterior (PID: {pid_anterior}) não está mais rodando. Removendo lock antigo.")
	
	# Criar novo lock file
	try:
		LOCK_FILE.write_text(str(pid_atual), encoding="utf-8")
		logger.info(f"Lock file criado (PID: {pid_atual})")
		return True
	except Exception as exc:
		logger.error(f"Erro ao criar lock file: {exc}")
		return False


def remover_lock() -> None:
	"""Remove o arquivo de lock."""
	try:
		if LOCK_FILE.exists():
			LOCK_FILE.unlink()
			logger.info("Lock file removido")
	except Exception as exc:
		logger.error(f"Erro ao remover lock file: {exc}")


def verificar_lock() -> bool:
	"""
	Verifica se o lock file atual pertence ao processo atual.
	
	Returns:
		True se o lock pertence ao processo atual, False caso contrário
	"""
	pid_atual = os.getpid()
	pid_lock = _obter_pid_do_lock()
	return pid_lock == pid_atual

