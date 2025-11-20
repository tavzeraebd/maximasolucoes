import requests
import base64
import os
from utils.logger import log
from utils.telegram import enviar_mensagem_telegram

def consultar_vendedores():
    winthor_auth_url = "https://api.ebdgrupo.com.br/oauth2/v1/access-token"
    winthor_api_url = "https://api.ebdgrupo.com.br/maxima/vendedor-ferias"

    winthor_client_id = os.getenv("WINTHOR_CLIENT_ID")
    winthor_client_secret = os.getenv("WINTHOR_CLIENT_SECRET")

    if not winthor_client_id or not winthor_client_secret:
        log("ERRO", "WINTHOR_CLIENT_ID ou WINTHOR_CLIENT_SECRET não encontrados no .env")
        enviar_mensagem_telegram("🚨 <b>Erro crítico:</b> Variáveis de ambiente do Winthor não encontradas.")
        exit(1)

    try:
        log("INFO", "Iniciando autenticação no Winthor...")
        credenciais_b64 = base64.b64encode(f"{winthor_client_id}:{winthor_client_secret}".encode()).decode()
        auth_headers = {
            "Authorization": f"Basic {credenciais_b64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        auth_data = {"grant_type": "client_credentials"}

        resp_auth = requests.post(winthor_auth_url, headers=auth_headers, data=auth_data)
        resp_auth.raise_for_status()

        access_token = resp_auth.json().get("access_token")
        log("OK", "Token Winthor gerado com sucesso!")

        log("INFO", "Consultando vendedores de férias no Winthor...")
        api_headers = {"Authorization": f"Bearer {access_token}"}
        resp_vendedores = requests.get(winthor_api_url, headers=api_headers)
        resp_vendedores.raise_for_status()

        vendedores = resp_vendedores.json()
        log("OK", "Consulta de vendedores realizada com sucesso!")

        return vendedores

    except Exception as e:
        log("ERRO", f"Falha Winthor: {e}")
        enviar_mensagem_telegram(f"🚨 <b>Erro crítico na autenticação ou consulta Winthor:</b>\n{str(e)}")
        exit(1)
