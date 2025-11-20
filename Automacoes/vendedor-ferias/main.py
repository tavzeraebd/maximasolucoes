from dotenv import load_dotenv
from services.winthor_service import consultar_vendedores
from services.maxima_service import login_maxima, enviar_vendedores
from utils.logger import log, obter_resumo, limpar_resumo
from utils.telegram import TelegramService
from datetime import datetime
import os

# =========================
# Início da execução principal
# =========================
if __name__ == "__main__":
    load_dotenv()
    log("INFO", "Variáveis de ambiente carregadas.")

    # Data/hora de início do processamento
    data_inicio = datetime.now()
    data_inicio_str = data_inicio.strftime('%d/%m/%Y %H:%M:%S')

    print("")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     MaxPedido - Vendedor de Férias                         ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"  Iniciado em: {data_inicio_str}")
    print("")

    log("INFO", "SCRIPT INICIADO")

    # Enviar mensagem inicial no Telegram
    message_id_inicial = None
    try:
        telegram_service = TelegramService()
        mensagem_inicial = (
            f"🤖 <b>MaxPedido - Vendedor de Férias</b>\n\n"
            f"🕐 Iniciado em: {data_inicio_str}"
        )
        message_id_inicial = telegram_service.enviar_mensagem(mensagem_inicial)
        if not message_id_inicial:
            log("ERRO", "Falha ao enviar mensagem inicial para o Telegram.")
    except Exception as exc:
        log("ERRO", f"Erro ao enviar mensagem inicial: {exc}")

    # Executar o processamento
    erro_ocorrido = False
    mensagem_erro = None
    try:
        vendedores = consultar_vendedores()
        token_maxima = login_maxima(os.getenv("MAXIMA_CLIENT_ID"), os.getenv("MAXIMA_CLIENT_SECRET"))
        enviar_vendedores(vendedores, token_maxima)
    except KeyboardInterrupt:
        log("ERRO", "Processamento interrompido pelo usuário (Ctrl+C)")
        erro_ocorrido = True
        mensagem_erro = "Processamento interrompido pelo usuário"
    except Exception as e:
        log("ERRO", f"Erro na execução principal: {e}")
        erro_ocorrido = True
        mensagem_erro = str(e)
    finally:
        # Data/hora de fim do processamento
        data_fim = datetime.now()
        data_fim_str = data_fim.strftime('%d/%m/%Y %H:%M:%S')

        # Obter resumo da execução
        resumo = obter_resumo()
        total_ok = resumo["total_ok"]
        total_erro = resumo["total_erro"]
        erros = resumo["erros"]

        # Deletar mensagem inicial e enviar mensagem final
        if message_id_inicial:
            try:
                telegram_service = TelegramService()
                # Deletar mensagem inicial
                if not telegram_service.deletar_mensagem(message_id_inicial):
                    log("ERRO", "Falha ao deletar mensagem inicial.")
                
                # Enviar mensagem final
                if erro_ocorrido or total_erro > 0:
                    mensagem_final = (
                        f"🤖 <b>MaxPedido - Vendedor de Férias</b>\n\n"
                        f"❌ <b>ERRO</b>\n"
                        f"🕐 Iniciado em: {data_inicio_str}\n"
                        f"🕐 Finalizado em: {data_fim_str}\n"
                        f"✅ Sucessos: {total_ok} - ❌ Erros: {total_erro}"
                    )
                    if mensagem_erro:
                        mensagem_final += f"\n\n⚠️ {mensagem_erro}"
                    if erros:
                        mensagem_final += "\n\n🧾 <b>Erros encontrados:</b>\n"
                        # Limita a 10 erros para não exceder o limite do Telegram
                        erros_formatados = erros[:10]
                        mensagem_final += "\n".join(erros_formatados)
                        if len(erros) > 10:
                            mensagem_final += f"\n\n... e mais {len(erros) - 10} erro(s)"
                else:
                    mensagem_final = (
                        f"🤖 <b>MaxPedido - Vendedor de Férias</b>\n\n"
                        f"✅ <b>CONCLUÍDO</b>\n"
                        f"🕐 Iniciado em: {data_inicio_str}\n"
                        f"🕐 Finalizado em: {data_fim_str}\n"
                        f"✅ Sucessos: {total_ok} - ❌ Erros: {total_erro}"
                    )
                
                if not telegram_service.enviar_mensagem(mensagem_final):
                    log("ERRO", "Falha ao enviar mensagem final para o Telegram.")
            except Exception as exc:
                log("ERRO", f"Erro ao processar mensagens finais: {exc}")

        if erro_ocorrido or total_erro > 0:
            log("ERRO", "SCRIPT FINALIZADO COM ERRO")
        else:
            log("INFO", "SCRIPT FINALIZADO COM SUCESSO")
        
        # Limpar resumo para próxima execução
        limpar_resumo()

