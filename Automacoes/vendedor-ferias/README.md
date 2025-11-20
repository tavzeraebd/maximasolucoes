# 📅 Sistema de Sincronização de Vendedor Férias

Sistema automatizado desenvolvido em Python para sincronizar informações de férias de vendedores entre as APIs Winthor e Máxima.

## 🎯 Objetivo

Este sistema realiza a sincronização automática de dados de férias de vendedores:
1. Autentica na API Winthor
2. Obtém lista de vendedores de férias
3. Autentica na API Máxima
4. Atualiza os registros de férias na API Máxima

## 📋 Requisitos

- **Python**: 3.8 ou superior
- **Acesso às APIs**: Winthor e Máxima

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd Automacoes/vendedor-ferias
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

**Dependências:**
- `requests>=2.31.0` - Requisições HTTP
- `python-dotenv>=1.0.1` - Carregamento de variáveis de ambiente

### 3. Configure as variáveis de ambiente

Copie o arquivo `env.example` para `.env`:

```bash
cp env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
# Credenciais de Autenticação
USERNAME_WINTHOR=seu_usuario
PASSWORD_WINTHOR=sua_senha

# URLs da API Winthor
WINTHOR_OAUTH_URL=https://api.exemplo.com/oauth2/v1/access-token
WINTHOR_VENDEDOR_FERIAS_URL=https://api.exemplo.com/maxima/vendedor-ferias

# URLs da API Máxima
MAXIMA_LOGIN_URL=https://servidor.exemplo.com:81/api/v1/Login
MAXIMA_FERIAS_URL=https://servidor.exemplo.com:81/api/v1/FeriasVendedor/Atualizar

# Configurações de Timeout (opcional)
API_TIMEOUT=30
```

## 📁 Estrutura do Projeto

```
vendedor-ferias/
├── vendedor-ferias-v1.py    # Script principal
├── config.py                 # Configurações centralizadas
├── env.example               # Template de configuração
├── requirements.txt          # Dependências Python
├── .gitignore               # Arquivos ignorados pelo Git
└── README.md                # Este arquivo
```

## 🔧 Configuração

### Variáveis de Ambiente Obrigatórias

- `USERNAME_WINTHOR`: Usuário para autenticação nas APIs
- `PASSWORD_WINTHOR`: Senha para autenticação nas APIs
- `WINTHOR_OAUTH_URL`: URL do endpoint de autenticação OAuth2 do Winthor
- `WINTHOR_VENDEDOR_FERIAS_URL`: URL do endpoint de vendedores de férias do Winthor
- `MAXIMA_LOGIN_URL`: URL do endpoint de login da API Máxima
- `MAXIMA_FERIAS_URL`: URL do endpoint de atualização de férias da API Máxima

### Variáveis de Ambiente Opcionais

- `API_TIMEOUT`: Timeout para requisições HTTP em segundos (padrão: 30)

## 🚀 Execução

### Execução Manual

```bash
python vendedor-ferias-v1.py
```

### Execução via Agendador (Windows Task Scheduler)

1. Abra o **Agendador de Tarefas** (Task Scheduler)
2. Crie uma nova tarefa
3. Configure:
   - **Nome**: "Sincronização Vendedor Férias"
   - **Gatilho**: Conforme necessário (ex: diariamente)
   - **Ação**: Executar programa
   - **Programa**: `python.exe` (ou caminho completo)
   - **Argumentos**: `C:\caminho\para\Automacoes\vendedor-ferias\vendedor-ferias-v1.py`
   - **Diretório inicial**: `C:\caminho\para\Automacoes\vendedor-ferias`
4. Configure conta de usuário com acesso às APIs

## 📊 Como Funciona

### Fluxo de Execução

1. **Validação de Configuração**: Verifica se todas as variáveis de ambiente obrigatórias estão configuradas
2. **Autenticação Winthor**: Obtém token de acesso da API Winthor usando OAuth2
3. **Obtenção de Dados**: Consulta lista de vendedores de férias na API Winthor
4. **Autenticação Máxima**: Obtém token de acesso da API Máxima
5. **Atualização**: Para cada vendedor, envia os dados de férias para a API Máxima

### Tratamento de Erros

- **Erro de Configuração**: Exibe mensagem clara sobre variáveis faltantes
- **Erro de Autenticação**: Interrompe execução e exibe mensagem de erro
- **Erro de Conexão**: Loga erro e continua com próximo registro (quando aplicável)
- **Erro de API**: Loga resposta da API para análise

## 📝 Logs

O sistema utiliza logs coloridos no console:

- **INFO** (Azul): Informações gerais do processo
- **OK** (Verde): Operações concluídas com sucesso
- **ERRO** (Vermelho): Erros e falhas
- **FIM** (Amarelo): Mensagens de início e fim do processo

## 🔍 Troubleshooting

### Problema: Erro de configuração

- Verifique se o arquivo `.env` existe na raiz do diretório `vendedor-ferias`
- Verifique se todas as variáveis obrigatórias estão preenchidas
- Verifique se não há espaços extras ou caracteres especiais nas variáveis

### Problema: Falha na autenticação Winthor

- Verifique se `USERNAME_WINTHOR` e `PASSWORD_WINTHOR` estão corretos
- Verifique se `WINTHOR_OAUTH_URL` está correto e acessível
- Verifique conectividade de rede com a API

### Problema: Falha na autenticação Máxima

- Verifique se as credenciais estão corretas (mesmas do Winthor)
- Verifique se `MAXIMA_LOGIN_URL` está correto e acessível
- Verifique se o servidor está acessível na porta especificada

### Problema: Falha ao obter vendedores de férias

- Verifique se o token de autenticação foi obtido com sucesso
- Verifique se `WINTHOR_VENDEDOR_FERIAS_URL` está correto
- Verifique permissões do usuário na API Winthor

### Problema: Falha ao atualizar férias

- Verifique se o token da API Máxima foi obtido com sucesso
- Verifique se `MAXIMA_FERIAS_URL` está correto
- Verifique permissões do usuário na API Máxima
- Verifique o formato dos dados enviados

## 🔒 Segurança

- **Nunca commite o arquivo `.env`** - Ele está protegido pelo `.gitignore`
- **Use credenciais fortes** para as APIs
- **Mantenha as URLs das APIs privadas** - Não compartilhe informações sensíveis
- **Revise as permissões** do usuário nas APIs regularmente

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

1. Verifique os logs de execução
2. Verifique configurações em `config.py` e `.env`
3. Verifique conectividade com as APIs
4. Verifique credenciais e permissões

---

**Desenvolvido para sincronização de dados entre APIs Winthor e Máxima.**

