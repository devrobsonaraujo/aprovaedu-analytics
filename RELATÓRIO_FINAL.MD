
# Análise de Consistência e Atualizações do Relatório Final — AprovaEdu Analytics

## Resumo das Correções

A chegada da **base de dados completa** altera de forma significativa a validade e a interpretação das análises anteriores. O relatório antigo baseava-se em premissas de alta amostragem em tabelas críticas (como matrículas e presenças) e n-amostrais reduzidos (ex.: apenas 47 alunos com presença e 6 alunos em 2025).

Abaixo está o diagnóstico ponto a ponto do que precisa ser alterado, seguido da nova versão proposta do relatório.

---

### Diagnóstico de Diferenças (Relatório Antigo vs. Dados Completos)

1. **Evolução da Taxa de Aprovação (Q1):**

   * **Como era:** O denominador era projetado com base em uma amostra de alunos únicos (ex.: 6 alunos em 2025 resultando em taxa estimada instável de ~71%).
   * **Como fica:** Com a base populacional completa, temos os denominadores reais: **138** (2021), **170** (2022), **218** (2023), **263** (2024) e **233** (2025).
   * **Nova interpretação:** A taxa real de aprovação oscila em uma faixa estável entre **30,0% e 36,2%** ao longo dos 5 anos. O ano de 2025, anteriormente apontado como distorcido (~71%), apresenta na verdade uma taxa de **34,3%** (80 aprovados em 233 matriculados).
2. **Presença vs. Aprovação e Desempenho (Q2):**

   * **Como era:** Cobertura de apenas 47 alunos.
   * **Como fica:** Base completa com **$N=800$ alunos** ($N_{\text{Aprovados}} = 306$, $N_{\text{Não aprovados}} = 494$).
   * **Nova interpretação:** A taxa de presença média é exatamente idêntica em ambos os grupos (**84,0%**)[cite: 1]. O teste de Mann-Whitney resulta em $p = 0,5737$ e a correlação entre presença e nota no simulado é de $r = -0,054$ ($p = 0,1241$)[cite: 1, 3]. **Conclusão sólida:** A frequência às aulas, isoladamente, não possui relação estatisticamente relevante com a aprovação ou com a nota dos simulados.
3. **Desempenho por Matéria (Q3):**

   * **Como era:** Diagnóstico limitado a pequenas amostras por matéria (36–56 matrículas) e dados de simulados restritos a Física e Matemática.
   * **Como fica:** Cobertura massiva por matéria ($N \approx 775 \text{ a } 1.027$ matrículas por disciplina). As notas de simulado agora cobrem todas as disciplinas (médias entre 60,7 e 62,0), com exceção de Redação (que não possui nota de simulado em formato de múltipla escolha).
   * **Nova interpretação:** A taxa de finalização/conclusão é uniformemente alta em todas as matérias (**83,9% a 85,9%**), derrubando a hipótese anterior de que Inglês sofria com evasão crítica (que apresentava 51% no relatório amostrado).

---

# Versão Atualizada do Relatório Final — AprovaEdu Analytics

## Resumo executivo

Com a consolidação da **base de dados completa** (cobrindo o período de 2021 a 2025), todas as métricas de acompanhamento passam a refletir valores populacionais reais, sem a necessidade de projeções ou inferências baseadas em amostras parciais.

Os dados confirmam o crescimento sustentado no volume de alunos aprovados ao longo dos anos, com a taxa global de aprovação mantendo-se em uma faixa média de **33,4%**. Além disso, a análise detalhada de engajamento indica que a frequência às aulas não diferencia, por si só, os alunos aprovados dos não aprovados. Por fim, a performance por matéria apresenta alta consistência em retenção e notas.

---

## 1. Qual foi a evolução da taxa de aprovação ao longo dos anos?

Com a consolidação do total de matriculados por ano, a evolução das aprovações e das taxas de sucesso é apresentada na tabela a seguir:

| Ano            | Aprovados | Alunos Matriculados | Taxa de Aprovação | Variação dos Aprovados (YoY) |
| :------------- | :-------: | :-----------------: | :-----------------: | :----------------------------: |
| **2021** |    50    |         138         |        36,2%        |               —               |
| **2022** |    53    |         170         |        31,2%        |             +6,0%             |
| **2023** |    77    |         218         |        35,3%        |             +45,3%             |
| **2024** |    79    |         263         |        30,0%        |             +2,6%             |
| **2025** |    80    |         233         |        34,3%        |             +1,3%             |

### Principais Destaques:

