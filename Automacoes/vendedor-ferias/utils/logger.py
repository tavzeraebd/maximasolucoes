# utils/logger.py
from datetime import datetime
from pathlib import Path

# Garante que o diretório 'reports' exista
LOG_DIR = Path("reports")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "log-execucao.txt"

log_summary = {
    "OK": [],
    "ERRO": []
}

def log(msg_type: str, message: str) -> None:
    """
    Registra uma mensagem de log no terminal, arquivo e Telegram (se aplicável).
    
    Args:
        msg_type: Tipo da mensagem (INFO, OK, ERRO)
        message: Texto da mensagem
    """
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    emojis = {"INFO": "ℹ️", "OK": "✅", "ERRO": "❌"}
    colors = {"INFO": "\033[94m", "OK": "\033[92m", "ERRO": "\033[91m"}

    emoji = emojis.get(msg_type, "")
    color = colors.get(msg_type, "\033[0m")
    reset = "\033[0m"
    formatted_msg = f"[ {msg_type} ] - {timestamp} - {message}"

    # Print no terminal com cor
    print(f"{color}{formatted_msg}{reset}")

    # Log em arquivo (sem cor)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted_msg + "\n")
    except Exception as e:
        print(f"[ERRO] Falha ao escrever no arquivo de log: {e}")

    # Adiciona ao resumo se for OK ou ERRO
    if msg_type in ["OK", "ERRO"]:
        log_summary[msg_type].append(f"{emoji} {message}")

def obter_resumo() -> dict:
    """
    Retorna um dicionário com o resumo da execução.
    
    Returns:
        Dicionário com total_ok, total_erro e lista de erros
    """
    return {
        "total_ok": len(log_summary["OK"]),
        "total_erro": len(log_summary["ERRO"]),
        "erros": log_summary["ERRO"].copy()
    }

def limpar_resumo() -> None:
    """
    Limpa o resumo de logs.
    """
    log_summary["OK"] = []
    log_summary["ERRO"] = []
