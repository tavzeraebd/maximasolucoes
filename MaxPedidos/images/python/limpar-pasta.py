import os
import shutil
import pandas as pd
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# Caminho para o arquivo Excel com os códigos válidos
CAMINHO_EXCEL = 'produtos.xlsx'

# Caminho para o diretório com as imagens originais
DIRETORIO_IMAGENS = 'A'

# Caminho para o diretório de destino (na mesma raiz do A)
DIRETORIO_DESTINO = 'resized'

# Cria o diretório de destino, se não existir
os.makedirs(DIRETORIO_DESTINO, exist_ok=True)

# 1️⃣ Ler o Excel e carregar os códigos válidos
print(f"Lendo lista de produtos válidos do arquivo: {CAMINHO_EXCEL}")
df = pd.read_excel(CAMINHO_EXCEL)

# Verifica se existe a coluna esperada
if 'CODPROD' not in df.columns:
    raise ValueError('A planilha precisa ter uma coluna chamada "CODPROD".')

# Pega os códigos válidos e transforma em conjunto (set) para busca rápida
codigos_validos = set(df['CODPROD'].astype(str).str.strip())
print(f"Total de códigos válidos carregados: {len(codigos_validos)}")

# 2️⃣ Percorrer os arquivos do diretório e verificar
arquivos = os.listdir(DIRETORIO_IMAGENS)
movidos = 0
mantidos = 0

for arquivo in arquivos:
    caminho_arquivo = os.path.join(DIRETORIO_IMAGENS, arquivo)

    # Ignora subpastas
    if not os.path.isfile(caminho_arquivo):
        continue

    # Extrai o nome do arquivo sem extensão
    nome_sem_extensao, _ = os.path.splitext(arquivo)
    codigo = nome_sem_extensao.strip()

    # Verifica se o código está na lista de válidos
    if codigo in codigos_validos:
        # Move o arquivo para o diretório "resized"
        destino = os.path.join(DIRETORIO_DESTINO, arquivo)
        shutil.move(caminho_arquivo, destino)
        movidos += 1
        print(f"Movido para 'resized': {arquivo}")
    else:
        mantidos += 1

# 3️⃣ Resumo
print("\nResumo da triagem:")
print(f"Total de arquivos movidos para 'resized': {movidos}")
print(f"Total de arquivos mantidos no diretório 'A': {mantidos}")