* **Crescimento no volume absoluto:** O número de aprovados subiu de 50 (2021) para 80 (2025), acumulando um ganho de 60% no período. O principal impulso ocorreu entre 2022 e 2023 (+45,3%).
* **Estabilidade da Taxa de Aprovação:** A taxa de aprovação oscila dentro de uma margem estreita (entre 30,0% e 36,2%), demonstrando que o cursinho conseguiu expandir sua capacidade de alunos mantendo a proporção histórica de aprovações.
* **Distribuição e Benefícios:** As aprovações continuam concentradas nas principais instituições da região — destaque para UECE (60), UFC (51) e UNILAB (35). Do total de aprovados, **47,2%** obtiveram bolsa integral e **24,5%** bolsa parcial.

---

## 2. Existe relação entre presença nas aulas e aprovação no vestibular?

**Base populacional analisada:** $N = 800$ estudantes.

| Grupo                    | $N$ | Taxa Média de Presença |
| :----------------------- | :---: | :----------------------: |
| **Aprovados**      |  306  |          84,0%          |
| **Não Aprovados** |  494  |          84,0%          |
| **Geral**          |  800  |          84,0%          |

* **Teste de Mann-Whitney U:** $p = 0,5737$.
* **Correlação (Presença $\times$ Nota do Simulado):** $r = -0,054$ ($p = 0,1241$).

### Conclusão:

**Não existe relação estatisticamente significativa** entre a frequência às aulas e a taxa de aprovação ou o desempenho nos simulados. A taxa média de presença é exatamente 84,0% tanto para os alunos que conquistaramm a vaga quanto para os que não foram aprovados.

Isso indica que a presença física ou virtual em sala é uma condição baseline do estudante, mas não o fator determinante para a aprovação. Variáveis como horas de estudo individual, bagagem prévia e qualidade do treino via simulados tendem a exercer maior peso no resultado final.

---

## 3. Quais cursos ou matérias parecem apresentar melhor desempenho?

A avaliação por matéria cobre mais de 8.000 matrículas distribuídas entre as 11 disciplinas oferecidas.

| Matéria              | Matrículas ($N$) | Nota Diagnóstico (Média) | Nota Simulado (Média) | Taxa de Finalização |
| :-------------------- | :-----------------: | :------------------------: | :--------------------: | :-------------------: |
| **Português**  |        1.026        |            58,5            |     **62,0**     |    **85,9%**    |
| **Física**     |         806         |            57,4            |          61,0          |         85,7%         |
| **Sociologia**  |         801         |            56,7            |          60,8          |         85,6%         |
| **Biologia**    |         805         |            57,9            |          61,2          |         85,3%         |
| **Química**    |         775         |            57,7            |          61,4          |         85,3%         |
| **Redação**   |        1.027        |            58,1            |          N/A*          |         85,1%         |
| **História**   |         784         |            57,7            |          61,5          |         85,0%         |
| **Matemática** |        1.027        |       **58,7**       |          60,9          |         84,8%         |
| **Filosofia**   |         789         |            59,0            |          61,5          |         84,6%         |
| **Inglês**     |         829         |            58,1            |          61,3          |         84,5%         |
| **Geografia**   |         783         |            58,5            |          60,7          |         83,9%         |

*\*Redação não possui nota em simulado padrão de múltipla escolha.*

### Leitura dos Dados:

* **Equilíbrio de Retenção:** A taxa de finalização é homogênea entre todas as disciplinas, variando de 83,9% (Geografia) a 85,9% (Português). O problema de evasão pontual em Inglês observado na amostragem anterior não se confirma na base completa.
* **Evolução de Notas:** Todas as disciplinas apresentam evolução positiva entre a avaliação diagnóstica de entrada ($\approx 56,7 - 59,0$) e a nota média dos simulados ($\approx 60,7 - 62,0$).
* **Destaques de Desempenho:** **Português** lidera tanto em nota média no simulado (62,0) quanto na taxa de retenção de alunos (85,9%). **Matemática** apresenta a maior nota no diagnóstico de entrada (58,7).

---

## 4. Recomendações para a Coordenação do Cursinho

1. **Foco no Estudo Dirigido e Treino Autónomo:** Como a presença em aula é idêntica entre aprovados e não aprovados (84,0%), a coordenação não deve focar esforços apenas em cobrar presença. O diferencial estratégico deve ser direcionado para o acompanhamento da rotina de estudos fora da sala e na resolução de simulados.
2. **Manutenção do Modelo Pedagógico por Matéria:** A uniformidade nas taxas de conclusão ($\approx 85\%$) e na evolução das notas mostra um currículo bem equilibrado entre as 11 disciplinas. Recomendamos manter a estrutura atual de ofertas, voltando o foco pedagógico para o nivelamento inicial nas matérias com diagnóstico mais baixo (ex.: Sociologia com 56,7).
3. **Formalização do Pipeline de Dados em Tempo Real:** A transição do relatório amostrado para o relatório populacional demonstrou o impacto direto da qualidade dos dados nas tomadas de decisão. Sugere-se a automação contínua do pipeline ETL desenvolvido para atualização mensal dos dados do dashboard institucional.
