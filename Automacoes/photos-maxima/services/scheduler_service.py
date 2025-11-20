# services/scheduler_service.py
import time
import threading
from datetime import datetime, timedelta
from config import TELEGRAM_ENABLED
from services.logging_service import get_app_logger
from services.telegram_service import TelegramService

logger = get_app_logger()


class SchedulerService:
	"""Serviço para agendar execuções em horários específicos."""

	def __init__(self):
		self.running = False
		self.thread = None
		self.telegram_service = None
		self._lock = threading.Lock()
		
		if TELEGRAM_ENABLED:
			try:
				self.telegram_service = TelegramService()
			except Exception as e:
				logger.warning(f"Erro ao inicializar Telegram Service no scheduler: {e}")

	def _calcular_proxima_hora_cheia(self) -> datetime:
		"""
		Calcula o próximo horário de hora cheia.
		
		Returns:
			datetime do próximo horário de hora cheia
		"""
		agora = datetime.now()
		proxima_hora = agora.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
		return proxima_hora

	def _calcular_segundos_ate_proxima_hora(self) -> float:
		"""
		Calcula quantos segundos faltam até a próxima hora cheia.
		
		Returns:
			Número de segundos até a próxima hora cheia
		"""
		proxima_hora = self._calcular_proxima_hora_cheia()
		agora = datetime.now()
		delta = (proxima_hora - agora).total_seconds()
		return max(0, delta)

	def _executar_notificacao(self):
		"""Executa a notificação do Telegram."""
		if not self.telegram_service:
			return
			
		try:
			self.telegram_service.notificar_execucao_servico("Serviço de Imagens")
			logger.info("Notificação agendada enviada para o Telegram")
		except Exception as exc:
			logger.warning(f"Erro ao executar notificação agendada: {exc}")

	def _loop_agendamento(self):
		"""Loop principal do agendador."""
		print("[SCHEDULER] Agendador iniciado. Aguardando próxima hora cheia...")
		logger.info("[SCHEDULER] Agendador iniciado. Aguardando próxima hora cheia...")
		
		while True:
			# Verificar se deve continuar rodando
			with self._lock:
				if not self.running:
					break
			
			try:
				# Calcular tempo até próxima hora cheia
				segundos_ate_proxima = self._calcular_segundos_ate_proxima_hora()
				proxima_hora = self._calcular_proxima_hora_cheia()
				
				print(f"[SCHEDULER] Próxima execução: {proxima_hora.strftime('%d/%m/%Y %H:%M:%S')}")
				print(f"[SCHEDULER] Aguardando {segundos_ate_proxima:.0f} segundos...")
				logger.info(f"[SCHEDULER] Próxima execução: {proxima_hora.strftime('%d/%m/%Y %H:%M:%S')}")
				logger.info(f"[SCHEDULER] Aguardando {segundos_ate_proxima:.0f} segundos...")
				
				# Aguardar até a próxima hora cheia (com verificação periódica)
				intervalo_verificacao = min(60, segundos_ate_proxima)  # Verificar a cada minuto ou menos
				tempo_restante = segundos_ate_proxima
				
				while tempo_restante > 0:
					with self._lock:
						if not self.running:
							return
					
					sleep_time = min(intervalo_verificacao, tempo_restante)
					time.sleep(sleep_time)
					tempo_restante -= sleep_time
				
				# Verificar novamente antes de executar
				with self._lock:
					if not self.running:
						break
				
				# Executar notificação
				logger.info(f"[SCHEDULER] Executando notificação às {datetime.now().strftime('%H:%M:%S')}...")
				self._executar_notificacao()
				
				# Aguardar 1 segundo para evitar múltiplas execuções no mesmo segundo
				time.sleep(1)
				
			except Exception as exc:
				logger.error(f"Erro no loop do agendador: {exc}")
				time.sleep(60)  # Aguardar 1 minuto antes de tentar novamente
		
		logger.info("[SCHEDULER] Loop do agendador finalizado.")

	def _contar_threads_ativas(self) -> int:
		"""Conta o número de threads ativas."""
		return threading.active_count()
	
	def _limpar_threads_antigas(self):
		"""Limpa threads antigas do scheduler que possam estar em memória."""
		# Para a thread atual se estiver rodando
		if self.thread and self.thread.is_alive():
			logger.info("[SCHEDULER] Encontrada thread antiga, finalizando...")
			with self._lock:
				self.running = False
			self.thread.join(timeout=5)
			if self.thread.is_alive():
				logger.warning("[SCHEDULER] Thread antiga não finalizou no tempo esperado.")
			else:
				logger.info("[SCHEDULER] Thread antiga finalizada com sucesso.")
		
		# Reset do estado
		with self._lock:
			self.running = False
		self.thread = None
		
		# Busca e loga outras threads do scheduler que possam estar rodando (para informação)
		threads_orfas = []
		for thread in threading.enumerate():
			if thread.name == "SchedulerThread" and thread != threading.current_thread():
				if thread.is_alive():
					threads_orfas.append(thread.ident)
		
		if threads_orfas:
			logger.warning(f"[SCHEDULER] Encontradas {len(threads_orfas)} thread(s) órfã(s): {threads_orfas}")
			logger.warning("[SCHEDULER] Threads órfãs serão finalizadas quando o processo terminar (são daemon threads)")

	def iniciar(self):
		"""Inicia o agendador em uma thread separada."""
		# Limpa threads antigas antes de iniciar
		self._limpar_threads_antigas()
		
		with self._lock:
			if self.running:
				logger.warning("[AVISO] Agendador já está em execução.")
				return
			
			if not TELEGRAM_ENABLED:
				logger.info("[SCHEDULER] Telegram desabilitado. Agendador não será iniciado.")
				return
			
			self.running = True
		
		# Cria nova thread
		self.thread = threading.Thread(
			target=self._loop_agendamento,
			daemon=True,
			name="SchedulerThread"
		)
		self.thread.start()
		
		# Mensagens informativas (como no orders-rejects)
		print("[SCHEDULER] Agendador iniciado em thread separada.")
		print(f"[SCHEDULER] Thread ID: {self.thread.ident} | Nome: {self.thread.name}")
		print(f"[SCHEDULER] Total de threads ativas: {self._contar_threads_ativas()}")
		print("💡 Dica: Use Ctrl+C para encerrar")
		logger.info(f"[SCHEDULER] Agendador iniciado em thread separada (ID: {self.thread.ident}, Nome: {self.thread.name})")

	def parar(self):
		"""Para o agendador."""
		with self._lock:
			if not self.running:
				return
			self.running = False
		
		if self.thread and self.thread.is_alive():
			logger.info("[SCHEDULER] Aguardando finalização da thread do agendador...")
			self.thread.join(timeout=10)
			if self.thread.is_alive():
				logger.warning("[SCHEDULER] Thread do agendador não finalizou no tempo esperado.")
			else:
				logger.info("[SCHEDULER] Thread do agendador finalizada com sucesso.")
		
		logger.info("[SCHEDULER] Agendador parado.")
	
	def esta_rodando(self) -> bool:
		"""Verifica se o agendador está rodando."""
		with self._lock:
			return self.running

