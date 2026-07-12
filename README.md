# AprovaEdu Analytics — Desafio Técnico (Analista de Dados)

Solução analítica para a base de um cursinho pré-vestibular fictício (2021–2025),
desenvolvida para o desafio técnico da AprovaEdu Analytics.

## 📁 Estrutura do projeto

```
aprovaedu_analytics/
├── data/
│   ├── raw/                         # Base bruta original (xlsx com amostras)
│   └── processed/                   # Saída do ETL: dimensões e fatos tratados (CSV)
│       ├── dim_professores.csv
│       ├── dim_estudantes.csv
│       ├── dim_ofertas.csv
│       ├── dim_simulados.csv
│       ├── fact_matriculas.csv
│       ├── fact_aprovacoes.csv
│       ├── fact_resultados_sim.csv
│       ├── fact_aulas.csv
│       └── fact_presencas.csv
├── src/
│   ├── etl.py                       # Leitura, limpeza, normalização e modelagem
│   └── analysis.py                  # Análises obrigatórias (Q1-Q3) e geração de figuras
├── outputs/
│   ├── figures/                     # Gráficos estáticos (PNG) usados no relatório
│   └── dashboard.html               # Dashboard interativo (Plotly, standalone)
├── docs/
│   ├── log_tratamento.md            # Log automático de todas as decisões do ETL
│   ├── metricas.json                # Métricas calculadas (fonte do relatório)
│   └── dashboard_data.json          # Dados agregados usados pelo dashboard
├── RELATORIO_FINAL.md               # Respostas às 4 perguntas obrigatórias + recomendações
└── README.md
```

## ▶️ Como rodar

### Opção 1: Ver os resultados imediatamente (sem executar código)

Os **dados processados e visualizações já estão incluídos** no repositório:

- 📊 **Dashboards interativos:** Abra `outputs/dashboard.html` ou `outputs/dashboard_logap.html` no navegador
- 📈 **Gráficos estáticos:** Pasta `outputs/figures/`
- 📄 **Relatório completo:** Veja `RELATORIO_FINAL.md`
- 📊 **Dados tratados:** Pasta `data/processed/` (CSVs prontos)

### Opção 2: Executar o pipeline completo

Requisitos: Python 3.10+

```bash
# Instalar dependências
pip install -r requirements.txt

# Ou manualmente:
pip install pandas numpy scipy openpyxl matplotlib

# Executar pipeline
python src/etl.py        # gera data/processed/*.csv e docs/log_tratamento.md
python src/analysis.py   # gera outputs/figures/*.png e docs/metricas.json
```

### Opção 3: Com Docker (ambiente reproduzível)

```bash
docker compose run --rm pipeline
```

Veja `README_DOCKER.md` para mais detalhes.

## � Dashboard Interativo

Duas versões disponíveis para demonstração:

1. **`outputs/dashboard.html`** - Versão padrão com paleta neutra (azul navy/laranja)

   - Representa o branding fictício da AprovaEdu (cliente do case)
