
import os
import shutil
from datetime import datetime
import pandas as pd

# Mês e ano do arquivo que quer gerar DF e subir p BQ
MesAno_Referencia = 'AGO25'   # < < < < < < < < < < < 

# 1. IMPORTANTE: Altere o caminho abaixo para a pasta onde estão seus arquivos TXT.
PASTA_ORIGEM = r'\\user\'

# 2. OPCIONAL: Pasta de destino para organização mensal dos arquivos originais.
PASTA_DESTINO = r'\\user\'

# 3. NOVO: Pasta final onde todos os arquivos compilados por mês serão armazenados.
PASTA_COMPILADOS = r'\\user\'

# --- INÍCIO DO SCRIPT ---

def ler_arquivo_com_fallback(caminho_arquivo):
    """
    Tenta ler um arquivo com diferentes codificações (encodings) para evitar erros.
    Retorna o conteúdo do arquivo ou None se a leitura falhar.
    """
    encodings_para_tentar = ['utf-8', 'latin-1', 'windows-1252']
    
    for encoding in encodings_para_tentar:
        try:
            with open(caminho_arquivo, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
            
    print(f"  AVISO: Não foi possível decodificar o arquivo '{os.path.basename(caminho_arquivo)}' com as codificações testadas. Este arquivo será pulado.")
    return None

def processar_arquivos():
    """
    Função principal que copia, compila e move os arquivos.
    """
    sufixo_ano_atual = datetime.now().strftime('%y')
    mapa_meses = {
        '01': 'JAN', '02': 'FEV', '03': 'MAR', '04': 'ABR', '05': 'MAI', '06': 'JUN',
        '07': 'JUL', '08': 'AGO', '09': 'SET', '10': 'OUT', '11': 'NOV', '12': 'DEZ'
    }
    arquivos_por_mes = {}
    base_path_destino = PASTA_DESTINO if PASTA_DESTINO else PASTA_ORIGEM

    if not PASTA_ORIGEM:
        print("ERRO: A variável 'PASTA_ORIGEM' está vazia. Por favor, defina o caminho para os seus arquivos.")
        return

    # Garante que a pasta de compilados exista antes de começar
    if PASTA_COMPILADOS:
        os.makedirs(PASTA_COMPILADOS, exist_ok=True)
        print(f"Pasta de compilados configurada para: '{os.path.abspath(PASTA_COMPILADOS)}'")
    else:
        print("AVISO: 'PASTA_COMPILADOS' não foi definida. Os arquivos compilados permanecerão nas pastas mensais.")

    print(f"Analisando arquivos na pasta: '{os.path.abspath(PASTA_ORIGEM)}'...")
    if PASTA_DESTINO:
        os.makedirs(PASTA_DESTINO, exist_ok=True)
        print(f"Pasta de destino configurada para: '{os.path.abspath(PASTA_DESTINO)}'")

    try:
        lista_de_arquivos = os.listdir(PASTA_ORIGEM)
    except FileNotFoundError:
        print(f"ERRO: A pasta de origem '{PASTA_ORIGEM}' não foi encontrada.")
        return
    except OSError as e:
        print(f"ERRO de sistema ao acessar a pasta '{PASTA_ORIGEM}': {e}")
        return

    for nome_arquivo in lista_de_arquivos:
        caminho_completo = os.path.join(PASTA_ORIGEM, nome_arquivo)
        if os.path.isfile(caminho_completo) and nome_arquivo.lower().endswith('.txt'):
            nome_sem_extensao = os.path.splitext(nome_arquivo)[0]
            
            if len(nome_sem_extensao) >= 2 and nome_sem_extensao[-2:].isdigit():
                numero_mes = nome_sem_extensao[-2:]
                if numero_mes in mapa_meses:
                    if numero_mes not in arquivos_por_mes:
                        arquivos_por_mes[numero_mes] = []
                    arquivos_por_mes[numero_mes].append(nome_arquivo)

    if not arquivos_por_mes:
        print("\nProcesso interrompido. Nenhum arquivo TXT com final numérico de mês (01-12) foi encontrado.")
        return

    for numero_mes, lista_arquivos in arquivos_por_mes.items():
        nome_pasta_destino = f"{mapa_meses[numero_mes]}{sufixo_ano_atual}"
        caminho_pasta_destino = os.path.join(base_path_destino, nome_pasta_destino)
        os.makedirs(caminho_pasta_destino, exist_ok=True)
        print(f"\n--- Processando Mês: {mapa_meses[numero_mes]} ---")
        print(f"Pasta de trabalho: '{caminho_pasta_destino}'")

        print("Copiando arquivos originais...")
        for nome_arquivo in lista_arquivos:
            caminho_origem_arquivo = os.path.join(PASTA_ORIGEM, nome_arquivo)
            caminho_destino_arquivo = os.path.join(caminho_pasta_destino, nome_arquivo)
            try:
                shutil.copy2(caminho_origem_arquivo, caminho_destino_arquivo)
            except Exception as e:
                print(f"ERRO ao copiar o arquivo '{nome_arquivo}': {e}")

        nome_arquivo_compilado = f"{nome_pasta_destino}.csv"
        caminho_arquivo_compilado_temp = os.path.join(caminho_pasta_destino, nome_arquivo_compilado)

        try:
            with open(caminho_arquivo_compilado_temp, 'w', encoding='utf-8') as arquivo_final:
                print(f"Criando arquivo compilado: '{nome_arquivo_compilado}'")
                for nome_arquivo in lista_arquivos:
                    caminho_arquivo_copiado = os.path.join(caminho_pasta_destino, nome_arquivo)
                    conteudo = ler_arquivo_com_fallback(caminho_arquivo_copiado)
                    
                    if conteudo is not None:
                        arquivo_final.write(conteudo)

            # Move o arquivo compilado para a pasta final
            if PASTA_COMPILADOS:
                caminho_final_compilado = os.path.join(PASTA_COMPILADOS, nome_arquivo_compilado)
                print(f"Movendo arquivo compilado para '{caminho_final_compilado}'...")
                shutil.move(caminho_arquivo_compilado_temp, caminho_final_compilado)

        except IOError as e:
            print(f"ERRO ao escrever no arquivo compilado: {e}")
            continue

    print("\nProcesso de compilação concluído com sucesso!")

# --- Executa a primeira parte do script ---
if __name__ == "__main__":
    processar_arquivos()

# === Criar df a partir do arquivo compilado na PASTA_COMPILADOS ===

nome_arquivo_leitura = f"RDI_COMPILADO_{MesAno_Referencia}.csv"
caminho_completo_leitura = os.path.join(PASTA_COMPILADOS, nome_arquivo_leitura)

print(f"\n--- Lendo o arquivo compilado para o DataFrame ---")
print(f"Caminho do arquivo: {caminho_completo_leitura}")

try:
    # Código de leitura simplificado e consolidado.
    df = pd.read_csv(
        caminho_completo_leitura,
        sep=';',              # O delimitador que você identificou como correto.
        header=None,          # Seus dados não têm cabeçalho no arquivo.
        encoding='latin-1',   # Codificação comum para arquivos de sistemas brasileiros.
        on_bad_lines='warn'   # Avisa sobre linhas com problemas, mas não para o script.
    )

    print("\nArquivo carregado com sucesso no DataFrame!")

    Titulos = ["Evento", "DT_Evento", "DT_Emissao", "Cia_Seg", "SUCURSAL", "Ramo", 
               "Sistema", "Negocio", "N_Apolice", "N_G_Apolice", "N_Endosso", 
               "V_Corret_Conc", "Val_Agenc_Cong", "Valo_P_Labore_Cong", 
               "Val_TX_ADM", "DT_Venc_Tit"]


    df.columns = Titulos
    df = df.astype(str)
    df_bkp = df.copy() # Criando o backup após a renomeação das colunas
    

    


    print("\nColunas renomeadas com sucesso!")
    print("Amostra do DataFrame (5 primeiras linhas):")
    print(df.head())

except FileNotFoundError:
    print(f"\nERRO: O arquivo '{nome_arquivo_leitura}' não foi encontrado em '{PASTA_COMPILADOS}'.")
    print("Verifique se a variável 'MesAno_Referencia' está correta e se a primeira parte do script (compilação) gerou o arquivo esperado.")
except Exception as e:
    print(f"\nOcorreu um erro inesperado ao ler o arquivo e processá-lo com o Pandas: {e}")


# Lembre-se que ele precisa do DataFrame 'df' que agora deve ser criado corretamente.

from google.cloud import bigquery

project_id = " "
dataset_id = " "
table_id = f' '
destination_table = f"{dataset_id}.{table_id}"

print(f"\nIniciando o upload para o BigQuery na tabela: {destination_table}")
try:
    df.to_gbq(destination_table, project_id=project_id, if_exists='replace')
    print("DataFrame enviado com sucesso para o BigQuery!")
except Exception as e:
    print(f"Ocorreu um erro durante o upload para o BigQuery: {e}")

# |==================================================================================================|