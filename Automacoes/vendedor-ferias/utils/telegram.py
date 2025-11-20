# utils/telegram.py
"""
Serviço para envio de mensagens via Telegram Bot API.
"""
import requests
from typing import Optional
import os
from datetime import datetime


class TelegramService:
    """Serviço para envio de mensagens via Telegram Bot API."""

    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
        """
        Inicializa o serviço de Telegram.
        Usa o bot Sentinel do photos-maxima por padrão.
        
        Args:
            bot_token: Token do bot do Telegram (ou usa variável de ambiente TELEGRAM_BOT_TOKEN, ou token do Sentinel)
            chat_id: ID do chat (ou usa variável de ambiente TELEGRAM_CHAT_ID)
        """
        # Token do bot Sentinel (mesmo usado no photos-maxima e orders-rejects)
        SENTINEL_BOT_TOKEN = "8535974979:AAEJU7Ek_gz-esL7zbMeYVt6FZgCQwx4C-8"
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN", "") or os.getenv("TOKEN_TELEGRAM", "") or SENTINEL_BOT_TOKEN
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID", "")

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
            print("[AVISO] TELEGRAM_BOT_TOKEN não configurado. Mensagem não enviada.")
            return None
        
        chat_id_final = chat_id or self.chat_id
        
        if not chat_id_final:
            print("[AVISO] TELEGRAM_CHAT_ID não configurado. Mensagem não enviada.")
            return None
        
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
            result = response.json()
            if result.get("ok") and "result" in result:
                return result["result"].get("message_id")
            return None
        except requests.RequestException as exc:
            print(f"[ERRO] Falha ao enviar mensagem para Telegram: {exc}")
            if hasattr(exc, 'response') and exc.response is not None:
                try:
                    error_data = exc.response.json()
                    print(f"[ERRO] Detalhes: {error_data}")
                except:
                    pass
            return None

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
            print("[AVISO] TELEGRAM_BOT_TOKEN não configurado. Mensagem não deletada.")
            return False
        
        chat_id_final = chat_id or self.chat_id
        
        if not chat_id_final:
            print("[AVISO] TELEGRAM_CHAT_ID não configurado. Mensagem não deletada.")
            return False
        
        url = f"https://api.telegram.org/bot{self.bot_token}/deleteMessage"
        
        payload = {
            "chat_id": chat_id_final,
            "message_id": message_id
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()
            return result.get("ok", False)
        except requests.RequestException as exc:
            print(f"[ERRO] Falha ao deletar mensagem: {exc}")
            if hasattr(exc, 'response') and exc.response is not None:
                try:
                    error_data = exc.response.json()
                    print(f"[ERRO] Detalhes: {error_data}")
                except:
                    pass
            return False

    def notificar_execucao_servico(self, nome_servico: str = "Serviço de Vendedor de Férias") -> Optional[int]:
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
            f"🤖 <b>{nome_servico}</b>\n\n"
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


# Função de compatibilidade para manter o código existente funcionando
def enviar_mensagem_telegram(mensagem: str) -> bool:
    """
    Função de compatibilidade para manter o código existente funcionando.
    Usa a classe TelegramService internamente.
    """
    service = TelegramService()
    message_id = service.enviar_mensagem(mensagem)
    return message_id is not None
