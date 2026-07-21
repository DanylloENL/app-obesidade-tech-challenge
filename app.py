# ============================================================================
# TECH CHALLENGE - FASE 4 - DATA ANALYTICS
# APLICAÇÃO PREDITIVA - NÍVEL DE OBESIDADE
# ============================================================================
#
# Esta aplicação carrega o arquivo "modelo_obesidade.pkl" (gerado no notebook
# de treinamento a partir da planilha Obesity_Ana_lise_Preliminar.xlsx, aba
# Base_Data) e oferece uma tela onde o usuário preenche os mesmos campos que
# existem nessa base. A aplicação calcula o IMC exatamente como no notebook e
# envia os dados para o pipeline treinado (pré-processamento + modelo),
# retornando a classe prevista.
#
# Para rodar localmente:
#   streamlit run app.py
# ============================================================================

import pandas as pd
import joblib
import streamlit as st
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Preditor de Obesidade",
    page_icon="🩺",
    layout="centered",
)

# ----------------------------------------------------------------------------
# CARREGAMENTO DO MODELO
# ----------------------------------------------------------------------------
# O @st.cache_resource evita recarregar o arquivo .pkl a cada interação do
# usuário, deixando a aplicação mais rápida.
NOME_ARQUIVO_MODELO = "modelo_obesidade.pkl"


@st.cache_resource
def carregar_modelo(caminho: str):
    """Carrega a pipeline treinada (pré-processador + modelo)."""
    return joblib.load(caminho)


try:
    modelo = carregar_modelo(NOME_ARQUIVO_MODELO)
except FileNotFoundError:
    st.error(
        f"Arquivo '{NOME_ARQUIVO_MODELO}' não encontrado. "
        "Coloque o arquivo .pkl gerado pelo notebook na mesma pasta do app.py "
        "(veja o README para instruções de deploy)."
    )
    st.stop()

# ----------------------------------------------------------------------------
# DICIONÁRIO DE TRADUÇÃO DAS CLASSES PARA UMA LEITURA MAIS AMIGÁVEL
# ----------------------------------------------------------------------------
TRADUCAO_CLASSES = {
    "Abaixo do Peso": "Abaixo do peso",
    "Peso Normal": "Peso normal",
    "Sobrepeso Nível I": "Sobrepeso (nível I)",
    "Sobrepeso Nível II": "Sobrepeso (nível II)",
    "Obesidade Nível I": "Obesidade (nível I)",
    "Obesidade Nível II": "Obesidade (nível II)",
    "Obesidade Nível III": "Obesidade (nível III)",
}

# ----------------------------------------------------------------------------
# FAIXAS OFICIAIS DE IMC (OMS) — usadas para o gráfico comparativo
# ----------------------------------------------------------------------------
# Cada faixa tem: rótulo, limite inferior, limite superior e cor.
FAIXAS_OMS = [
    ("Abaixo do peso", 0, 18.5, "#5DA5DA"),
    ("Peso normal", 18.5, 25, "#60BD68"),
    ("Sobrepeso", 25, 30, "#F7DC6F"),
    ("Obesidade grau I", 30, 35, "#F4A460"),
    ("Obesidade grau II", 35, 40, "#E8743B"),
    ("Obesidade grau III", 40, 55, "#C0392B"),
]


def montar_grafico_imc_oms(imc_paciente: float):
    """Cria uma barra horizontal com as faixas da OMS e marca o IMC do paciente."""
    fig, ax = plt.subplots(figsize=(8, 1.8))

    for nome, inicio, fim, cor in FAIXAS_OMS:
        ax.barh(0, fim - inicio, left=inicio, color=cor, edgecolor="white", height=0.6)
        centro = inicio + (fim - inicio) / 2
        limite_texto = min(fim, 48)
        ax.text(min(centro, limite_texto - 2), -0.55, nome, ha="center", va="top", fontsize=8)

    limite_eixo = max(48, imc_paciente + 3)
    ax.set_xlim(0, limite_eixo)

    imc_no_grafico = min(imc_paciente, limite_eixo - 1)
    ax.axvline(imc_no_grafico, color="black", linewidth=2)
    ax.plot(imc_no_grafico, 0, marker="v", color="black", markersize=12)
    ax.text(
        imc_no_grafico, 0.55, f"IMC {imc_paciente:.1f}",
        ha="center", va="bottom", fontsize=10, fontweight="bold"
    )

    ax.set_ylim(-0.9, 0.9)
    ax.set_yticks([])
    ax.set_xlabel("IMC (kg/m²)")
    ax.spines[["top", "right", "left"]].set_visible(False)
    fig.tight_layout()
    return fig

# ----------------------------------------------------------------------------
# CABEÇALHO
# ----------------------------------------------------------------------------
st.title("🩺 Sistema Preditivo de Obesidade")
st.markdown(
    """
Preencha os campos abaixo com as informações do paciente. O sistema utiliza
um modelo de Machine Learning treinado com dados clínicos, comportamentais e
de estilo de vida para estimar o nível de obesidade.

*Ferramenta de apoio à decisão médica — não substitui avaliação clínica.*
"""
)

st.divider()

