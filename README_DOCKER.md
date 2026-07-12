# 🐋 Uso do Docker - AprovaEdu Analytics

## Pré-requisitos

- Docker instalado
- Docker Compose instalado

## 🚀 Como usar

### 1. Executar o pipeline completo (ETL + Análises)

```bash
# Opção 1: Com docker compose
docker compose run --rm pipeline

# Opção 2: Com docker direto
docker build -t aprovaedu-analytics .
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/outputs:/app/outputs" \
  -v "$(pwd)/docs:/app/docs" \
  aprovaedu-analytics
```

**O que acontece:**

- Processa os dados brutos (ETL)
- Gera CSVs tratados em `data/processed/`
- Cria gráficos em `outputs/figures/`
- Gera `docs/metricas.json` e `docs/dashboard_data.json`

### 2. Visualizar o dashboard

```bash
# Subir servidor HTTP na porta 8080
docker compose --profile dashboard up

# Acessar: http://localhost:8080/dashboard.html
```

### 3. Modo debug (shell interativo)

```bash
docker run --rm -it \
  -v "$(pwd):/app" \
  aprovaedu-analytics bash

# Dentro do container:
python src/etl.py
python src/analysis.py
exit
```

## 📁 Estrutura de volumes

Os seguintes diretórios são montados como volumes:

- `./data` → `/app/data` - Dados brutos e processados
- `./outputs` → `/app/outputs` - Figuras e dashboard
- `./docs` → `/app/docs` - JSONs de métricas
- `./src` → `/app/src` - Código-fonte (apenas no compose)

## 🔧 Comandos úteis

```bash
# Rebuild da imagem (após mudanças no código)
docker compose build

# Ver logs do pipeline
docker compose run pipeline

# Limpar containers e volumes
docker compose down -v

# Remover a imagem
docker rmi aprovaedu-analytics
```

## 📦 Dependências

Todas as dependências Python estão definidas em `requirements.txt`:

- pandas >= 3.0.0
- numpy >= 2.4.0
- scipy >= 1.18.0
- matplotlib >= 3.11.0
- openpyxl >= 3.1.5

## ⚠️ Notas importantes

1. **Dados brutos**: O arquivo Excel deve estar em `data/raw/base_pre_vestibular_dicionario_amostras.xlsx`
2. **Primeira execução**: Se os diretórios não existirem, serão criados automaticamente
3. **Windows**: Use PowerShell ou Git Bash para os comandos com `$(pwd)`
