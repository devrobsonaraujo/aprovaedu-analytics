# 📸 Como Adicionar Screenshots dos Dashboards

Se você não conseguir ativar GitHub Pages ou preferir ter screenshots estáticos:

## Opção 1: Tirar prints manualmente (Windows)

1. Abra `dashboard.html` no navegador
2. Pressione `Win + Shift + S` (ferramenta de recorte)
3. Selecione a área do dashboard
4. Salve como `dashboard_overview.png` nesta pasta

Repita para `dashboard_logap.html`

**Sugestão de prints:**
- `01_dashboard_header.png` - Header e KPIs
- `02_evolucao_aprovacoes.png` - Gráfico Q1
- `03_presenca_aprovacao.png` - Gráfico Q2
- `04_desempenho_materias.png` - Gráfico Q3
- `05_dashboard_logap_full.png` - Dashboard Logap completo

---

## Opção 2: Screenshot automático (requer pacote)

```powershell
# Instalar selenium e webdriver
pip install selenium pillow

# Executar script de screenshot (se criar um)
python scripts/take_screenshots.py
```

---

## Opção 3: Usar ferramenta online

1. Acesse https://www.screenshotmachine.com/
2. Cole o caminho local ou suba o HTML temporariamente
3. Faça o download do screenshot
4. Salve nesta pasta

---

## ❌ Se não tiver tempo

**Não é obrigatório ter screenshots!** O dashboard HTML funcionando já é suficiente.

Basta garantir que:
1. Os arquivos `.html` estão no repositório
2. No README você menciona: "Dashboards em `outputs/*.html` - abrir localmente"
3. Durante apresentação (se houver), você abre ao vivo

---

## 📝 O que fazer após adicionar screenshots

Se adicionar prints, mencione no `README.md`:

```markdown
## 📊 Visualizações

### Dashboards Interativos
- `outputs/dashboard.html` - Versão AprovaEdu
- `outputs/dashboard_logap.html` - Versão Logap

### Screenshots
Veja `outputs/screenshots/` para visualizações estáticas dos dashboards.
```
