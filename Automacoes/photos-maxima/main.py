import sys
import atexit
from datetime import datetime

from services.monitor_service import monitorar
from config import SOURCE_DIR, DESTINO, TELEGRAM_ENABLED
from services.logging_service import get_app_logger
from services.telegram_service import TelegramService
from services.lock_service import criar_lock, remover_lock

if __name__ == "__main__":
	logger = get_app_logger()
	
	# Criar lock file e garantir execução única
	if not criar_lock():
		logger.error("Não foi possível criar lock file. Outra instância pode estar rodando.")
		sys.exit(1)
	
	# Garantir que o lock seja removido ao sair
	atexit.register(remover_lock)
	
	dir_origem = str(SOURCE_DIR).strip()

	# Data/hora de início do processamento
	data_inicio = datetime.now()
	data_inicio_str = data_inicio.strftime('%d/%m/%Y %H:%M:%S')

	print("")
	print("╔════════════════════════════════════════════════════════════╗")
	print("║     MaxPedido - Monitor de Imagens                         ║")
	print("╚════════════════════════════════════════════════════════════╝")
	print(f"  Iniciado em: {data_inicio_str}")
	print("")

	logger.info("SCRIPT INICIADO")

	# Enviar mensagem inicial no Telegram
	message_id_inicial = None
	if TELEGRAM_ENABLED:
		try:
			telegram_service = TelegramService()
			mensagem_inicial = (
				f"🤖 <b>MaxPedido -Monitor de Imagenss</b>\n\n"
				f"🕐 Iniciado em: {data_inicio_str}"
			)
			message_id_inicial = telegram_service.enviar_mensagem(mensagem_inicial)
			if not message_id_inicial:
				logger.error("Falha ao enviar mensagem inicial para o Telegram.")
		except Exception as exc:
			logger.error(f"Erro ao enviar mensagem inicial: {exc}")

	# Executar o processamento
	erro_ocorrido = False
	mensagem_erro = None
	imagens_processadas = 0
	try:
		imagens_processadas = monitorar(dir_origem)
	except KeyboardInterrupt:
		logger.error("Processamento interrompido pelo usuário (Ctrl+C)")
		erro_ocorrido = True
		mensagem_erro = "Processamento interrompido pelo usuário"
		# Não fazer raise para permitir que o script termine normalmente
	except (PermissionError, OSError, FileNotFoundError) as exc:
		logger.error(f"Erro de acesso ao diretório: {exc}")
		erro_ocorrido = True
		mensagem_erro = f"Erro de acesso: {exc}"
		# Não fazer raise para permitir que o script termine normalmente
	except Exception as exc:
		logger.error(f"Erro durante o processamento: {exc}")
		erro_ocorrido = True
		mensagem_erro = f"Erro: {exc}"
		# Não fazer raise para permitir que o script termine normalmente
	finally:
		# Data/hora de fim do processamento
		data_fim = datetime.now()
		data_fim_str = data_fim.strftime('%d/%m/%Y %H:%M:%S')

		# Deletar mensagem inicial e enviar mensagem final
		if TELEGRAM_ENABLED and message_id_inicial:
			try:
				telegram_service = TelegramService()
				# Deletar mensagem inicial
				if not telegram_service.deletar_mensagem(message_id_inicial):
					logger.error("Falha ao deletar mensagem inicial.")
				
				# Enviar mensagem final
				if erro_ocorrido:
					mensagem_final = (
						f"🤖 <b>MaxPedido -Monitor de Imagenss</b>\n\n"
						f"❌ <b>ERRO</b>\n"
						f"🕐 Iniciado em: {data_inicio_str}\n"
						f"🕐 Finalizado em: {data_fim_str}\n"
						f"⚠️ {mensagem_erro}"
					)
				else:
					mensagem_final = (
						f"🤖 <b>MaxPedido -Monitor de Imagenss</b>\n\n"
						f"✅ <b>CONCLUÍDO</b>\n"
						f"🕐 Iniciado em: {data_inicio_str}\n"
						f"🕐 Finalizado em: {data_fim_str}\n"
						f"🖼️ Imagens processadas: {imagens_processadas}"
					)
				if not telegram_service.enviar_mensagem(mensagem_final):
					logger.error("Falha ao enviar mensagem final para o Telegram.")
			except Exception as exc:
				logger.error(f"Erro ao processar mensagens finais: {exc}")

		# Remover lock file antes de sair
		remover_lock()
		
		if erro_ocorrido:
			logger.error("SCRIPT FINALIZADO COM ERRO")
			sys.exit(1)  # Código de saída 1 indica erro
		else:
			logger.success("SCRIPT FINALIZADO")
			sys.exit(0)  # Código de saída 0 indica sucesso
