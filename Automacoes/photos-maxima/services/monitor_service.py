from __future__ import annotations

"""
Processamento pontual de imagens.

Executa uma única vez por chamada (Agendador do Windows faz a repetição).
A cada execução o script:

1. Determina a janela temporal desde a última execução até agora (limitada ao dia atual).
2. Procura imagens novas na origem dentro dessa janela.
3. Processa e copia as imagens para o destino.
4. Envia uma notificação pelo Telegram informando que rodou.
5. Salva o timestamp da execução atual.
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import List

from config import DESTINO, EXTS
from services.image_service import copiar_imagem
from services.logging_service import get_app_logger
from services.state_service import obter_ultima_execucao, salvar_execucao

logger = get_app_logger()


def _calcular_intervalo_execucao(agora: datetime | None = None) -> tuple[datetime, datetime]:
	"""
	Determina o intervalo a ser processado com base no último registro.
	
	Regras:
	- Processa apenas arquivos do dia atual (não processa dias anteriores).
	- Se não houver histórico OU última execução for de outro dia:
	  → Início = início do dia atual (00:00:00)
	- Se última execução for do mesmo dia:
	  → Início = última execução registrada
	- Fim = momento atual (sem segundos/microsegundos)
	"""
	ref = (agora or datetime.now()).replace(second=0, microsecond=0)
	ultima_execucao = obter_ultima_execucao()
	
	# Início do dia atual
	inicio_dia = ref.replace(hour=0, minute=0, second=0, microsecond=0)
	
	# Se não há última execução OU é de outro dia, começa do início do dia atual
	if (
		not ultima_execucao
		or ultima_execucao.date() != ref.date()
	):
		inicio = inicio_dia
	else:
		# Última execução é do mesmo dia, usa ela como início
		inicio = ultima_execucao
	
	# Garante que início não seja maior que fim
	if inicio >= ref:
		# Se início >= fim, usa início do dia como fallback
		inicio = inicio_dia
	
	# Garante que início não seja anterior ao início do dia
	if inicio < inicio_dia:
		inicio = inicio_dia

	return inicio, ref


def _listar_imagens_intervalo(origem: Path, inicio: datetime, fim: datetime) -> List[Path]:
	"""Retorna todas as imagens encontradas dentro da janela solicitada."""
	selecionadas: List[tuple[datetime, Path]] = []
	contador = 0

	logger.info("Buscando imagens no diretório...")
	
	try:
		for arquivo in origem.rglob("*"):
			contador += 1
			# Log de progresso a cada 1000 arquivos verificados
			if contador % 1000 == 0:
				logger.info(f"Verificados {contador} arquivos...")
			
			try:
				if not arquivo.is_file():
					continue
				if arquivo.suffix.lower() not in EXTS:
					continue

				stat_info = arquivo.stat()
				data_referencia = datetime.fromtimestamp(
					max(stat_info.st_mtime, getattr(stat_info, "st_ctime", stat_info.st_mtime))
				)
			except (PermissionError, OSError):
				continue

			if inicio <= data_referencia <= fim:
				selecionadas.append((data_referencia, arquivo))
	except KeyboardInterrupt:
		logger.error("Busca de imagens interrompida pelo usuário")
		raise

	logger.info(f"Busca concluída. Total de arquivos verificados: {contador}")
	selecionadas.sort(key=lambda registro: registro[0])
	return [arquivo for _, arquivo in selecionadas]


def monitorar(diretorio: str):
	"""Executa o processamento pontual baseado em janela temporal."""
	origem = Path(diretorio).expanduser().resolve()
	
	# Verificar se o diretório existe
	if not origem.exists():
		logger.error(f"Diretório de origem não encontrado: {origem}")
		raise FileNotFoundError(f"Diretório não encontrado: {origem}")
	
	# Verificar se tem permissão de acesso ao diretório
	try:
		# Tentar listar o diretório para verificar permissões
		list(origem.iterdir())
	except PermissionError as exc:
		logger.error(f"Acesso negado ao diretório: {origem}")
		raise PermissionError(f"Acesso negado ao diretório: {origem}") from exc
	except OSError as exc:
		logger.error(f"Erro de rede/acesso ao diretório: {origem} - {exc}")
		raise OSError(f"Erro de rede/acesso ao diretório: {origem}") from exc

	inicio, fim = _calcular_intervalo_execucao()
	arquivos = _listar_imagens_intervalo(origem, inicio, fim)
	
	logger.info(f"IMAGENS LOCALIZADAS: {len(arquivos)}")
	
	if not arquivos:
		salvar_execucao(fim)
		return 0

	logger.info("IMAGENS EM PROCESSAMENTO")

	processadas = 0
	erros = 0
	for arquivo in arquivos:
		try:
			copiar_imagem(arquivo)
			processadas += 1
		except Exception as exc:
			logger.error(f"Erro ao processar {arquivo.name}: {exc}")
			erros += 1

	if erros == 0:
		logger.success(f"IMAGENS PROCESSADAS: {processadas}")
	else:
		logger.error(f"IMAGENS PROCESSADAS: {processadas} | ERROS: {erros}")
	
	salvar_execucao(fim)
	return processadas
