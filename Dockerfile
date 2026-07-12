# AprovaEdu Analytics — ambiente reprodutível
# Build:  docker build -t aprovaedu-analytics .
# Rodar o pipeline completo (ETL + análises):
#   docker run --rm -v "$(pwd)/data:/app/data" -v "$(pwd)/outputs:/app/outputs" -v "$(pwd)/docs:/app/docs" aprovaedu-analytics
# Rodar e depois abrir um shell dentro do container (debug):
#   docker run --rm -it -v "$(pwd):/app" aprovaedu-analytics bash

FROM python:3.11-slim

WORKDIR /app

# Dependências de sistema mínimas (matplotlib precisa de libfreetype/libpng em algumas distros)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libfreetype6 \
    libpng16-16 \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código-fonte
COPY src/ ./src/

# Criar diretórios necessários (caso não existam nos volumes)
RUN mkdir -p data/raw data/processed outputs/figures docs

# Executa o pipeline inteiro por padrão: ETL -> análises
CMD ["sh", "-c", "python src/etl.py && python src/analysis.py"]
