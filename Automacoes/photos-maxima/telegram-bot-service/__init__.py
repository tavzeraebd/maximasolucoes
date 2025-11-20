# __init__.py
"""
Telegram Bot Service - Serviço independente para envio de mensagens via Telegram com agendamento automático.

Este pacote pode ser copiado e usado em qualquer projeto Python.
"""

from telegram_service import TelegramService
from scheduler_service import SchedulerService
from thread_monitor import ThreadMonitor

__version__ = "1.0.0"
__all__ = ["TelegramService", "SchedulerService", "ThreadMonitor"]

