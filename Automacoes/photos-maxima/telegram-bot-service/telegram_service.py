# telegram_service.py
"""
Serviço independente para envio de mensagens via Telegram Bot API.

Este serviço pode ser usado em qualquer projeto Python.
"""
import requests
import os
from typing import Optional
from datetime import datetime


class TelegramService:
    """Serviço para envio de mensagens via Telegram Bot API."""

    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
        """
        Inicializa o serviço de Telegram.
        
        Args:
            bot_token: Token do bot do Telegram (ou usa variável de ambiente TELEGRAM_BOT_TOKEN)
            chat_id: ID do chat (ou usa variável de ambiente TELEGRAM_CHAT_ID)
        """
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID", "")

    def enviar_mensagem(self, mensagem: str, chat_id: Optional[str] = None, parse_mode: str = "HTML") -> bool:
        """
        Envia uma mensagem para o Telegram.
        
        Args:
            mensagem: Texto da mensagem a ser enviada
            chat_id: ID do chat (se None, usa o configurado)
            parse_mode: Modo de parsing (HTML, Markdown, ou None)
        
        Returns:
            True se enviado com sucesso, False caso contrário
        """
        if not self.bot_token:
            print("[AVISO] TELEGRAM_BOT_TOKEN não configurado. Mensagem não enviada.")
            return False
        
        chat_id_final = chat_id or self.chat_id
        
        if not chat_id_final:
            print("[AVISO] TELEGRAM_CHAT_ID não configurado. Mensagem não enviada.")
            return False
        
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        
        payload = {
            "chat_id": chat_id_final,
            "text": mensagem
        }
        
        if parse_mode:
            payload["parse_mode"] = parse_mode
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except requests.RequestException as exc:
            print(f"[ERRO] Falha ao enviar mensagem para Telegram: {exc}")
            if hasattr(exc, 'response') and exc.response is not None:
                try:
                    error_data = exc.response.json()
                    print(f"[ERRO] Detalhes: {error_data}")
                except:
                    pass
            return False

    def notificar_execucao_servico(self, nome_servico: str = "Serviço") -> bool:
        """
        Envia notificação padrão informando que o serviço rodou.
        
        Args:
            nome_servico: Nome do serviço a ser exibido na mensagem
        
        Returns:
            True se enviado com sucesso, False caso contrário
        """
        agora = datetime.now()
        data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")
        
        mensagem = (
            f"🤖 <b>{nome_servico}</b>\n\n"
            f"✅ Serviço executado com sucesso!\n"
            f"🕐 Data/Hora: {data_hora}"
        )
        
        return self.enviar_mensagem(mensagem)

    def enviar_mensagem_simples(self, texto: str, chat_id: Optional[str] = None) -> bool:
        """
        Envia uma mensagem de texto simples (sem formatação HTML).
        
        Args:
            texto: Texto da mensagem
            chat_id: ID do chat (se None, usa o configurado)
        
        Returns:
            True se enviado com sucesso, False caso contrário
        """
        return self.enviar_mensagem(texto, chat_id=chat_id, parse_mode=None)