2. **`outputs/dashboard_logap.html`** - Versão adaptada ao branding Logap

   - Paleta tech em azul cyan (#00A8E8) alinhada à identidade visual da empresa
   - Demonstra capacidade de adaptação a guidelines visuais do cliente

> **Nota:** A versão Logap foi criada especificamente para este processo seletivo,
> mostrando atenção ao branding corporativo. Em um projeto real, as cores seriam
> sempre adaptadas à identidade visual do cliente final.

## 🀽�️ Ferramentas utilizadas

- **Python 3** (pandas, numpy, scipy, matplotlib) — ETL e análise estatística
- **Plotly.js** (via CDN) — dashboard interativo standalone (HTML puro, sem backend)
- Sem uso de banco de dados: o volume de dados (amostras de até ~500 linhas) não
  justificava a sobrecarga de um SGBD; o modelo dimensional foi implementado em
  CSV/pandas, mas a estrutura (dimensões + fatos com chaves `*_id`) é a mesma que
  seria usada em um DW relacional ou num modelo estrela no Power BI.

## 🧭 Decisões técnicas e analíticas relevantes

### 1. Natureza da base fornecida 

A planilha entrega **amostras**, não a base completa (isso está explícito na aba
`Resumo`). Ao investigar, descobri que:

- **Professores, Ofertas_Curso, Aprovações e Simulados vieram completos**
  (o nº de linhas da amostra bate exatamente com o "nº de linhas no CSV completo" informado na aba Resumo).
- **Estudantes, Matrículas, Resultados_Sim, Aulas e Presenças_Aulas são
  recortes pequenos** da base completa (ex.: Presenças_Aulas tem 500 linhas de
  um total de 74.997 — 0,7% da base; Resultados_Sim tem 500 de 21.510, e **100%
  desses 500 registros são do ano de 2021** — ou seja, não é uma amostra
  aleatória estratificada por ano, é um recorte cronológico inicial).

Essa constatação muda a estratégia analítica: cruzamentos entre tabelas grandes
(ex. presença x aprovação) têm interseção pequena de alunos em comum, e qualquer
"taxa" que dependa do universo completo de matriculados precisa ser tratada como
**estimativa**, não como número exato. Isso está documentado e sinalizado em
cada resposta do relatório final — reportar um número "bonito" sem essa ressalva
seria enganoso.

### 2. Padronização de categorias

Vários campos vinham com grafias inconsistentes (`"Mat."`, `"Matematica"`,
`"MATEMÁTICA"` → `"Matemática"`; `"uece"`, `"UECE"` → `"UECE"`; etc.). Foram
criados dicionários de mapeamento (`MATERIA_MAP`, `UNIV_MAP`, mapas por campo)
aplicados de forma determinística, nenhuma inferência "inteligente" foi usada
para não introduzir viés silencioso.

### 3. Datas em formatos mistos

Colunas de data continham `YYYY-MM-DD`, `YYYY/MM/DD`, `DD/MM/YYYY`,
`MM-DD-YYYY` e datetimes com hora, todos na mesma coluna. O parser tenta cada
formato em sequência (do mais específico ao mais genérico) antes de cair em um
parser de fallback, evitando ambiguidade tipo "01/02/2023" (dia ou mês?).

### 4. Deduplicação

- **Aprovações**: 15 registros eram duplicatas de negócio (mesmo aluno, mesmo
  ano, mesma universidade, mesma nota), inclusive com uma dica no próprio dado
  (`chamada = "Cadastro duplicado?"`, usado apenas para localizar o problema,
  depois descartado). Mantido o registro de menor `aprovacao_id`.
- Demais tabelas: sem duplicidade de chave primária na amostra fornecida.

### 5. Outliers e inconsistências

- Notas de simulado fora da faixa 0–100 (ex. 105) → nulificadas.
- Tempo de finalização ≤ 0 com status "Finalizado" → nulificado (implausível).
- Status "Ausente" com nota preenchida → nota nulificada (inconsistência lógica).
- CPFs fictícios fora do padrão de 11 dígitos → nulificados (não confiáveis).

### 6. Denormalização

`professor_nome_informado` (em Ofertas e Simulados) foi comparado ao nome
cadastrado na dimensão de professores (fonte única da verdade) e substituído
por ele, evita que o relatório reflita erros de digitação no campo
denormalizado.

### 7. Integridade referencial

O ETL registra (mas não descarta automaticamente) chaves estrangeiras "órfãs".
A maior parte dos órfãos encontrados é explicada pela limitação de amostragem
do item 1 (ex.: um `aluno_id` presente em Aprovações mas fora dos 500 alunos
sorteados para a dimensão Estudantes), não por erro de digitação.

## ✅ O que foi entregue

- [X] Leitura das bases originais
- [X] Tratamento e padronização documentados (código + `docs/log_tratamento.md`)
- [X] Base estruturada em modelo dimensional (dimensões + fatos)
- [X] Indicadores e respostas às 4 perguntas obrigatórias (`RELATORIO_FINAL.md`)
- [X] Dashboard interativo (`outputs/dashboard.html`)
- [X] Recomendações práticas para a coordenação

## 📚 Documentação Adicional

- **`RELATORIO_FINAL.md`** - Respostas completas às 4 perguntas obrigatórias + recomendações
- **`docs/log_tratamento.md`** - Log detalhado de todas as decisões de tratamento do ETL
- **`USO_DE_IA.md`** - Documentação transparente sobre o uso de IA no projeto
- **`NOTAS_DESENVOLVIMENTO.md`** - Descobertas e decisões durante o desenvolvimento
- **`README_DOCKER.md`** - Instruções completas de uso do Docker
- **`outputs/README_DASHBOARDS.md`** - Explicação das duas versões do dashboard
