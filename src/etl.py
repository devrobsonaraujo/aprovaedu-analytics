# -*- coding: utf-8 -*-
"""
ETL - AprovaEdu Analytics
Le as amostras brutas (xlsx), aplica tratamentos de qualidade de dados,
normaliza categorias, corrige datas em formatos mistos, deduplica registros
e gera uma base tratada (modelo dimensional simples: dimensões + fatos)
em CSV, pronta para as análises obrigatórias.

Todas as decisões de tratamento estão comentadas no código e resumidas
no README.md / RELATORIO_FINAL.md.
"""

import re
import unicodedata
import pandas as pd
import numpy as np
from pathlib import Path

RAW_PATH = Path(__file__).resolve().parents[1] / "data" / "raw"
OUT_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

LOG = []  # log de decisões de tratamento (vira docs/log_tratamento.md)


def log(msg):
    LOG.append(msg)
    print(msg)


# ---------------------------------------------------------------------------
# Helpers genéricos
# ---------------------------------------------------------------------------

def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def parse_date_mixed(series: pd.Series) -> pd.Series:
    """Datas chegam em formatos misturados na mesma coluna:
    YYYY-MM-DD, YYYY/MM/DD, DD/MM/YYYY, MM-DD-YYYY, e datetime com hora.
    Estratégia: tentar formatos conhecidos em ordem; o que não bater com
    nenhum formato explícito cai no parser genérico do pandas (dayfirst=False)
    como último recurso.
    """
    s = series.astype(str).str.strip()
    s = s.replace({"None": np.nan, "nan": np.nan, "NaT": np.nan})

    formats = [
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%m-%d-%Y",
    ]
    result = pd.Series(pd.NaT, index=s.index)
    remaining = s.notna()
    for fmt in formats:
        if not remaining.any():
            break
        parsed = pd.to_datetime(s[remaining], format=fmt, errors="coerce")
        ok = parsed.notna()
        idx = remaining[remaining].index[ok.values]
        result.loc[idx] = parsed[ok].values
        remaining.loc[idx] = False
    # fallback genérico para o que sobrar
    if remaining.any():
        parsed = pd.to_datetime(s[remaining], errors="coerce", dayfirst=True)
        result.loc[remaining] = parsed
    return result


def norm_text(series: pd.Series) -> pd.Series:
    """Normalização básica de texto: strip espaços, remove espaços duplos."""
    return (
        series.astype(str)
        .str.strip()
        .replace({"None": np.nan, "nan": np.nan, "": np.nan})
        .str.replace(r"\s+", " ", regex=True)
    )


def map_categoria(series: pd.Series, mapping: dict, default_titlecase=True) -> pd.Series:
    """Normaliza categorias usando um dicionário {variação_lower_sem_acento: valor_canonico}."""
    s = norm_text(series)

    def _map(v):
        if pd.isna(v):
            return v
        key = strip_accents(v).lower().strip()
        if key in mapping:
            return mapping[key]
        return v.title() if default_titlecase else v

    return s.map(_map)


def to_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series.astype(str).str.replace(",", ".", regex=False), errors="coerce")


# ---------------------------------------------------------------------------
# 1. LEITURA DAS BASES BRUTAS
# ---------------------------------------------------------------------------

def load_raw():
    # Mapeamento do nome lógico esperado pelo ETL para o nome do arquivo CSV
    file_mapping = {
        "Amostra_Professores": "professores.csv",
        "Amostra_Estudantes": "estudantes.csv",
        "Amostra_Ofertas_Curso": "ofertas_curso.csv",
        "Amostra_Matriculas": "matriculas.csv",
        "Amostra_Aprovacoes": "aprovacoes_vestibular.csv",
        "Amostra_Simulados": "simulados.csv",
        "Amostra_Resultados_Sim": "resultados_simulados.csv",
        "Amostra_Aulas": "aulas.csv",
        "Amostra_Presencas_Aulas": "presencas_aulas.csv",
    }
    
    raw = {}
    for key, filename in file_mapping.items():
        filepath = RAW_PATH / filename
        if filepath.exists():
            # Tenta ler com separador vírgula (padrão) ou ponto e vírgula se necessário
            try:
                raw[key] = pd.read_csv(filepath, dtype=str)
            except Exception:
                raw[key] = pd.read_csv(filepath, dtype=str, sep=";")
        else:
            log(f"[AVISO] Arquivo não encontrado: {filepath}")

    log(f"[LOAD] {len(raw)} tabelas lidas de {RAW_PATH}")
    for k, v in raw.items():
        log(f"  - {k}: {v.shape[0]} linhas x {v.shape[1]} colunas")
    return raw