# ----------------------------------------------------------------------------
# FORMULÁRIO DE ENTRADA
# ----------------------------------------------------------------------------
# Os campos e as opções seguem exatamente o dicionário de dados do desafio.
with st.form("formulario_predicao"):

    st.subheader("Características da população")
    col1, col2 = st.columns(2)
    with col1:
        genero = st.selectbox("Gênero", options=["Feminino", "Masculino"])
        idade = st.number_input("Idade (anos)", min_value=14, max_value=100, value=30, step=1)
    with col2:
        altura = st.number_input("Altura (m)", min_value=1.30, max_value=2.20, value=1.70, step=0.01, format="%.2f")
        peso = st.number_input("Peso (kg)", min_value=30.0, max_value=250.0, value=70.0, step=0.5, format="%.1f")

    st.subheader("Histórico e hábitos alimentares")
    col3, col4 = st.columns(2)
    with col3:
        historico_familiar = st.selectbox(
            "Algum familiar tem/teve excesso de peso?", options=["Sim", "Não"]
        )
        favc = st.selectbox(
            "Come alimentos muito calóricos com frequência?", options=["Sim", "Não"]
        )
        caec = st.selectbox(
            "Come algo entre as refeições?",
            options=["Não", "As vezes", "Frequentemente", "Sempre"]
        )
    with col4:
        fcvc = st.slider("Frequência de consumo de vegetais", min_value=1, max_value=3, value=2, help="1 = raramente, 2 = às vezes, 3 = sempre")
        ncp = st.slider("Refeições principais por dia", min_value=1, max_value=4, value=3)
        calc = st.selectbox(
            "Frequência de consumo de álcool",
            options=["Não", "As vezes", "Frequentemente", "Sempre"]
        )

    st.subheader("Estilo de vida")
    col5, col6 = st.columns(2)
    with col5:
        fumante = st.selectbox("Fuma?", options=["Sim", "Não"])
        ch2o = st.slider("Consumo diário de água", min_value=1, max_value=3, value=2, help="1 = <1L, 2 = 1-2L, 3 = >2L")
        scc = st.selectbox(
            "Monitora as calorias que ingere?", options=["Sim", "Não"]
        )
    with col6:
        faf = st.slider("Frequência de atividade física (semana)", min_value=0, max_value=3, value=1, help="0 = nenhuma, 3 = 5x ou mais por semana")
        tue = st.slider("Tempo em dispositivos eletrônicos", min_value=0, max_value=2, value=1, help="0 = 0-2h/dia, 1 = 3-5h/dia, 2 = >5h/dia")
        mtrans = st.selectbox(
            "Meio de transporte habitual",
            options=["Automóvel", "Motocicleta", "Bicicleta", "Transporte Público", "A pé"]
        )

    enviado = st.form_submit_button("Gerar predição", use_container_width=True, type="primary")

# ----------------------------------------------------------------------------
# PREDIÇÃO
# ----------------------------------------------------------------------------
if enviado:

    # Calcula o IMC exatamente como foi feito no notebook de treinamento.
    imc = peso / (altura ** 2)

    # Monta um DataFrame com as mesmas colunas usadas no treinamento (X),
    # usando os nomes de coluna exatamente como aparecem na planilha
    # "Obesity_Ana_lise_Preliminar.xlsx" (aba Base_Data).
    entrada = pd.DataFrame([{
        "Gênero": genero,
        "Idade": idade,
        "Altura (m)": altura,
        "Peso (Kg)": peso,
        "Histórico Familiar": historico_familiar,
        "FAVC": favc,
        "FCVC": fcvc,
        "NCP": ncp,
        "CAEC": caec,
        "SMOKE": fumante,
        "CH2O": ch2o,
        "SCC": scc,
        "FAF": faf,
        "TUE": tue,
        "CALC": calc,
        "MTRANS": mtrans,
        "IMC": imc,
    }])

    previsao = modelo.predict(entrada)[0]
    classe_traduzida = TRADUCAO_CLASSES.get(previsao, previsao)

    st.divider()
    st.subheader("Resultado da predição")

    st.metric("IMC calculado", f"{imc:.2f}")
    st.success(f"**Nível de obesidade previsto:** {classe_traduzida}")

    # Gráfico comparando o IMC do paciente com as faixas oficiais da OMS.
    st.markdown("**Onde o IMC do paciente se encaixa (faixas da OMS):**")
    figura_imc = montar_grafico_imc_oms(imc)
    st.pyplot(figura_imc, use_container_width=True)
    st.caption(
        "Faixas de referência da Organização Mundial da Saúde (OMS) para adultos. "
        "O IMC é uma medida populacional e não substitui avaliação individualizada."
    )

    # Se o modelo suportar probabilidades, mostra o ranking de confiança.
    if hasattr(modelo, "predict_proba"):
        probabilidades = modelo.predict_proba(entrada)[0]
        classes = modelo.named_steps["modelo"].classes_ if hasattr(modelo, "named_steps") else modelo.classes_

        tabela_prob = pd.DataFrame({
            "Classe": [TRADUCAO_CLASSES.get(c, c) for c in classes],
            "Probabilidade (%)": (probabilidades * 100).round(2),
        }).sort_values("Probabilidade (%)", ascending=True)

        st.markdown("**Distribuição de probabilidade entre as classes previstas pelo modelo:**")

        fig_prob, ax_prob = plt.subplots(figsize=(8, 3.5))
        cores_barras = [
            "#C0392B" if c == classe_traduzida else "#95A5A6"
            for c in tabela_prob["Classe"]
        ]
        ax_prob.barh(tabela_prob["Classe"], tabela_prob["Probabilidade (%)"], color=cores_barras)
        for i, valor in enumerate(tabela_prob["Probabilidade (%)"]):
            ax_prob.text(valor + 1, i, f"{valor:.1f}%", va="center", fontsize=8)
        ax_prob.set_xlabel("Probabilidade (%)")
        ax_prob.set_xlim(0, 100)
        ax_prob.spines[["top", "right"]].set_visible(False)
        fig_prob.tight_layout()

        st.pyplot(fig_prob, use_container_width=True)

    st.caption(
        "Resultado gerado por um modelo de Machine Learning para apoio à decisão. "
        "A confirmação diagnóstica deve sempre ser feita por um profissional de saúde."
    )
