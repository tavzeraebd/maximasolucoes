import os
import sys
import requests
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# ===== Função para exibir mensagens de log =====
def log(mensagem, tipo="INFO"):
    cores = {
        "INFO": "\033[94m",   # Azul
        "OK": "\033[92m",     # Verde
        "ERRO": "\033[91m",   # Vermelho
        "FIM": "\033[93m"     # Amarelo
    }
    reset = "\033[0m"
    print(f"{cores.get(tipo, '')}[{tipo}] {mensagem}{reset}")

# ===== Passo 1: Autenticação Winthor =====
def autenticar_winthor():
    log("Iniciando autenticação na API Winthor...")

    url = "https://api.ebdgrupo.com.br/oauth2/v1/access-token"
    payload = {
        "username": os.getenv("username-winthor"),
        "password": os.getenv("password-winthor")
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            dados = response.json()
            access_token = dados.get("access_token")
            if access_token:
                log("Autenticação realizada com sucesso!", "OK")
                return access_token
        log(f"Falha na autenticação Winthor: {response.text}", "ERRO")
        sys.exit(1)
    except Exception as e:
        log(f"Erro de conexão: {e}", "ERRO")
        sys.exit(1)

# ===== Passo 2: Obter vendedores de férias =====
def obter_vendedores_ferias(access_token):
    log("Consultando vendedores de férias na API Winthor...")

    url = "https://api.ebdgrupo.com.br/maxima/vendedor-ferias"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            vendedores = response.json()
            log(f"Foram encontrados {len(vendedores)} registros de férias.", "OK")
            return vendedores
        log(f"Falha ao obter dados: {response.text}", "ERRO")
        sys.exit(1)
    except Exception as e:
        log(f"Erro de conexão: {e}", "ERRO")
        sys.exit(1)

# ===== Passo 3: Autenticação Máxima =====
def autenticar_maxima():
    log("Iniciando autenticação na API Máxima...")

    url = "https://intext-04.solucoesmaxima.com.br:81/api/v1/Login"
    payload = {
        "username": os.getenv("username-maxima"),
        "password": os.getenv("password-maxima")
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            dados = response.json()
            log(dados.get("resposta", "Sem resposta"), "OK")
            token_maxima = dados.get("token_De_Acesso")
            if token_maxima:
                return token_maxima
        log(f"Falha na autenticação Máxima: {response.text}", "ERRO")
        sys.exit(1)
    except Exception as e:
        log(f"Erro de conexão: {e}", "ERRO")
        sys.exit(1)

# ===== Passo 4: Atualizar férias na API Máxima =====
def atualizar_ferias_maxima(token_maxima, vendedores):
    log("Enviando dados de férias para API Máxima...")

    url = "https://intext-04.solucoesmaxima.com.br:81/api/v1/FeriasVendedor/Atualizar"
    headers = {"Authorization": f"Bearer {token_maxima}"}

    for vendedor in vendedores:
        payload = [vendedor]
        log(f"Enviando férias do vendedor {vendedor['codigoVendedorErp']}...")
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                log(f"Registro enviado com sucesso: {response.text}", "OK")
            else:
                log(f"Falha ao enviar registro: {response.text}", "ERRO")
        except Exception as e:
            log(f"Erro de conexão: {e}", "ERRO")

# ===== Execução principal =====
if __name__ == "__main__":
    log("===== INÍCIO DO PROCESSO =====", "FIM")

    token_winthor = autenticar_winthor()
    vendedores_ferias = obter_vendedores_ferias(token_winthor)
    token_maxima = autenticar_maxima()
    atualizar_ferias_maxima(token_maxima, vendedores_ferias)

    log("===== PROCESSO FINALIZADO =====", "FIM")