# ---------------------------------------------------------------------------
# 2. DIMENSÃO PROFESSORES
# ---------------------------------------------------------------------------

MATERIA_MAP = {
    "matematica": "Matemática", "mat.": "Matemática", "mat": "Matemática",
    "fisica": "Física",
    "quimica": "Química",
    "biologia": "Biologia",
    "portugues": "Português",
    "historia": "História",
    "geografia": "Geografia",
    "filosofia": "Filosofia",
    "sociologia": "Sociologia",
    "ingles": "Inglês",
    "redacao": "Redação",
}


def clean_professores(df):
    df = df.copy()
    df["nome_professor"] = norm_text(df["nome_professor"])
    df["email_professor"] = norm_text(df["email_professor"]).str.lower()
    df["materia_principal"] = map_categoria(df["materia_principal"], MATERIA_MAP)
    df["materias_ensina"] = norm_text(df["materias_ensina"])
    # lista de matérias que o professor ensina, cada item normalizado
    df["materias_ensina_lista"] = df["materias_ensina"].fillna("").apply(
        lambda s: [MATERIA_MAP.get(strip_accents(x).lower().strip(), x.strip())
                   for x in s.split(";") if x.strip()]
    )
    df["data_contratacao"] = parse_date_mixed(df["data_contratacao"])
    df["status_professor"] = map_categoria(
        df["status_professor"], {"ativo": "Ativo", "inativo": "Inativo"}
    )
    df["unidade_base"] = norm_text(df["unidade_base"])
    df["carga_horaria_semanal"] = to_numeric(df["carga_horaria_semanal"])
    df["observacoes"] = norm_text(df["observacoes"])

    dup = df["professor_id"].duplicated().sum()
    log(f"[PROFESSORES] duplicidades em professor_id: {dup}")
    df = df.drop_duplicates(subset=["professor_id"])
    log("[PROFESSORES] materia_principal normalizada (ex.: 'Mat.', 'Matematica' -> 'Matemática')")
    return df


# ---------------------------------------------------------------------------
# 3. DIMENSÃO ESTUDANTES
# ---------------------------------------------------------------------------

def clean_cpf(series):
    def _fmt(v):
        if pd.isna(v):
            return np.nan
        digits = re.sub(r"\D", "", v)
        if len(digits) != 11:
            return np.nan  # cpf ficticio invalido -> nulo (mantém rastreabilidade sem inventar dado)
        return f"{digits[0:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:11]}"

    return series.map(_fmt)


def clean_estudantes(df):
    df = df.copy()
    df["nome_aluno"] = norm_text(df["nome_aluno"])
    df["cpf_ficticio"] = clean_cpf(df["cpf_ficticio"])
    df["email_aluno"] = norm_text(df["email_aluno"]).str.lower()
    df["telefone"] = norm_text(df["telefone"])
    df["data_nascimento"] = parse_date_mixed(df["data_nascimento"])
    df["cidade"] = map_categoria(df["cidade"], {})  # apenas casing (title case)
    df["escola_origem"] = map_categoria(
        df["escola_origem"],
        {"publica": "Pública", "privada": "Privada", "federal": "Federal",
         "nao informado": "Não informado"},
    )
    df["escola_origem"] = df["escola_origem"].fillna("Não informado")
    df["data_cadastro"] = parse_date_mixed(df["data_cadastro"])
    df["canal_captacao"] = map_categoria(df["canal_captacao"], {})

    dup = df["aluno_id"].duplicated().sum()
    log(f"[ESTUDANTES] duplicidades em aluno_id: {dup}")
    df = df.drop_duplicates(subset=["aluno_id"])
    log("[ESTUDANTES] cidade/escola_origem/canal_captacao normalizados (casing); "
        "CPFs fora do padrão (!=11 dígitos) marcados como nulos por não serem confiáveis")
    return df


