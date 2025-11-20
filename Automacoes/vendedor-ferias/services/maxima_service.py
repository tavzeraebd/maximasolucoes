import requests
from utils.logger import log
from utils.telegram import enviar_mensagem_telegram

def login_maxima(usuario, senha):
    maxima_login_url = "https://intext-04.solucoesmaxima.com.br:81/api/v1/Login"

    if not usuario or not senha:
        log("ERRO", "MAXIMA_CLIENT_ID ou MAXIMA_CLIENT_SECRET não encontrados no .env")
        enviar_mensagem_telegram("🚨 <b>Erro crítico:</b> Variáveis de ambiente da Maxima não encontradas.")
        exit(1)

    try:
        log("INFO", "Iniciando login na Maxima...")
        payload_login = {"login": usuario, "password": senha}
        resp_login = requests.post(maxima_login_url, json=payload_login)
        resp_login.raise_for_status()

        token_maxima = resp_login.json().get("token_De_Acesso")
        if not token_maxima:
            log("ERRO", "Token de acesso da Maxima não encontrado.")
            enviar_mensagem_telegram("🚨 <b>Erro crítico:</b> Token de acesso da Maxima ausente.")
            exit(1)

        log("OK", "Login Maxima realizado com sucesso!")
        return token_maxima

    except Exception as e:
        log("ERRO", f"Falha login Maxima: {e}")
        enviar_mensagem_telegram(f"🚨 <b>Erro crítico no login Maxima:</b>\n{str(e)}")
        exit(1)


def enviar_vendedores(vendedores, token_maxima):
    maxima_post_url = "https://intext-04.solucoesmaxima.com.br:81/api/v1/FeriasVendedor/Atualizar"
    maxima_headers = {"Authorization": f"Bearer {token_maxima}", "Content-Type": "application/json"}

    log("INFO", "Preparando envio dos vendedores para a Maxima...")

    if isinstance(vendedores, dict) and "vendedores" in vendedores:
        lista_vendedores = vendedores["vendedores"]
    elif isinstance(vendedores, dict):
        lista_vendedores = [vendedores]
    else:
        lista_vendedores = vendedores

    log("INFO", f"Total de vendedores a enviar: {len(lista_vendedores)}")

    for v in lista_vendedores:
        payload_ferias = [
            {
                "codigoVendedorErp": v.get("codigoVendedorErp"),
                "dataInicioFerias": v.get("dataInicioFerias"),
                "dataFimFerias": v.get("dataFimFerias")
            }
        ]
        try:
            resp_envio = requests.post(maxima_post_url, json=payload_ferias, headers=maxima_headers)

            if resp_envio.status_code == 200:
                resp_json = resp_envio.json()
                if not resp_json.get("success"):
                    log("ERRO", f"Falha no envio do vendedor {v.get('codigoVendedorErp')}: resposta vazia da integradora. Detalhes: {resp_json}")
                else:
                    log("OK", f"Vendedor {v.get('codigoVendedorErp')} enviado com sucesso!")
            else:
                log("ERRO", f"Falha ao enviar vendedor {v.get('codigoVendedorErp')}. Status: {resp_envio.status_code}")
        except Exception as e:
            log("ERRO", f"Exceção ao enviar vendedor {v.get('codigoVendedorErp')}: {e}")
