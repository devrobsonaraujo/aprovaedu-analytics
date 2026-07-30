# -*- coding: utf-8 -*-
"""
Análises obrigatórias - AprovaEdu Analytics (Base de Dados Completa)
Lê a base tratada (data/processed) e responde às 4 perguntas do desafio,
gerando figuras (outputs/figures) e um resumo de métricas (docs/metricas.json).
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]
PROC = BASE / "data" / "processed"
FIG = BASE / "outputs" / "figures"
FIG.mkdir(parents=True, exist_ok=True)
DOCS = BASE / "docs"
DOCS.mkdir(exist_ok=True)

plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "white",
    "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
})
COLOR_PRIMARY = "#2A5C8A"
COLOR_ACCENT = "#E07A3F"

metrics = {}

dim_estudantes = pd.read_csv(PROC / "dim_estudantes.csv")
dim_ofertas = pd.read_csv(PROC / "dim_ofertas.csv")
dim_simulados = pd.read_csv(PROC / "dim_simulados.csv")
fact_matriculas = pd.read_csv(PROC / "fact_matriculas.csv")
fact_aprovacoes = pd.read_csv(PROC / "fact_aprovacoes.csv")
fact_resultados = pd.read_csv(PROC / "fact_resultados_sim.csv")
fact_aulas = pd.read_csv(PROC / "fact_aulas.csv")
fact_presencas = pd.read_csv(PROC / "fact_presencas.csv")

# ===========================================================================
# Q1 — Evolução da taxa de aprovação ao longo dos anos
# ===========================================================================
print("== Q1: evolução da taxa de aprovação ==")

aprov_por_ano = fact_aprovacoes.groupby("ano_vestibular")["aluno_id"].nunique().rename("aprovados")
matric_alunos_por_ano = fact_matriculas.groupby("ano")["aluno_id"].nunique().rename("alunos_matriculados")

q1 = pd.concat([aprov_por_ano, matric_alunos_por_ano], axis=1)
# Cálculo da taxa real de aprovação (base populacional completa)
q1["taxa_aprovacao_%"] = (q1["aprovados"] / q1["alunos_matriculados"] * 100).round(1)
q1["variacao_aprovados_%"] = q1["aprovados"].pct_change().mul(100).round(1)
print(q1)

metrics["q1_aprovacoes_por_ano"] = q1.reset_index().to_dict(orient="records")
metrics["q1_crescimento_total_aprovacoes_%"] = round(
    (q1["aprovados"].iloc[-1] / q1["aprovados"].iloc[0] - 1) * 100, 1
)

fig, ax1 = plt.subplots(figsize=(8, 4.5))
ax1.bar(q1.index.astype(str), q1["aprovados"], color=COLOR_PRIMARY, label="Nº de aprovações (base completa)")
ax1.set_ylabel("Nº de aprovações", color=COLOR_PRIMARY)
ax1.set_xlabel("Ano do vestibular")
for x, y in zip(q1.index.astype(str), q1["aprovados"]):
    ax1.annotate(str(y), (x, y), ha="center", va="bottom", fontsize=10)

ax2 = ax1.twinx()
ax2.plot(q1.index.astype(str), q1["taxa_aprovacao_%"], color=COLOR_ACCENT,
         marker="o", linewidth=2, label="Taxa de aprovação real (%)")
ax2.set_ylabel("Taxa de aprovação real (%)", color=COLOR_ACCENT)
ax1.set_title("Evolução das aprovações: nº absoluto (barras) e taxa real (linha)")
fig.tight_layout()
fig.savefig(FIG / "q1_evolucao_aprovacoes.png", dpi=150)
plt.close(fig)

# Aprovações por universidade / modalidade
apr_uni = fact_aprovacoes["universidade"].value_counts()
apr_bolsa = fact_aprovacoes["bolsa_aprovacao"].value_counts(normalize=True).mul(100).round(1)
metrics["q1_aprovacoes_por_universidade"] = apr_uni.to_dict()
metrics["q1_pct_aprovados_com_bolsa"] = apr_bolsa.to_dict()

fig, ax = plt.subplots(figsize=(7, 4.5))
apr_uni.sort_values().plot(kind="barh", ax=ax, color=COLOR_PRIMARY)
ax.set_title("Aprovações por universidade (2021–2025, base completa)")
ax.set_xlabel("Nº de aprovações")
fig.tight_layout()
fig.savefig(FIG / "q1b_aprovacoes_por_universidade.png", dpi=150)
plt.close(fig)

# ===========================================================================
# Q2 — Presença nas aulas x aprovação no vestibular
# ===========================================================================
print("\n== Q2: presença x aprovação ==")

# Taxa de presença por aluno: Presente/Atrasado contam como presença efetiva
freq_status = fact_presencas.copy()
freq_status["presente_efetivo"] = freq_status["status_presenca"].isin(["Presente", "Atrasado"]).astype(int)
attendance = freq_status.groupby("aluno_id").agg(
    aulas_registradas=("presenca_id", "count"),
    presencas_efetivas=("presente_efetivo", "sum"),
).reset_index()
attendance["taxa_presenca_%"] = (attendance["presencas_efetivas"] / attendance["aulas_registradas"] * 100).round(1)

metrics["q2_n_alunos_com_registro_presenca"] = int(len(attendance))
metrics["q2_taxa_presenca_media_%"] = round(attendance["taxa_presenca_%"].mean(), 1)
metrics["q2_taxa_presenca_mediana_%"] = round(attendance["taxa_presenca_%"].median(), 1)

# Status de aprovação na base completa
aprovados_ids = set(fact_aprovacoes["aluno_id"].unique())
attendance["aprovado"] = attendance["aluno_id"].isin(aprovados_ids)

n_aprov = attendance["aprovado"].sum()
n_nao = (~attendance["aprovado"]).sum()
metrics["q2_overlap_presenca_aprovacao_n"] = int(len(attendance))
metrics["q2_overlap_aprovados"] = int(n_aprov)
metrics["q2_overlap_nao_aprovados"] = int(n_nao)

grp_aprov = attendance.loc[attendance["aprovado"], "taxa_presenca_%"]
grp_nao = attendance.loc[~attendance["aprovado"], "taxa_presenca_%"]
metrics["q2_media_presenca_aprovados_%"] = round(grp_aprov.mean(), 1)
metrics["q2_media_presenca_nao_aprovados_%"] = round(grp_nao.mean(), 1)

# Resumo de presença x aprovação
q2_resumo = pd.DataFrame({
    "Grupo": ["Aprovados", "Não aprovados", "Geral"],
    "N": [n_aprov, n_nao, len(attendance)],
    "Taxa presença média (%)": [
        round(grp_aprov.mean(), 1),
        round(grp_nao.mean(), 1),
        round(attendance["taxa_presenca_%"].mean(), 1)
    ]
})
print(q2_resumo.to_string(index=False))

if len(grp_aprov) > 1 and len(grp_nao) > 1:
    u_stat, p_val = stats.mannwhitneyu(grp_aprov, grp_nao, alternative="two-sided")
    metrics["q2_mannwhitney_p_valor"] = round(float(p_val), 4)
    print(f"Mann-Whitney U test: p-valor = {round(float(p_val), 4)}")
else:
    metrics["q2_mannwhitney_p_valor"] = None
    print("Grupos insuficientes para teste estatístico")

fig, ax = plt.subplots(figsize=(6, 4.5))
data_box = [grp_nao.values, grp_aprov.values]
bp = ax.boxplot(data_box, patch_artist=True, widths=0.5)
for patch, color in zip(bp["boxes"], [COLOR_ACCENT, COLOR_PRIMARY]):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax.set_xticklabels([f"Não aprovado\n(N={n_nao})", f"Aprovado\n(N={n_aprov})"])
ax.set_ylabel("Taxa de presença (%)")
ax.set_title(f"Presença nas aulas x aprovação (N={len(attendance)} alunos)")
fig.tight_layout()
fig.savefig(FIG / "q2_presenca_aprovacao_boxplot.png", dpi=150)
plt.close(fig)

# Presença x Desempenho em Simulados
res_aluno = fact_resultados.groupby("aluno_id")["nota"].mean().rename("nota_media_simulado")
att_res = attendance.merge(res_aluno, on="aluno_id", how="inner")
metrics["q2b_n_presenca_x_simulado"] = int(len(att_res))
if len(att_res) > 2:
    corr, p_corr = stats.pearsonr(att_res["taxa_presenca_%"], att_res["nota_media_simulado"].fillna(att_res["nota_media_simulado"].mean()))
    metrics["q2b_correlacao_presenca_nota_simulado"] = round(float(corr), 3)
    metrics["q2b_p_valor"] = round(float(p_corr), 4)
    print(f"Correlação presença x nota simulado (N={len(att_res)}): r={round(float(corr), 3)}, p={round(float(p_corr), 4)}")

fig, ax = plt.subplots(figsize=(6, 4.5))
ax.scatter(att_res["taxa_presenca_%"], att_res["nota_media_simulado"], color=COLOR_PRIMARY, alpha=0.7)
if len(att_res) > 2:
    z = np.polyfit(att_res["taxa_presenca_%"], att_res["nota_media_simulado"].fillna(att_res["nota_media_simulado"].mean()), 1)
    xs = np.linspace(att_res["taxa_presenca_%"].min(), att_res["taxa_presenca_%"].max(), 50)
    ax.plot(xs, np.polyval(z, xs), color=COLOR_ACCENT, linewidth=2)
ax.set_xlabel("Taxa de presença (%)")
ax.set_ylabel("Nota média nos simulados")
ax.set_title(f"Presença x desempenho em simulados (N={len(att_res)} alunos)")
fig.tight_layout()
fig.savefig(FIG / "q2b_presenca_vs_simulado.png", dpi=150)
plt.close(fig)

# ===========================================================================
# Q3 — Desempenho por curso / matéria
# ===========================================================================
print("\n== Q3: desempenho por matéria ==")

diag = fact_matriculas.groupby("materia_declarada").agg(
    n_matriculas=("matricula_id", "count"),
    nota_diagnostico_media=("nota_diagnostico", "mean"),
    taxa_conclusao_pct=("status_matricula", lambda s: round((s == "Concluída").mean() * 100, 1)),
).round(1).sort_values("nota_diagnostico_media", ascending=False)

sim_join = fact_resultados.merge(dim_simulados[["simulado_id", "materia"]], on="simulado_id", how="left")
sim_mat = sim_join.groupby("materia").agg(
    n_resultados=("resultado_id", "count"),
    nota_simulado_media=("nota", "mean"),
    taxa_finalizacao_pct=("status_realizacao", lambda s: round((s == "Finalizado").mean() * 100, 1)),
).round(1)

q3 = diag.join(sim_mat, how="left")
print(q3)
metrics["q3_desempenho_por_materia"] = q3.reset_index().rename(columns={"index": "materia"}).to_dict(orient="records")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
diag_sorted = diag.sort_values("nota_diagnostico_media")
axes[0].barh(diag_sorted.index, diag_sorted["nota_diagnostico_media"], color=COLOR_PRIMARY)
axes[0].set_title("Nota média no diagnóstico de matrícula, por matéria")
axes[0].set_xlabel("Nota média (0–100)")

sim_sorted = sim_mat.sort_values("nota_simulado_media")
axes[1].barh(sim_sorted.index, sim_sorted["nota_simulado_media"], color=COLOR_ACCENT)
axes[1].set_title("Nota média nos simulados, por matéria")
axes[1].set_xlabel("Nota média (0–100)")
fig.tight_layout()
fig.savefig(FIG / "q3_desempenho_materias.png", dpi=150)
plt.close(fig)

fig, ax = plt.subplots(figsize=(7, 4.5))
conc_sorted = diag.sort_values("taxa_conclusao_pct")
ax.barh(conc_sorted.index, conc_sorted["taxa_conclusao_pct"], color=COLOR_PRIMARY)
ax.set_title("Taxa de conclusão da matrícula, por matéria")
ax.set_xlabel("% de matrículas concluídas")
fig.tight_layout()
fig.savefig(FIG / "q3b_taxa_conclusao_materia.png", dpi=150)
plt.close(fig)

# ===========================================================================
# Salvar métricas
# ===========================================================================
def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_clean(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return None if np.isnan(o) else float(o)
    if isinstance(o, float) and np.isnan(o):
        return None
    return o


with open(DOCS / "metricas.json", "w", encoding="utf-8") as f:
    json.dump(_clean(metrics), f, ensure_ascii=False, indent=2, default=str)

# ===========================================================================
# Gerar dashboard_data.json para visualização interativa
# ===========================================================================
dashboard_data = {
    "q1_por_ano": q1.reset_index().rename(columns={"ano_vestibular": "ano"}).to_dict(orient="records"),
    "q1_universidade": apr_uni.to_dict(),
    "q1_bolsa": apr_bolsa.to_dict(),
    
    "q2_attendance_points": attendance[["taxa_presenca_%", "aprovado"]].rename(
        columns={"taxa_presenca_%": "taxa", "aprovado": "aprovado"}
    ).to_dict(orient="records"),
    "q2_group_means": {
        "aprovado": float(grp_aprov.mean()),
        "nao_aprovado": float(grp_nao.mean())
    },
    "q2_pvalue": float(metrics.get("q2_mannwhitney_p_valor", 0)) if metrics.get("q2_mannwhitney_p_valor") else None,
    
    "q2b_scatter": att_res[["taxa_presenca_%", "nota_media_simulado"]].rename(
        columns={"taxa_presenca_%": "presenca", "nota_media_simulado": "nota"}
    ).to_dict(orient="records"),
    
    "q3_materia": q3.reset_index().rename(columns={"index": "materia"}).to_dict(orient="records")
}

with open(DOCS / "dashboard_data.json", "w", encoding="utf-8") as f:
    json.dump(_clean(dashboard_data), f, ensure_ascii=False, indent=2, default=str)

print("\nFiguras salvas em outputs/figures/.")
print("Métricas salvas em docs/metricas.json")
print("Dados do dashboard salvos em docs/dashboard_data.json")