# ---------------------------------------------------------------------------
# 4. DIMENSÃO OFERTAS DE CURSO
# ---------------------------------------------------------------------------

def clean_ofertas(df, dim_professores):
    df = df.copy()
    df["ano"] = to_numeric(df["ano"]).astype("Int64")
    df["turma"] = norm_text(df["turma"])
    df["turno"] = norm_text(df["turno"])
    df["unidade"] = norm_text(df["unidade"])
    df["materia"] = map_categoria(df["materia"], MATERIA_MAP)
    df["modalidade"] = map_categoria(df["modalidade"], {})
    df["carga_horaria_total"] = to_numeric(df["carga_horaria_total"])
    df["preco_lista"] = to_numeric(df["preco_lista"])
    df["data_inicio"] = parse_date_mixed(df["data_inicio"])
    df["data_fim"] = parse_date_mixed(df["data_fim"])

    # Denormalização: professor_nome_informado deve bater com dim_professores
    nomes = dim_professores.set_index("professor_id")["nome_professor"]
    df["professor_nome_dim"] = df["professor_id"].map(nomes)
    diverge = (
        df["professor_nome_informado"].astype(str).str.strip().str.lower()
        != df["professor_nome_dim"].astype(str).str.strip().str.lower()
    ) & df["professor_nome_dim"].notna()
    log(f"[OFERTAS] divergências entre professor_nome_informado e cadastro do professor: {diverge.sum()}")
    # decisão: manter nome oficial da dimensão (fonte de verdade = cadastro de professor)
    df["professor_nome"] = df["professor_nome_dim"].fillna(df["professor_nome_informado"])
    df = df.drop(columns=["professor_nome_informado", "professor_nome_dim"])

    dup = df["oferta_id"].duplicated().sum()
    log(f"[OFERTAS] duplicidades em oferta_id: {dup}")
    df = df.drop_duplicates(subset=["oferta_id"])
    log("[OFERTAS] materia normalizada; nome do professor passou a vir da dimensão "
        "(fonte única da verdade) em vez do campo digitado na tabela fato")
    return df


# ---------------------------------------------------------------------------
# 5. FATO MATRICULAS
# ---------------------------------------------------------------------------

def clean_matriculas(df):
    df = df.copy()
    df["ano"] = to_numeric(df["ano"]).astype("Int64")
    df["materia_declarada"] = map_categoria(df["materia_declarada"], MATERIA_MAP)
    df["data_matricula"] = parse_date_mixed(df["data_matricula"])
    df["bolsa_percentual"] = to_numeric(df["bolsa_percentual"]).clip(0, 100)
    df["status_matricula"] = map_categoria(
        df["status_matricula"],
        {"ativa": "Ativa", "cancelada": "Cancelada", "concluida": "Concluída", "trancada": "Trancada"},
    )
    df["nota_diagnostico"] = to_numeric(df["nota_diagnostico"])
    # nota_diagnostico fora de faixa plausível (0-100) -> nula
    invalid = ~df["nota_diagnostico"].between(0, 100) & df["nota_diagnostico"].notna()
    log(f"[MATRICULAS] nota_diagnostico fora da faixa 0-100: {invalid.sum()} -> tratada como nula")
    df.loc[invalid, "nota_diagnostico"] = np.nan
    df["origem_captacao"] = map_categoria(df["origem_captacao"], {})

    dup = df["matricula_id"].duplicated().sum()
    log(f"[MATRICULAS] duplicidades em matricula_id: {dup}")
    df = df.drop_duplicates(subset=["matricula_id"])
    return df


