# 📸 Sistema de Processamento de Imagens - Photos Maxima

Sistema automatizado de processamento de imagens desenvolvido em Python que monitora um diretório de origem, processa novas imagens (conversão, redimensionamento e compressão), copia para um destino e integra com API externa e Telegram para notificações.

## 🎯 Características

- **Processamento Pontual**: Execução sob demanda via agendador (Task Scheduler)
- **Janela Temporal Inteligente**: Processa apenas imagens novas desde a última execução
- **Otimização Automática**: Redimensiona e comprime imagens para tamanho otimizado
- **Backup Automático**: Preserva arquivos existentes antes de sobrescrever
- **Integração API**: Notifica sistema externo sobre atualizações
- **Notificações Telegram**: Informa sobre execuções e resultados
- **Logs Separados**: Log geral e log específico de fotos processadas
- **Resiliência**: Continua processando mesmo com erros em arquivos individuais
- **Suporte a Múltiplos Formatos**: Aceita 13+ formatos de imagem

## 📋 Requisitos

- **Python**: 3.10 ou superior
- **Sistema Operacional**: Windows (para integração com Task Scheduler) ou Linux
- **Acesso de rede**: Acesso aos diretórios de origem e destino (compartilhamentos de rede)

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd photos-maxima
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

**Dependências principais:**
- `Pillow>=10.0.0` - Processamento de imagens
- `requests>=2.31.0` - Requisições HTTP (API e Telegram)
- `python-dotenv>=1.0.1` - Carregamento de variáveis de ambiente

### 3. Configure as variáveis de ambiente

Copie o arquivo `env.example` para `.env` e configure as variáveis:

```bash
cp env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
# Diretórios de Origem e Destino
SOURCE_DIR=\\servidor\caminho\origem
DEST_DIR=\\servidor\caminho\destino

# API Externa
API_BASE_URL=https://api.exemplo.com/products
API_ENABLED=true
API_TIMEOUT=15

# Telegram Bot
TELEGRAM_BOT_TOKEN=seu_token_aqui
TELEGRAM_CHAT_ID=seu_chat_id_aqui
TELEGRAM_ENABLED=true
TELEGRAM_TIMEOUT=10

# Configurações de Processamento de Imagens
IMAGE_MAX_WIDTH=225
IMAGE_QUALITY_INITIAL=50
IMAGE_QUALITY_MIN=10
IMAGE_MAX_SIZE_KB=100
IMAGE_COMPRESSION_STEP=5
IMAGE_MAX_ITERATIONS=12

# Configurações de Logging
APP_LOG_FILE=app.log
PHOTOS_LOG_FILE=photos.log
LOG_MAX_BYTES=2097152
LOG_BACKUP_COUNT=3
```

## 📁 Estrutura do Projeto

```
photos-maxima/
├── main.py                          # Ponto de entrada
├── config.py                        # Configurações centralizadas
├── requirements.txt                 # Dependências Python
├── env.example                      # Exemplo de arquivo de configuração
├── .gitignore                       # Arquivos ignorados pelo Git
│
├── services/                        # Serviços principais
│   ├── monitor_service.py          # Lógica de processamento pontual
│   ├── image_service.py            # Processamento de imagens
│   ├── api_service.py              # Integração com API externa
│   ├── telegram_service.py         # Envio de mensagens Telegram
│   ├── scheduler_service.py        # Agendamento de notificações
│   ├── state_service.py            # Persistência do estado
│   ├── logging_service.py          # Configuração de logs
│   └── lock_service.py             # Gerenciamento de lock file
│
├── utils/                           # Utilitários
│   └── file_utils.py               # Validação de arquivos de imagem
│
├── handlers/                        # Handlers de eventos
│   └── image_handler.py            # Handler de imagens
│
├── telegram-bot-service/            # Serviço independente de Telegram
│   ├── telegram_service.py         # Serviço reutilizável
│   ├── scheduler_service.py        # Agendador de notificações
│   ├── get_chat_id.py             # Script auxiliar para obter CHAT_ID
│   └── example_usage.py            # Exemplos de uso
│
└── logs/                            # Logs gerados em runtime
    ├── app.log                     # Log geral da aplicação
    ├── photos.log                  # Log apenas com nomes das fotos
    └── execution_state.json        # Estado da última execução
```

## 🔧 Configuração

### Variáveis de Ambiente Obrigatórias

- `SOURCE_DIR`: Diretório de origem onde as imagens serão monitoradas
- `DEST_DIR`: Diretório de destino onde as imagens processadas serão salvas

### Variáveis de Ambiente Opcionais

Consulte o arquivo `env.example` para ver todas as variáveis disponíveis e seus valores padrão.

