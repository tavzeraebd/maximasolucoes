# scheduler_service.py
import time
import threading
from datetime import datetime, timedelta
from telegram_service import TelegramService
from thread_monitor import ThreadMonitor


class SchedulerService:
    """Serviço para agendar execuções em horários específicos."""

    def __init__(self, telegram_service: TelegramService = None, nome_servico: str = "Serviço"):
        """
        Inicializa o scheduler.
        
        Args:
            telegram_service: Instância do TelegramService (se None, cria uma nova)
            nome_servico: Nome do serviço para as notificações
        """
        self.running = False
        self.thread = None
        self.telegram_service = telegram_service or TelegramService()
        self.nome_servico = nome_servico

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
        try:
            self.telegram_service.notificar_execucao_servico(self.nome_servico)
        except Exception as exc:
            print(f"[ERRO] Falha ao executar notificação: {exc}")

    def _loop_agendamento(self):
        """Loop principal do agendador."""
        print("[SCHEDULER] Agendador iniciado. Aguardando próxima hora cheia...")
        
        while self.running:
            try:
                # Calcular tempo até próxima hora cheia
                segundos_ate_proxima = self._calcular_segundos_ate_proxima_hora()
                proxima_hora = self._calcular_proxima_hora_cheia()
                
                print(f"[SCHEDULER] Próxima execução: {proxima_hora.strftime('%d/%m/%Y %H:%M:%S')}")
                print(f"[SCHEDULER] Aguardando {segundos_ate_proxima:.0f} segundos...")
                
                # Aguardar até a próxima hora cheia
                time.sleep(segundos_ate_proxima)
                
                if not self.running:
                    break
                
                # Executar notificação
                print(f"[SCHEDULER] Executando notificação às {datetime.now().strftime('%H:%M:%S')}...")
                self._executar_notificacao()
                
                # Aguardar 1 segundo para evitar múltiplas execuções no mesmo segundo
                time.sleep(1)
                
            except Exception as exc:
                print(f"[ERRO] Erro no loop do agendador: {exc}")
                time.sleep(60)  # Aguardar 1 minuto antes de tentar novamente

    def iniciar(self):
        """Inicia o agendador em uma thread separada."""
        if self.running:
            print("[AVISO] Agendador já está em execução.")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._loop_agendamento, daemon=True, name="SchedulerThread")
        self.thread.start()
        print("[SCHEDULER] Agendador iniciado em thread separada.")
        print(f"[SCHEDULER] Thread ID: {self.thread.ident} | Nome: {self.thread.name}")
        print(f"[SCHEDULER] Total de threads ativas: {ThreadMonitor.contar_threads_ativas()}")

    def parar(self):
        """Para o agendador."""
        if not self.running:
            return
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("[SCHEDULER] Agendador parado.")

    def listar_threads(self):
        """Lista todas as threads ativas."""
        ThreadMonitor.imprimir_threads_ativas()

    def aguardar(self):
        """Aguarda a thread do agendador (útil para manter o programa rodando)."""
        if self.thread:
            try:
                self.thread.join()
            except KeyboardInterrupt:
                print("\n[SCHEDULER] Interrompido pelo usuário.")
                self.parar()