# ---------------------------------------------------------------------------
# 6. FATO APROVACOES
# ---------------------------------------------------------------------------

UNIV_MAP = {
    "ufc": "UFC", "uece": "UECE", "urn": "UERN", "uern": "UERN", "ufrn": "UFRN",
    "ufca": "UFCA", "ufpe": "UFPE", "unifor": "UNIFOR", "unilab": "UNILAB",
    "uva": "UVA", "ifce": "IFCE",
}


def clean_aprovacoes(df):
    df = df.copy()
    df["ano_vestibular"] = to_numeric(df["ano_vestibular"]).astype("Int64")
    df["universidade"] = map_categoria(df["universidade"], UNIV_MAP, default_titlecase=False)
    df["curso_aprovado"] = norm_text(df["curso_aprovado"])
    df["modalidade_vaga"] = map_categoria(
        df["modalidade_vaga"],
        {"ampla concorrencia": "Ampla concorrência", "cota escola publica": "Cota escola pública",
         "pcd": "PCD", "ppi": "PPI"},
    )
    df["bolsa_aprovacao"] = map_categoria(df["bolsa_aprovacao"], {"sim": "Sim", "nao": "Não", "parcial": "Parcial"})
    df["data_resultado"] = parse_date_mixed(df["data_resultado"])
    df["nota_final_vestibular"] = to_numeric(df["nota_final_vestibular"])
    df["campus"] = norm_text(df["campus"])

    # "chamada" mistura duas informações: forma de ingresso (SISU / Vestibular próprio)
    # e a chamada numérica (1ª/2ª chamada / Lista de espera), além do marcador de
    # teste 'Cadastro duplicado?'. Não é possível separar com segurança sem
    # dicionário de negócio adicional, então preservamos o campo original em
    # 'chamada_bruta' e criamos uma flag de qualidade.
    df["chamada_bruta"] = norm_text(df["chamada"])
    df["flag_registro_teste"] = df["chamada_bruta"].str.lower().str.contains("duplicado", na=False)

    before = len(df)
    # Deduplicação de negócio: mesmo aluno, mesmo ano, mesma nota e mesma
    # universidade = mesma aprovação lançada 2x (confirmado nos dados: os
    # registros marcados 'Cadastro duplicado?' repetem aluno/ano/nota já
    # existentes). Mantém o primeiro registro (menor aprovacao_id).
    df = df.sort_values("aprovacao_id")
    dedup_keys = ["aluno_id", "ano_vestibular", "universidade", "nota_final_vestibular"]
    dup_mask = df.duplicated(subset=dedup_keys, keep="first")
    log(f"[APROVACOES] registros duplicados (mesmo aluno/ano/universidade/nota): {dup_mask.sum()} de {before}")
    df = df[~dup_mask].drop(columns=["chamada_bruta", "flag_registro_teste", "chamada"])

    dup_id = df["aprovacao_id"].duplicated().sum()
    log(f"[APROVACOES] duplicidades remanescentes em aprovacao_id: {dup_id}")
    return df


# ---------------------------------------------------------------------------
# 7. DIMENSÃO SIMULADOS
# ---------------------------------------------------------------------------

def clean_simulados(df, dim_professores):
    df = df.copy()
    df["ano"] = to_numeric(df["ano"]).astype("Int64")
    df["data_simulado"] = parse_date_mixed(df["data_simulado"])
    df["materia"] = map_categoria(df["materia"], MATERIA_MAP)
    df["dificuldade"] = map_categoria(df["dificuldade"], {"dificil": "Difícil", "facil": "Fácil", "media": "Média"})
    df["tipo_simulado"] = norm_text(df["tipo_simulado"])
    df["total_questoes"] = to_numeric(df["total_questoes"])
    df["tempo_limite_min"] = to_numeric(df["tempo_limite_min"])
    df["tema"] = norm_text(df["tema"])

    nomes = dim_professores.set_index("professor_id")["nome_professor"]
    df["professor_nome"] = df["professor_id"].map(nomes).fillna(df["professor_nome_informado"])
    df = df.drop(columns=["professor_nome_informado"])

    dup = df["simulado_id"].duplicated().sum()
    log(f"[SIMULADOS] duplicidades em simulado_id: {dup}")
    df = df.drop_duplicates(subset=["simulado_id"])
    return df


