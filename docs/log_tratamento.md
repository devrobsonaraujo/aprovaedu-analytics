# Log de Decisões de Tratamento — ETL AprovaEdu Analytics

Gerado automaticamente pela execução de `src/etl.py`.

```
[LOAD] 9 tabelas lidas de base_pre_vestibular_dicionario_amostras.xlsx
  - Amostra_Professores: 35 linhas x 10 colunas
  - Amostra_Estudantes: 500 linhas x 10 colunas
  - Amostra_Ofertas_Curso: 220 linhas x 13 colunas
  - Amostra_Matriculas: 500 linhas x 10 colunas
  - Amostra_Aprovacoes: 354 linhas x 11 colunas
  - Amostra_Simulados: 165 linhas x 11 colunas
  - Amostra_Resultados_Sim: 500 linhas x 12 colunas
  - Amostra_Aulas: 500 linhas x 10 colunas
  - Amostra_Presencas_Aulas: 500 linhas x 6 colunas
[PROFESSORES] duplicidades em professor_id: 0
[PROFESSORES] materia_principal normalizada (ex.: 'Mat.', 'Matematica' -> 'Matemática')
[ESTUDANTES] duplicidades em aluno_id: 0
[ESTUDANTES] cidade/escola_origem/canal_captacao normalizados (casing); CPFs fora do padrão (!=11 dígitos) marcados como nulos por não serem confiáveis
[OFERTAS] divergências entre professor_nome_informado e cadastro do professor: 0
[OFERTAS] duplicidades em oferta_id: 0
[OFERTAS] materia normalizada; nome do professor passou a vir da dimensão (fonte única da verdade) em vez do campo digitado na tabela fato
[MATRICULAS] nota_diagnostico fora da faixa 0-100: 0 -> tratada como nula
[MATRICULAS] duplicidades em matricula_id: 0
[APROVACOES] registros duplicados (mesmo aluno/ano/universidade/nota): 15 de 354
[APROVACOES] duplicidades remanescentes em aprovacao_id: 0
[SIMULADOS] duplicidades em simulado_id: 0
[RESULTADOS_SIM] notas fora da faixa 0-100: 5 -> tratadas como nulas
[RESULTADOS_SIM] tempo de finalização <=0 em simulados 'Finalizado': 1 -> tratados como nulos
[RESULTADOS_SIM] status 'Ausente' com nota preenchida (inconsistente): 0 -> nota anulada
[RESULTADOS_SIM] duplicidades em resultado_id: 0
[AULAS] duplicidades em aula_id: 0
[PRESENCAS] duplicidades em presenca_id: 0
[FK CHECK] Matriculas -> Estudantes: 0 de 500 registros com aluno_id não encontrado na dimensão
[FK CHECK] Matriculas -> Ofertas: 0 de 500 registros com oferta_id não encontrado na dimensão
[FK CHECK] Aprovacoes -> Estudantes: 120 de 339 registros com aluno_id não encontrado na dimensão
[FK CHECK] Resultados_Sim -> Estudantes: 179 de 500 registros com aluno_id não encontrado na dimensão
[FK CHECK] Resultados_Sim -> Simulados: 0 de 500 registros com simulado_id não encontrado na dimensão
[FK CHECK] Aulas -> Ofertas: 0 de 500 registros com oferta_id não encontrado na dimensão
[FK CHECK] Presencas -> Aulas: 0 de 500 registros com aula_id não encontrado na dimensão
[FK CHECK] Presencas -> Estudantes: 158 de 500 registros com aluno_id não encontrado na dimensão
[SAVE] dim_professores.csv -> 35 linhas x 11 colunas
[SAVE] dim_estudantes.csv -> 500 linhas x 10 colunas
[SAVE] dim_ofertas.csv -> 220 linhas x 13 colunas
[SAVE] dim_simulados.csv -> 165 linhas x 11 colunas
[SAVE] fact_matriculas.csv -> 500 linhas x 10 colunas
[SAVE] fact_aprovacoes.csv -> 339 linhas x 10 colunas
[SAVE] fact_resultados_sim.csv -> 500 linhas x 12 colunas
[SAVE] fact_aulas.csv -> 500 linhas x 10 colunas
[SAVE] fact_presencas.csv -> 500 linhas x 6 colunas
```
