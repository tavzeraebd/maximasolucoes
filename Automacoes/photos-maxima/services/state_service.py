from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from config import LOG_DIR
from services.logging_service import get_app_logger

logger = get_app_logger()
STATE_FILE = LOG_DIR / "execution_state.json"


def obter_ultima_execucao() -> Optional[datetime]:
	"""Lê o timestamp da última execução registrada."""
	if not STATE_FILE.exists():
		return None

	try:
		data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
		valor = data.get("ultima_execucao")
		if not valor:
			return None
		return datetime.fromisoformat(valor)
	except Exception as exc:
		logger.warning(f"Falha ao ler estado da última execução: {exc}")
		return None


def salvar_execucao(moment: datetime) -> None:
	"""Atualiza o timestamp da última execução."""
	try:
		STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
		payload = {"ultima_execucao": moment.isoformat()}
		STATE_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
	except Exception as exc:
		logger.warning(f"Não foi possível persistir o estado da execução: {exc}")