# ---------------------------------------------------------------------------
# 8. FATO RESULTADOS_SIM
# ---------------------------------------------------------------------------

def clean_resultados_sim(df):
    df = df.copy()
    df["ano"] = to_numeric(df["ano"]).astype("Int64")
    df["status_realizacao"] = map_categoria(
        df["status_realizacao"], {"finalizado": "Finalizado", "ausente": "Ausente", "incompleto": "Incompleto"}
    )
    df["nota"] = to_numeric(df["nota"])
    df["acertos"] = to_numeric(df["acertos"])
    df["tempo_finalizacao_min"] = to_numeric(df["tempo_finalizacao_min"])
    df["inicio_simulado"] = parse_date_mixed(df["inicio_simulado"])
    df["dispositivo"] = map_categoria(df["dispositivo"], {})
    df["tentativas"] = to_numeric(df["tentativas"])
    df["unidade_aplicacao"] = map_categoria(df["unidade_aplicacao"], {})

    # Outliers: nota deve estar entre 0 e 100 (escala do simulado); valores
    # acima de 100 são erro de digitação/lançamento -> nulos
    bad_nota = ~df["nota"].between(0, 100) & df["nota"].notna()
    log(f"[RESULTADOS_SIM] notas fora da faixa 0-100: {bad_nota.sum()} -> tratadas como nulas")
    df.loc[bad_nota, "nota"] = np.nan

    # tempo_finalizacao_min = 0 com status Finalizado é implausível -> nulo
    bad_tempo = (df["tempo_finalizacao_min"] <= 0) & (df["status_realizacao"] == "Finalizado")
    log(f"[RESULTADOS_SIM] tempo de finalização <=0 em simulados 'Finalizado': {bad_tempo.sum()} -> tratados como nulos")
    df.loc[bad_tempo, "tempo_finalizacao_min"] = np.nan

    # Ausente/Incompleto não deveriam ter nota -> nula para evitar inconsistência
    incons = df["status_realizacao"].isin(["Ausente"]) & df["nota"].notna()
    log(f"[RESULTADOS_SIM] status 'Ausente' com nota preenchida (inconsistente): {incons.sum()} -> nota anulada")
    df.loc[incons, "nota"] = np.nan

    dup = df["resultado_id"].duplicated().sum()
    log(f"[RESULTADOS_SIM] duplicidades em resultado_id: {dup}")
    df = df.drop_duplicates(subset=["resultado_id"])
    return df


# ---------------------------------------------------------------------------
# 9. FATO AULAS
# ---------------------------------------------------------------------------

def clean_aulas(df):
    df = df.copy()
    df["ano"] = to_numeric(df["ano"]).astype("Int64")
    df["data_aula"] = parse_date_mixed(df["data_aula"])
    df["materia"] = map_categoria(df["materia"], MATERIA_MAP)
    df["turma"] = norm_text(df["turma"])
    df["tema_aula"] = norm_text(df["tema_aula"])
    df["duracao_min"] = to_numeric(df["duracao_min"])
    df["modalidade_aula"] = map_categoria(df["modalidade_aula"], {})

    dup = df["aula_id"].duplicated().sum()
    log(f"[AULAS] duplicidades em aula_id: {dup}")
    df = df.drop_duplicates(subset=["aula_id"])
    return df


# ---------------------------------------------------------------------------
# 10. FATO PRESENCAS_AULAS
# ---------------------------------------------------------------------------

