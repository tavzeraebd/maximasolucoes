# services/telegram_service.py
"""
Serviço para envio de mensagens via Telegram Bot API.
"""
import requests
import os
from typing import Optional
from datetime import datetime
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_TIMEOUT
from services.logging_service import get_app_logger

logger = get_app_logger()


class TelegramService:
	"""Serviço para envio de mensagens via Telegram Bot API."""

	def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
		"""
		Inicializa o serviço de Telegram.
		
		Args:
			bot_token: Token do bot do Telegram (ou usa variável de ambiente TELEGRAM_BOT_TOKEN)
			chat_id: ID do chat (ou usa variável de ambiente TELEGRAM_CHAT_ID)
		"""
		self.bot_token = bot_token or TELEGRAM_BOT_TOKEN or os.getenv("TELEGRAM_BOT_TOKEN", "")
		self.chat_id = chat_id or TELEGRAM_CHAT_ID or os.getenv("TELEGRAM_CHAT_ID", "")

	def enviar_mensagem(self, mensagem: str, chat_id: Optional[str] = None, parse_mode: str = "HTML") -> Optional[int]:
		"""
		Envia uma mensagem para o Telegram.
		
		Args:
			mensagem: Texto da mensagem a ser enviada
			chat_id: ID do chat (se None, usa o configurado)
			parse_mode: Modo de parsing (HTML, Markdown, ou None)
		
		Returns:
			message_id se enviado com sucesso, None caso contrário
		"""
		if not self.bot_token:
			logger.warning("[TELEGRAM] TELEGRAM_BOT_TOKEN não configurado. Mensagem não enviada.")
			return None
		
		chat_id_final = chat_id or self.chat_id
		
		if not chat_id_final:
			logger.warning("[TELEGRAM] TELEGRAM_CHAT_ID não configurado. Mensagem não enviada.")
			return None
		
		url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
		
		payload = {
			"chat_id": chat_id_final,
			"text": mensagem
		}
		
		if parse_mode:
			payload["parse_mode"] = parse_mode
		
		try:
			response = requests.post(url, json=payload, timeout=TELEGRAM_TIMEOUT)
			response.raise_for_status()
			result = response.json()
			if result.get("ok") and "result" in result:
				return result["result"].get("message_id")
			return None
		except requests.RequestException as exc:
			logger.error(f"[TELEGRAM] Falha ao enviar mensagem: {exc}")
			if hasattr(exc, 'response') and exc.response is not None:
				try:
					error_data = exc.response.json()
					logger.error(f"[TELEGRAM] Detalhes: {error_data}")
				except:
					pass
			return None

	def notificar_execucao_servico(self, nome_servico: str = "Serviço de Imagens") -> Optional[int]:
		"""
		Envia notificação padrão informando que o serviço rodou.
		
		Args:
			nome_servico: Nome do serviço a ser exibido na mensagem
		
		Returns:
			message_id se enviado com sucesso, None caso contrário
		"""
		agora = datetime.now()
		data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")
		
		mensagem = (
            f"🤖 <b>Serviço Monitor de Imagens</b>\n\n"
            f"✅ Serviço executado com sucesso!\n"
            f"🕐 Data/Hora: {data_hora}"
        )
		
		return self.enviar_mensagem(mensagem)

	def enviar_mensagem_simples(self, texto: str, chat_id: Optional[str] = None) -> Optional[int]:
		"""
		Envia uma mensagem de texto simples (sem formatação HTML).
		
		Args:
			texto: Texto da mensagem
			chat_id: ID do chat (se None, usa o configurado)
		
		Returns:
			message_id se enviado com sucesso, None caso contrário
		"""
		return self.enviar_mensagem(texto, chat_id=chat_id, parse_mode=None)

	def deletar_mensagem(self, message_id: int, chat_id: Optional[str] = None) -> bool:
		"""
		Deleta uma mensagem do Telegram.
		
		Args:
			message_id: ID da mensagem a ser deletada
			chat_id: ID do chat (se None, usa o configurado)
		
		Returns:
			True se deletado com sucesso, False caso contrário
		"""
		if not self.bot_token:
			logger.warning("[TELEGRAM] TELEGRAM_BOT_TOKEN não configurado. Mensagem não deletada.")
			return False
		
		chat_id_final = chat_id or self.chat_id
		
		if not chat_id_final:
			logger.warning("[TELEGRAM] TELEGRAM_CHAT_ID não configurado. Mensagem não deletada.")
			return False
		
		url = f"https://api.telegram.org/bot{self.bot_token}/deleteMessage"
		
		payload = {
			"chat_id": chat_id_final,
			"message_id": message_id
		}
		
		try:
			response = requests.post(url, json=payload, timeout=TELEGRAM_TIMEOUT)
			response.raise_for_status()
			result = response.json()
			return result.get("ok", False)
		except requests.RequestException as exc:
			logger.error(f"[TELEGRAM] Falha ao deletar mensagem: {exc}")
			if hasattr(exc, 'response') and exc.response is not None:
				try:
					error_data = exc.response.json()
					logger.error(f"[TELEGRAM] Detalhes: {error_data}")
				except:
					pass
			return False