### Obter CHAT_ID do Telegram

Execute o script auxiliar:

```bash
python telegram-bot-service/get_chat_id.py
```

Ou passe o token como argumento:

```bash
python telegram-bot-service/get_chat_id.py seu_bot_token
```

## 🚀 Execução

### Execução Manual

```bash
python main.py
```

### Execução via Agendador (Windows Task Scheduler)

1. Abra o **Agendador de Tarefas** (Task Scheduler)
2. Crie uma nova tarefa
3. Configure:
   - **Nome**: "Processamento de Imagens Photos Maxima"
   - **Gatilho**: Conforme necessário (ex: a cada hora)
   - **Ação**: Executar programa
   - **Programa**: `python.exe` (ou caminho completo)
   - **Argumentos**: `C:\caminho\para\photos-maxima\main.py`
   - **Diretório inicial**: `C:\caminho\para\photos-maxima`
4. Configure conta de usuário com acesso aos diretórios de rede

## 📊 Como Funciona

### Fluxo de Execução

1. **Cálculo da Janela Temporal**: O sistema calcula o intervalo desde a última execução até o momento atual
2. **Busca de Imagens**: Varre recursivamente o diretório de origem procurando imagens novas na janela temporal
3. **Processamento**: Para cada imagem encontrada:
   - Converte para RGB
   - Redimensiona (largura máxima configurável)
   - Comprime iterativamente até atingir tamanho alvo
   - Cria backup se arquivo já existe
   - Salva no destino
4. **Integração API**: Notifica API externa sobre atualização (se habilitado)
5. **Notificação Telegram**: Envia resumo da execução (se habilitado)
6. **Persistência**: Salva timestamp da execução para próxima vez

### Processamento de Imagens

- **Formato de saída**: JPEG
- **Largura máxima**: Configurável (padrão: 225px)
- **Tamanho alvo**: Configurável (padrão: ~100 KB)
- **Compressão iterativa**: Ajusta qualidade automaticamente até atingir tamanho desejado
- **Progressive JPEG**: Habilitado para melhor carregamento progressivo

### Formatos Suportados

- `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`
- `.tiff`, `.tif`, `.webp`, `.heic`, `.heif`
- `.raw`, `.cr2`, `.nef`, `.orf`, `.sr2`, `.ico`

## 📝 Logs

### Arquivo: `logs/app.log`

Contém logs gerais da aplicação:
- Início e fim de execuções
- Janelas temporais processadas
- Quantidade de arquivos encontrados
- Processamento de cada imagem
- Erros e exceções
- Chamadas à API
- Notificações Telegram

### Arquivo: `logs/photos.log`

Contém apenas nomes de arquivos processados (uma linha por foto).

### Arquivo: `logs/execution_state.json`

Armazena o timestamp da última execução para cálculo da próxima janela temporal.

**Rotação de Logs:**
- Tamanho máximo: 2 MB por arquivo (configurável)
- Backups mantidos: 3 (configurável)
- Arquivos antigos são removidos automaticamente

## 🛠️ Manutenção

### Limpeza de Logs

Os logs têm rotação automática. Para limpar manualmente:

```bash
# Windows
del logs\*.log.*

# Linux
rm logs/*.log.*
```

### Monitoramento

Verifique regularmente:
- `logs/app.log` - Para erros e avisos
- `logs/photos.log` - Para confirmar processamento
- `logs/execution_state.json` - Para verificar última execução

## 🔍 Troubleshooting

### Problema: Nenhuma imagem sendo processada

- Verifique acesso ao diretório de origem
- Verifique se há imagens na janela temporal
- Verifique `execution_state.json` (pode estar com data futura)
- Verifique logs em `logs/app.log`

### Problema: Erros de permissão

- Verifique credenciais do usuário que executa o agendador
- Verifique permissões nos diretórios de rede
- Verifique se o usuário tem acesso de leitura na origem e escrita no destino

### Problema: API não está sendo chamada

- Verifique `API_ENABLED=true` no `.env`
- Verifique `API_BASE_URL` está correto
- Verifique logs para erros de conexão

### Problema: Telegram não envia notificações

- Verifique `TELEGRAM_ENABLED=true`
- Verifique `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID`
- Use `get_chat_id.py` para verificar CHAT_ID
- Verifique logs para erros de conexão

## 📄 Licença

Este projeto é de uso interno da organização.

## 👥 Contribuições

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para questões ou problemas:

1. Verifique os logs em `logs/app.log`
2. Verifique configurações em `config.py` e `.env`
3. Verifique acesso aos diretórios de rede
4. Verifique credenciais do Telegram e API

---

**Desenvolvido para automação de processamento de imagens no ambiente Maxima/ERP.**