def clean_presencas(df):
    df = df.copy()
    df["status_presenca"] = map_categoria(
        df["status_presenca"],
        {"presente": "Presente", "ausente": "Ausente", "atrasado": "Atrasado", "justificado": "Justificado"},
    )
    df["atraso_min"] = to_numeric(df["atraso_min"]).clip(lower=0)
    df["justificativa"] = norm_text(df["justificativa"])

    dup = df["presenca_id"].duplicated().sum()
    log(f"[PRESENCAS] duplicidades em presenca_id: {dup}")
    df = df.drop_duplicates(subset=["presenca_id"])
    return df


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    raw = load_raw()

    dim_professores = clean_professores(raw["Amostra_Professores"])
    dim_estudantes = clean_estudantes(raw["Amostra_Estudantes"])
    dim_ofertas = clean_ofertas(raw["Amostra_Ofertas_Curso"], dim_professores)
    fact_matriculas = clean_matriculas(raw["Amostra_Matriculas"])
    fact_aprovacoes = clean_aprovacoes(raw["Amostra_Aprovacoes"])
    dim_simulados = clean_simulados(raw["Amostra_Simulados"], dim_professores)
    fact_resultados_sim = clean_resultados_sim(raw["Amostra_Resultados_Sim"])
    fact_aulas = clean_aulas(raw["Amostra_Aulas"])
    fact_presencas = clean_presencas(raw["Amostra_Presencas_Aulas"])

    # Integridade referencial básica (log de órfãos, sem descartar automaticamente,
    # pois a amostra fornecida é um recorte e é esperado que nem toda FK exista)
    def check_fk(fact, col, dim, dim_col, name):
        orphans = ~fact[col].isin(dim[dim_col])
        log(f"[FK CHECK] {name}: {orphans.sum()} de {len(fact)} registros com {col} não encontrado na dimensão")

    check_fk(fact_matriculas, "aluno_id", dim_estudantes, "aluno_id", "Matriculas -> Estudantes")
    check_fk(fact_matriculas, "oferta_id", dim_ofertas, "oferta_id", "Matriculas -> Ofertas")
    check_fk(fact_aprovacoes, "aluno_id", dim_estudantes, "aluno_id", "Aprovacoes -> Estudantes")
    check_fk(fact_resultados_sim, "aluno_id", dim_estudantes, "aluno_id", "Resultados_Sim -> Estudantes")
    check_fk(fact_resultados_sim, "simulado_id", dim_simulados, "simulado_id", "Resultados_Sim -> Simulados")
    check_fk(fact_aulas, "oferta_id", dim_ofertas, "oferta_id", "Aulas -> Ofertas")
    check_fk(fact_presencas, "aula_id", fact_aulas, "aula_id", "Presencas -> Aulas")
    check_fk(fact_presencas, "aluno_id", dim_estudantes, "aluno_id", "Presencas -> Estudantes")

    tables = {
        "dim_professores": dim_professores,
        "dim_estudantes": dim_estudantes,
        "dim_ofertas": dim_ofertas,
        "dim_simulados": dim_simulados,
        "fact_matriculas": fact_matriculas,
        "fact_aprovacoes": fact_aprovacoes,
        "fact_resultados_sim": fact_resultados_sim,
        "fact_aulas": fact_aulas,
        "fact_presencas": fact_presencas,
    }

    for name, df in tables.items():
        path = OUT_DIR / f"{name}.csv"
        df.to_csv(path, index=False)
        log(f"[SAVE] {name}.csv -> {df.shape[0]} linhas x {df.shape[1]} colunas")

    # salvar log de tratamento
    docs_dir = Path(__file__).resolve().parents[1] / "docs"
    docs_dir.mkdir(exist_ok=True)
    with open(docs_dir / "log_tratamento.md", "w", encoding="utf-8") as f:
        f.write("# Log de Decisões de Tratamento — ETL AprovaEdu Analytics\n\n")
        f.write("Gerado automaticamente pela execução de `src/etl.py`.\n\n")
        f.write("```\n")
        f.write("\n".join(LOG))
        f.write("\n```\n")

    return tables


if __name__ == "__main__":
    main()
