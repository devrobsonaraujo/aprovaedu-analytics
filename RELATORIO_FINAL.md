# Relatório Final — AprovaEdu Analytics

## Resumo executivo

A base analisada cobre 2021–2025 e mistura tabelas **completas** (Professores,
Ofertas de Curso, Aprovações, Simulados) com tabelas **amostradas** de forma não
estratificada (Estudantes, Matrículas, Resultados de Simulado, Aulas,
Presenças). Essa distinção é o achado mais importante do diagnóstico de dados
e molda como cada pergunta abaixo deve ser lida: números vindos de tabelas
completas (aprovações, universidades, matérias) são sólidos; números que
dependem de cruzar tabelas amostradas (presença x aprovação) têm baixa
cobertura e devem ser tratados como sinal exploratório, não conclusão
definitiva, o que, em um cenário real, seria resolvido rodando o mesmo
pipeline sobre o CSV completo.

---

## 1. Qual foi a evolução da taxa de aprovação ao longo dos anos?

| Ano  | Aprovações (base completa) | Variação | Matriculados na amostra (únicos) | Taxa estimada* |
| ---- | ---------------------------- | ---------- | --------------------------------- | -------------- |
| 2021 | 50                           | —         | 9                                 | ~29%           |
| 2022 | 53                           | +6%        | 15                                | ~19%           |
| 2023 | 77                           | +45%       | 15                                | ~27%           |
| 2024 | 79                           | +3%        | 12                                | ~35%           |
| 2025 | 80                           | +1%        | 6                                 | ~71%**         |

\* Estimada projetando os alunos únicos matriculados na amostra (n pequeno) para
a escala da base completa (fator ~18,9x). \*\* O valor de 2025 é pouco confiável:
baseia-se em apenas 6 alunos únicos na amostra de matrículas daquele ano —
qualquer erro de amostragem se amplifica muito nesse denominador. Recomendo não usar esse número isoladamente.

**Principais movimentos observados:**

- O **número absoluto de aprovações cresceu de forma consistente**: 50 → 80
  (+60% em 5 anos), com o salto mais expressivo entre 2022 e 2023 (+45%).
- Esse crescimento é o dado mais confiável da análise, pois vem da tabela
  completa de aprovações (354 registros, sem amostragem).
- A "taxa" (aprovações / matriculados) não pôde ser calculada com precisão
  porque a tabela de Matrículas fornecida é uma amostra pequena e não
  estratificada por ano, o denominador é uma estimativa, não uma contagem
  real. Ainda assim, a estimativa não contradiz a leitura de que a aprovação
  está numericamente subindo mais rápido do que a base de matriculados parece
  crescer, o que é um indício (não uma prova) de melhora de efetividade.
- Como contexto adicional (dado completo, sem ressalva): as aprovações se
  concentram em UECE (60), UFC (51) e UNILAB (35); quase metade dos aprovados
  (47%) obteve alguma bolsa integral.

**Recomendação de próxima etapa:** recalcular a taxa real com o CSV completo de
matrículas (9.452 linhas) — é uma correção rápida e resolveria por completo a
principal limitação desta pergunta.

---

## 2. Existe relação entre presença nas aulas e aprovação no vestibular?

**Cobertura disponível:** apenas 47 alunos possuem registro de presença na
amostra fornecida (contra 500 linhas de eventos de presença, cada aluno
aparece, em média, em ~11 aulas). Desses 47, 18 aparecem também na tabela de
aprovações e 29 não aparecem (assumindo, como toda a base não tem uma tabela de "reprovados" explícita, que quem nunca aparece em Aprovações não foi aprovado
no período coberto).

| Grupo          | n  | Taxa média de presença |
| -------------- | -- | ------------------------ |
| Aprovados      | 18 | 85,5%                    |
| Não aprovados | 29 | 81,0%                    |

A diferença é **na direção esperada** (alunos aprovados frequentam um pouco
mais), mas o teste de Mann-Whitney não indica significância estatística
(p ≈ 0,12; com n=47 o poder estatístico é baixo — para detectar uma diferença
dessa magnitude com confiança seria necessário uma amostra bem maior).

**Análise complementar (mais robusta em tamanho amostral):** cruzando presença
com o desempenho médio nos simulados (mesma turma/ano de 2021, n=47, cobertura
quase total dos alunos com presença registrada), a correlação entre taxa de
presença e nota média em simulados é **fraca e não significativa**
(r ≈ 0,12; p ≈ 0,42).

**Conclusão:** com os dados disponíveis, **não há evidência estatística
forte** de relação entre presença e aprovação/desempenho, mas também não há
evidência de que a relação não exista; a amostra é pequena demais para
concluir em qualquer direção com confiança. A direção observada (mais presença
tende a levemente mais aprovação) é consistente com a intuição pedagógica e com a literatura educacional em geral, então recomendo tratar isso como hipótese a
confirmar com a base completa de presenças (74.997 registros), que teria poder
estatístico suficiente para uma conclusão definitiva.

---

## 3. Quais cursos ou matérias parecem apresentar melhor desempenho?

Baseado na nota média do diagnóstico de matrícula e na taxa de conclusão da
matrícula (disponíveis para as 11 matérias, com 36 a 56 matrículas cada — boa
cobertura):

