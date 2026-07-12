# Uso de IA neste projeto

O desafio lista "Uso de IA sobre os dados, desde que documentado" como diferencial.
Este documento explica exatamente onde e como IA generativa (Claude, Anthropic)
foi usada na construção deste projeto, para que o avaliador saiba separar o que
foi decisão/raciocínio do candidato do que foi assistência de ferramenta.

## O que a IA fez

- **Aceleração da escrita de código**: o código de ETL (`src/etl.py`) e de
  análise (`src/analysis.py`) foi escrito com apoio de Claude, a partir de
  decisões de tratamento definidas por mim.
- **Geração do dashboard interativo** (`outputs/dashboard.html, outputs/dashboard_logap.html`) em Plotly.js,
  a partir das métricas já calculadas pelo pipeline.
- **Redação inicial da documentação** (README, relatório final), revisada e
  ajustada por mim.

## O que a IA **não** fez

- Não decidiu sozinha as regras de negócio (ex.: o que conta como "presença
  efetiva", qual a definição de "aprovado" na ausência de uma tabela de
  reprovados). Essas decisões foram avaliadas e validadas por mim, inclusive cruzando manualmente os resultados no Power BI.
- Não teve acesso a nenhum dado além do que está neste repositório, não há
  chamadas de API externas, nem dados sensíveis enviados a serviços de
  terceiros.
- Não substituiu a validação: todos os números do relatório final foram
  conferidos de forma independente. Recriei as métricas no Power BI, justamente para garantir que a lógica esteja certa e não é só "a IA disse que está certo".

## Minha contribuição específica

- **Identificação do problema da amostragem**: Foi lendo a aba Resumo manualmente que percebi que algumas tabelas eram completas e outras eram amostras de 0,7%
  - isso não estava explícito e mudou toda a análise
- **Definições de negócio**: O que conta como "presença efetiva"? Como tratar
  duplicatas? Essas foram minhas decisões baseadas no contexto educacional
- **Validação cruzada**: Recriei as principais métricas no Power BI para garantir
  que os números estavam corretos antes de escrever o relatório

Ver `NOTAS_DESENVOLVIMENTO.md` para mais detalhes do processo.
