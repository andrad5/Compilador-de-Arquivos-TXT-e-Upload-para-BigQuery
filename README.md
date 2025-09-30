# 📁 Compilador de Arquivos TXT e Upload para Google BigQuery

Este script Python foi projetado para automatizar o processo de consolidação de múltiplos arquivos **.txt** (estruturados com delimitador) em um único arquivo **.csv** e, em seguida, carregar esse arquivo consolidado em uma tabela do Google BigQuery.

Ele é ideal para fluxos de trabalho que envolvem a coleta diária ou semanal de relatórios que precisam ser unificados e enviados para um Data Warehouse (como o BigQuery) mensalmente.

---

## ✨ Funcionalidades

* **Organização Mensal**: Copia os arquivos de origem para pastas de destino organizadas por **Mês/Ano** (ex: AGO25).
* **Compilação de Arquivos**: Concatena o conteúdo de todos os arquivos `.txt` de um determinado mês em um único arquivo `.csv`.
* **Decodificação Flexível**: Tenta ler os arquivos TXT usando várias codificações (**utf-8**, **latin-1**, **windows-1252**) para evitar erros de decodificação.
* **Criação de DataFrame**: Carrega o arquivo compilado no Pandas, aplicando o separador e o cabeçalho corretos, e renomeia as colunas.
* **Upload para BigQuery (BQ)**: Envia o DataFrame final para uma tabela específica no Google BigQuery, **substituindo o conteúdo existente**.

---

## 🛠️ Pré-requisitos

Para rodar este script, você precisará ter:
1.  **Python 3.x** instalado.
2.  As bibliotecas Python listadas na seção de Instalação.
3.  **Autenticação no Google Cloud**: O ambiente onde o script for executado deve estar autenticado e ter permissões para acessar e gravar no projeto e dataset do BigQuery especificados.

### Instalação de Bibliotecas

Instale as dependências usando `pip`:

```bash
pip install pandas google-cloud-bigquery
