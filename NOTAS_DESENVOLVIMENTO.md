
# 📝 Notas do Desenvolvimento & Decisões Métricas

> **Objetivo:** Registro pessoal de descobertas, decisões técnicas e premissas adotadas ao longo do projeto, atualizado após a consolidação da base de dados populacional completa.

---

## 🔍 1. Descobertas e Ajustes na Base de Dados

* **Transição de Amostra para Base Populacional Completa:**
  * *Histórico:* Inicialmente, trabalhou-se com uma amostragem reduzida (ex.: 500 linhas de presença e apenas 6 alunos cadastrados em 2025).
  * *Ajuste:* Com o recebimento da base completa, os números reais foram consolidados: **800 estudantes na análise de presenças** e denominadores reais de matrículas ano a ano (138 em 2021 até 233 em 2025).
* **Padronização de Universidades e Nomes:**
  * Identificadas inconsistências cadastrais com universidades gravadas de até 3 formas distintas (caixa alta, caixa baixa e abreviações).
  * *Ação:* Foi realizada a limpeza e unificação de nomes para garantir a correta distribuição geográfica e institucional dos aprovados (destaque para UECE com 60, UFC com 51 e UNILAB com 35).
* **Tratamento de Duplicatas e Limpeza:**
  * Identificados e removidos **15 registros duplicados** na aba `Aprovações`, utilizando a combinação com a coluna `chamada` como chave de identificação.
* **Padronização de Datas:**
  * Trataram-se múltiplos formatos de data ao longo das tabelas para viabilizar as junções (*joins*) das séries temporais.

---

## 🛠️ 2. Premissas e Regras de Negócio Adotadas

Diante das regras de negócio do desafio e da necessidade de padronização, foram definidas as seguintes premissas:

1. **Status de Aprovação:** O aluno que não consta na listagem da tabela `Aprovações` foi considerado como **Não Aprovado** ($N = 494$ não aprovados vs $N = 306$ aprovados na base total).
2. **Critério de Pontualidade:** O status "Atrasado" foi contabilizado como **Presença Confirmada**, assumindo-se que o estudante participou do conteúdo da aula.

---

## 📊 3. Principais Descobertas Estatísticas

* **Independência da Frequência (Presença vs. Desempenho):**
  * A taxa média de presença resultou em exatamente **84,0%** tanto para o grupo de Aprovados quanto para o de Não Aprovados.
  * O Teste de Mann-Whitney resultou em **$p = 0,5737$** e a correlação (Presença $\times$ Nota do Simulado) em **$r = -0,054$** ($p = 0,1241$).
  * *Conclusão:* A frequência isolada às aulas não é o fator determinante de aprovação, indicando que o foco deve migrar para a qualidade do estudo autônomo.
* **Revisão de Mitos Pedagógicos:**
  * A hipótese inicial de evasão crítica em Inglês (51% na amostra) foi descartada: na base completa, a disciplina apresentou **84,5% de finalização**, perfeitamente alinhada com as demais (83,9% a 85,9%).

---

## 📌 4. Questões Recomendadas para Alinhamento com o Cliente

* [ ] **Tolerância de Atrasos:** Confirmar se o critério de pontualidade/atraso deve ter peso diferenciado no cálculo futuro de engajamento.
* [ ] **Notas de Redação:** Definir se haverá inclusão de notas de redação em formato numérico padronizado nos próximos simulados.
* [ ] **Governança de Dados:** Implementar validação na entrada dos cadastros para evitar duplicidades de chamadas e nomes despadronizados de universidades na origem.
