# Telegram Bot Service com Scheduler

Serviço independente e reutilizável para envio de mensagens via Telegram Bot API com sistema de agendamento automático em projetos Python.

## 📋 Requisitos

- Python 3.7+
- Biblioteca `requests`

## 🚀 Instalação

1. Copie a pasta `telegram-bot-service` para o seu projeto
2. Instale as dependências:

```bash
pip install requests python-dotenv
```

## ⚙️ Configuração

### Opção 1: Variáveis de Ambiente

Crie um arquivo `.env` na raiz do seu projeto:

```env
TELEGRAM_BOT_TOKEN=seu_bot_token_aqui
TELEGRAM_CHAT_ID=seu_chat_id_aqui
```

### Opção 2: Passar Credenciais Diretamente

Você também pode passar as credenciais diretamente ao inicializar o serviço:

```python
telegram = TelegramService(
    bot_token="seu_bot_token",
    chat_id="seu_chat_id"
)
```

## 📖 Como Obter o CHAT_ID

1. Envie uma mensagem para o seu bot no Telegram
2. Execute o script auxiliar:

```bash
python telegram-bot-service/get_chat_id.py
```

Ou passe o token como argumento:

```bash
python telegram-bot-service/get_chat_id.py seu_bot_token
```

## 💻 Uso Básico

### TelegramService - Envio de Mensagens

```python
from telegram_service import TelegramService

# Inicializar o serviço (usa variáveis de ambiente)
service = TelegramService()

# Enviar mensagem simples
service.enviar_mensagem("Olá! Esta é uma mensagem de teste.")

# Enviar notificação de serviço
service.notificar_execucao_servico("Meu Serviço")
```

### SchedulerService - Agendamento Automático

```python
from telegram_service import TelegramService
from scheduler_service import SchedulerService

# Criar serviço de Telegram
telegram = TelegramService()

# Criar scheduler (envia notificação a cada hora cheia)
scheduler = SchedulerService(
    telegram_service=telegram,
    nome_servico="Meu Serviço Automatizado"
)

# Iniciar scheduler
scheduler.iniciar()

try:
    # Manter o programa rodando
    scheduler.aguardar()
except KeyboardInterrupt:
    scheduler.parar()
```

## 🎯 Características do Scheduler

O `SchedulerService` possui as seguintes características:

- ✅ **Execução em horas cheias**: Envia notificações automaticamente às 10:00, 11:00, 12:00, etc.
- ✅ **Thread separada**: Roda em background sem bloquear o programa principal
- ✅ **Thread daemon**: Encerra automaticamente quando o programa principal termina
- ✅ **Monitoramento de threads**: Pode listar todas as threads ativas
- ✅ **Tratamento de erros**: Continua funcionando mesmo em caso de erros temporários
- ✅ **Logs detalhados**: Mostra informações sobre próxima execução e status

## 📚 Métodos Disponíveis

### TelegramService

#### `enviar_mensagem(mensagem, chat_id=None, parse_mode="HTML")`

Envia uma mensagem formatada para o Telegram.

**Parâmetros:**
- `mensagem` (str): Texto da mensagem
- `chat_id` (str, opcional): ID do chat (usa o configurado se None)
- `parse_mode` (str, opcional): Modo de parsing ("HTML", "Markdown", ou None)

**Retorna:** `bool` - True se enviado com sucesso

#### `enviar_mensagem_simples(texto, chat_id=None)`

Envia uma mensagem de texto simples (sem formatação).

#### `notificar_execucao_servico(nome_servico="Serviço")`

Envia uma notificação padrão informando que o serviço rodou.

### SchedulerService

#### `iniciar()`

Inicia o agendador em uma thread separada. O scheduler calculará automaticamente a próxima hora cheia e aguardará até esse momento.

#### `parar()`

Para o agendador e encerra a thread.

#### `aguardar()`

Aguarda a thread do agendador (útil para manter o programa rodando). Use Ctrl+C para interromper.

#### `listar_threads()`

Lista todas as threads ativas no programa.

## 🔧 Integração com Outros Projetos

### 1. Copie a pasta para seu projeto

```bash
cp -r telegram-bot-service /caminho/do/seu/projeto/
```

### 2. Importe os serviços

```python
from telegram_bot_service.telegram_service import TelegramService
from telegram_bot_service.scheduler_service import SchedulerService
```

Ou se estiver na mesma pasta:

```python
from telegram_service import TelegramService
from scheduler_service import SchedulerService
```

### 3. Use em seu código

```python
# Executar seu serviço principal
executar_meu_servico()

# Iniciar scheduler para notificações periódicas
telegram = TelegramService()
scheduler = SchedulerService(
    telegram_service=telegram,
    nome_servico="Meu Serviço"
)
scheduler.iniciar()

# Manter o programa rodando
try:
    scheduler.aguardar()
except KeyboardInterrupt:
    scheduler.parar()
```

## 📝 Exemplo Completo

```python
from telegram_service import TelegramService
from scheduler_service import SchedulerService

def main():
    # 1. Executar seu serviço principal
    print("Executando serviço principal...")
    # seu_codigo_aqui()
    
    # 2. Configurar Telegram e Scheduler
    telegram = TelegramService()
    scheduler = SchedulerService(
        telegram_service=telegram,
        nome_servico="Meu Serviço de Processamento"
    )
    
    # 3. Iniciar scheduler
    scheduler.iniciar()
    
    # 4. Manter o programa rodando
    try:
        scheduler.aguardar()
    except KeyboardInterrupt:
        print("\n[SCHEDULER] Encerrando...")
        scheduler.parar()

if __name__ == "__main__":
    main()
```

## 🐛 Tratamento de Erros

Os serviços retornam `False` em caso de erro e imprimem mensagens de aviso no console. O scheduler continua funcionando mesmo em caso de erros temporários, tentando novamente na próxima hora cheia.

## 📊 Monitoramento de Threads

Você pode verificar as threads ativas a qualquer momento:

```python
from thread_monitor import ThreadMonitor

# Listar todas as threads
ThreadMonitor.imprimir_threads_ativas()

# Contar threads
total = ThreadMonitor.contar_threads_ativas()
```

## 📄 Estrutura de Arquivos

```
telegram-bot-service/
├── __init__.py              # Inicialização do pacote
├── telegram_service.py      # Serviço de Telegram
├── scheduler_service.py     # Serviço de agendamento
├── thread_monitor.py        # Utilitário para monitorar threads
├── get_chat_id.py          # Script auxiliar para obter CHAT_ID
├── example_usage.py        # Exemplos de uso
├── requirements.txt        # Dependências
└── README.md              # Esta documentação
```

## 📄 Licença

Este serviço é fornecido como está, livre para uso em qualquer projeto.

## 🤝 Contribuindo

Sinta-se à vontade para adaptar e melhorar este serviço conforme suas necessidades!