| Matéria    | Nota diagnóstico (méd.) | Taxa de conclusão |
| ----------- | ------------------------- | ------------------ |
| Matemática | 61,0                      | 66%                |
| Biologia    | 60,7                      | 68%                |
| Redação   | 59,3                      | 64%                |
| Filosofia   | 59,1                      | 74%                |
| Inglês     | 58,8                      | 51%                |
| Física     | 58,6                      | 60%                |
| Português  | 58,2                      | 66%                |
| Química    | 58,2                      | 72%                |
| Sociologia  | 54,8                      | 68%                |
| Geografia   | 55,8                      | 66%                |
| História   | 57,1                      | 68%                |

*(Dados de simulados só cobrem Matemática e Física na amostra fornecida —
Matemática: nota média 60,7 / 86% de finalização; Física: 59,6 / 80% — em
linha com o diagnóstico, sem indicar mudança de ranking.)*

**Leitura:**

- **Matemática e Biologia** têm o melhor desempenho médio no diagnóstico de
  entrada, mas isso não se traduz automaticamente em conclusão de curso,
  **Filosofia e Química têm as maiores taxas de conclusão (72-74%)** mesmo
  com nota de entrada mediana, sugerindo cursos "mais fáceis de reter o aluno
  até o fim" mesmo sem ser o de melhor nota.
- **Inglês** chama atenção pela combinação ruim: nota de entrada mediana e a
  **menor taxa de conclusão (51%)** de todas as matérias, candidata natural
  a investigação (professor, carga horária, modalidade?).
- **Sociologia e Geografia** têm as menores notas de diagnóstico, mas taxa de
  conclusão na média — indica que o problema pode ser mais de nivelamento de
  entrada do que de evasão.
- Nenhuma matéria se destaca simultaneamente em nota alta **e** alta
  conclusão **e** presença nos simulados — o "melhor desempenho" depende de
  qual métrica a coordenação prioriza (nível de entrada, retenção, ou
  performance em simulados).

---

## 4. Quais recomendações você faria para a coordenação do cursinho?

1. **Investigar a evasão em Inglês antes de qualquer outra ação de matéria.**
   É o único indicador com bandeira vermelha clara e consistente (menor taxa
   de conclusão da base). Vale um mergulho qualitativo: professor, modalidade
   de oferta, horário de turma.
2. **Não tratar a "taxa de aprovação" atual como métrica oficial de
   performance** até recalculá-la com a base completa de matrículas. Hoje ela
   é uma estimativa com margem de erro grande, especialmente para os anos mais
   recentes (2025). Sugestão: montar um pipeline (este mesmo ETL, generalizado)
   que rode sobre os CSVs completos mensalmente, para que a coordenação tenha
   um número confiável e atualizado.
3. **Ampliar a coleta e a granularidade dos dados de presença** antes de tirar
   conclusões sobre o efeito da frequência na aprovação. A base fornecida tem
   presença registrada para menos de 10% dos alunos e concentrada em 2021 —
   é insuficiente para uma decisão de política pedagógica (ex: "tornar a
   presença obrigatória"). Recomendo garantir que 100% das turmas registrem
   presença de forma consistente ano a ano.
4. **Usar Matemática e Biologia como referência de desenho de curso**
   (nota de entrada mais alta), mas usar Filosofia e Química como referência
   de retenção (conclusão mais alta) — são times diferentes vencendo jogos
   diferentes, e a coordenação pode aprender lições distintas de cada um
   (ex.: o que Filosofia faz de diferente para reter aluno mesmo com nota
   de entrada mediana? Pode ser um modelo a replicar em Inglês).
5. **Padronizar a captura de dados na origem** para reduzir o retrabalho de
   ETL observado neste desafio: grafias inconsistentes de matéria/universidade/
   status, formatos de data mistos e nomes de professor digitados livremente
   (quando já existe um cadastro com ID) geram risco de erro silencioso em
   relatórios futuros. Uma tela de cadastro com campos de seleção (em vez de
   texto livre) resolveria a maior parte disso na fonte.

---

## Limitações do estudo

- Estudantes, Matrículas, Resultados de Simulado, Aulas e Presenças são
  **amostras pequenas e não estratificadas** da base completa — os números
  desta análise devem ser lidos como indicativos, não como estatística
  populacional definitiva.
- Não há tabela explícita de "não aprovados"; a análise assume que um aluno
  matriculado que nunca aparece em Aprovações não foi aprovado no período
  coberto pelos dados — premissa razoável, mas não confirmada.
- Todas as figuras e números deste relatório são reproduzíveis a partir de
  `src/etl.py` + `src/analysis.py` sobre `data/raw/`.

---

## Visualizações interativas

Além dos gráficos estáticos (outputs/figures/*.png) usados neste relatório,
foram criadas duas versões de dashboard interativo:

- **`outputs/dashboard.html`** — versão padrão com paleta neutra, representando
  o branding fictício da AprovaEdu (cliente do case)
- **`outputs/dashboard_logap.html`** — versão adaptada à identidade visual da
  Logap (azul tech/cyan), demonstrando capacidade de adaptação a guidelines
  corporativas do cliente

Ambos podem ser abertos diretamente em qualquer navegador (não requerem servidor).
