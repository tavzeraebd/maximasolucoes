# example_usage.py
"""
Exemplo de uso do TelegramService e SchedulerService.

Este arquivo demonstra como usar os serviços de Telegram e Scheduler em seus projetos.
"""
import os
from pathlib import Path
from telegram_service import TelegramService
from scheduler_service import SchedulerService
from datetime import datetime

# Exemplo 1: Usando TelegramService com variáveis de ambiente
def exemplo_telegram_com_env():
    """Exemplo usando variáveis de ambiente (.env ou sistema)."""
    # As variáveis TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID devem estar configuradas
    service = TelegramService()
    
    # Enviar mensagem simples
    service.enviar_mensagem("Olá! Esta é uma mensagem de teste.")
    
    # Enviar notificação de serviço
    service.notificar_execucao_servico("Meu Serviço Personalizado")


# Exemplo 2: Usando SchedulerService com notificações a cada hora cheia
def exemplo_scheduler_basico():
    """Exemplo básico de uso do scheduler."""
    # Criar serviço de Telegram
    telegram = TelegramService()
    
    # Criar scheduler
    scheduler = SchedulerService(
        telegram_service=telegram,
        nome_servico="Meu Serviço Automatizado"
    )
    
    # Iniciar scheduler
    scheduler.iniciar()
    
    try:
        # Manter o programa rodando
        scheduler.aguardar()
    except KeyboardInterrupt:
        print("\n[SCHEDULER] Encerrando...")
        scheduler.parar()


# Exemplo 3: Scheduler com credenciais diretas
def exemplo_scheduler_com_credenciais():
    """Exemplo passando credenciais diretamente."""
    bot_token = "seu_bot_token_aqui"
    chat_id = "seu_chat_id_aqui"
    
    telegram = TelegramService(bot_token=bot_token, chat_id=chat_id)
    scheduler = SchedulerService(
        telegram_service=telegram,
        nome_servico="Serviço com Credenciais Diretas"
    )
    
    scheduler.iniciar()
    
    try:
        scheduler.aguardar()
    except KeyboardInterrupt:
        scheduler.parar()


# Exemplo 4: Verificar threads ativas
def exemplo_listar_threads():
    """Exemplo de como listar threads ativas."""
    from thread_monitor import ThreadMonitor
    
    telegram = TelegramService()
    scheduler = SchedulerService(telegram_service=telegram)
    
    scheduler.iniciar()
    
    # Listar threads
    print("\n📊 Listando threads ativas:")
    scheduler.listar_threads()
    
    # Ou usar diretamente
    ThreadMonitor.imprimir_threads_ativas()
    
    try:
        scheduler.aguardar()
    except KeyboardInterrupt:
        scheduler.parar()


# Exemplo 5: Integração completa
def exemplo_integracao_completa():
    """Exemplo de integração completa com seu serviço."""
    # 1. Criar serviço de Telegram
    telegram = TelegramService()
    
    # 2. Executar seu serviço principal
    print("Executando serviço principal...")
    # seu_codigo_aqui()
    
    # 3. Iniciar scheduler para notificações periódicas
    scheduler = SchedulerService(
        telegram_service=telegram,
        nome_servico="Meu Serviço de Processamento"
    )
    scheduler.iniciar()
    
    # 4. Manter o programa rodando
    try:
        scheduler.aguardar()
    except KeyboardInterrupt:
        print("\n[SCHEDULER] Encerrando...")
        scheduler.parar()


if __name__ == "__main__":
    print("📚 Exemplos de uso do TelegramService e SchedulerService\n")
    print("Descomente a função que deseja testar:\n")
    
    # Descomente para testar:
    # exemplo_telegram_com_env()
    # exemplo_scheduler_basico()
    # exemplo_scheduler_com_credenciais()
    # exemplo_listar_threads()
    # exemplo_integracao_completa()
    
    print("\n💡 Configure TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID antes de executar os exemplos.")

