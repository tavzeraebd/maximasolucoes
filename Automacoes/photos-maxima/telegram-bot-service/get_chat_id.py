# get_chat_id.py
"""
Script auxiliar para obter o CHAT_ID do Telegram.

Como usar:
1. Configure o TELEGRAM_BOT_TOKEN no .env ou passe como argumento
2. Envie uma mensagem para o bot no Telegram
3. Execute este script: python get_chat_id.py
4. O script retornará o CHAT_ID que você deve adicionar ao .env
"""
import requests
import os
import sys
from pathlib import Path


def obter_chat_id(bot_token: str = None):
    """
    Obtém o CHAT_ID do último update do bot.
    
    Args:
        bot_token: Token do bot (ou usa variável de ambiente TELEGRAM_BOT_TOKEN)
    
    Returns:
        CHAT_ID encontrado ou None
    """
    token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN", "")
    
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN não encontrado!")
        print("\nConfigure de uma das seguintes formas:")
        print("  1. Variável de ambiente: export TELEGRAM_BOT_TOKEN='seu_token'")
        print("  2. Arquivo .env: TELEGRAM_BOT_TOKEN=seu_token")
        print("  3. Passar como argumento: python get_chat_id.py seu_token")
        return None
    
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("ok") and data.get("result"):
            updates = data["result"]
            if updates:
                # Pegar o último update
                ultimo_update = updates[-1]
                chat_id = ultimo_update.get("message", {}).get("chat", {}).get("id")
                
                if chat_id:
                    print(f"\n✅ CHAT_ID encontrado: {chat_id}")
                    print(f"\nAdicione ao seu arquivo .env:")
                    print(f"TELEGRAM_CHAT_ID={chat_id}\n")
                    return chat_id
                else:
                    print("❌ Não foi possível extrair o CHAT_ID do último update.")
            else:
                print("⚠️  Nenhuma mensagem encontrada.")
                print("   Envie uma mensagem para o bot primeiro e execute este script novamente.")
        else:
            print("❌ Erro ao obter updates do bot.")
            if not data.get("ok"):
                print(f"   Descrição: {data.get('description', 'Erro desconhecido')}")
            
    except requests.RequestException as exc:
        print(f"❌ Erro ao conectar com a API do Telegram: {exc}")
    
    return None


if __name__ == "__main__":
    # Tentar carregar .env se existir
    try:
        from dotenv import load_dotenv
        env_path = Path('.') / '.env'
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
    except ImportError:
        pass  # dotenv não é obrigatório
    
    # Verificar se token foi passado como argumento
    bot_token = sys.argv[1] if len(sys.argv) > 1 else None
    
    print("🔍 Buscando CHAT_ID do Telegram...")
    obter_chat_id(bot_token)

