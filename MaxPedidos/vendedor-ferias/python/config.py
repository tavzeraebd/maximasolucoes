"""
Configurações centralizadas do sistema de Vendedor Férias.
Todas as variáveis são carregadas do arquivo .env
"""
import os
from dotenv import load_dotenv

# Carrega variáveis do .env (se existir)
load_dotenv()

# Credenciais de Autenticação
USERNAME_WINTHOR = os.getenv("USERNAME_WINTHOR", "")
PASSWORD_WINTHOR = os.getenv("PASSWORD_WINTHOR", "")

# URLs da API Winthor
WINTHOR_OAUTH_URL = os.getenv("WINTHOR_OAUTH_URL", "")
WINTHOR_VENDEDOR_FERIAS_URL = os.getenv("WINTHOR_VENDEDOR_FERIAS_URL", "")

# URLs da API Máxima
MAXIMA_LOGIN_URL = os.getenv("MAXIMA_LOGIN_URL", "")
MAXIMA_FERIAS_URL = os.getenv("MAXIMA_FERIAS_URL", "")

# Configurações de Timeout
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

# Validação de configurações obrigatórias
def validar_configuracao():
    """Valida se todas as configurações obrigatórias estão definidas."""
    erros = []
    
    if not USERNAME_WINTHOR:
        erros.append("USERNAME_WINTHOR não configurado no arquivo .env")
    if not PASSWORD_WINTHOR:
        erros.append("PASSWORD_WINTHOR não configurado no arquivo .env")
    if not WINTHOR_OAUTH_URL:
        erros.append("WINTHOR_OAUTH_URL não configurado no arquivo .env")
    if not WINTHOR_VENDEDOR_FERIAS_URL:
        erros.append("WINTHOR_VENDEDOR_FERIAS_URL não configurado no arquivo .env")
    if not MAXIMA_LOGIN_URL:
        erros.append("MAXIMA_LOGIN_URL não configurado no arquivo .env")
    if not MAXIMA_FERIAS_URL:
        erros.append("MAXIMA_FERIAS_URL não configurado no arquivo .env")
    
    if erros:
        raise ValueError("\n".join(erros))
    
    return True

