import pandas as pd
import streamlit as st
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# --- Dados simulados para treinar o modelo ---
data = {
    "Matemática": [450, 600, 300, 700, 400, 650, 480, 520],
    "Linguagens": [550, 400, 350, 600, 300, 700, 500, 450],
    "Ciências Humanas": [400, 620, 310, 680, 420, 630, 470, 510],
    "Ciências da Natureza": [430, 610, 290, 670, 410, 640, 460, 520],
    "Redação": [480, 590, 300, 690, 420, 600, 490, 530],
    "Dificuldade": [1, 0, 1, 0, 1, 0, 1, 0]
}

df = pd.DataFrame(data)
X = df.drop("Dificuldade", axis=1)
y = df["Dificuldade"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Função para prever dificuldade com o modelo
def prever_dificuldade(modelo, dados_alunos):
    return modelo.predict(dados_alunos)

# Recomendações baseadas nas matérias
recomendacoes = {
    "Matemática": "🔢 [Revisão Matemática Básica - YouTube](https://www.youtube.com/watch?v=ZB1H1awtOeM)",
    "Linguagens": "📚 [Interpretação de Texto ENEM - PDF](https://encurtador.com.br/ktzGH)",
    "Ciências Humanas": "🌍 [Resumo História e Geografia - Blog](https://encurtador.com.br/adnX8)",
    "Ciências da Natureza": "🧪 [Ciências com Experimentos - YouTube](https://www.youtube.com/watch?v=Ys6uKBz2m9w)",
    "Redação": "✍️ [Redação nota 1000 - Videoaula](https://www.youtube.com/watch?v=1yoKcR5QFyY)"
}

# Inicializa session_state para dificuldades
if "dificuldades" not in st.session_state:
    st.session_state.dificuldades = {}

# Menu lateral para escolher página
pagina = st.sidebar.selectbox("Escolha a página", ["Diagnóstico", "Cronograma"])

if pagina == "Diagnóstico":
    st.title("🎓 Diagnóstico de Dificuldades")
    uploaded_file = st.file_uploader("📤 Envie arquivo CSV com notas", type="csv")

    if uploaded_file:
        df_alunos = pd.read_csv(uploaded_file)
        st.write("📄 Dados recebidos:", df_alunos)

        colunas_esperadas = ["Matemática", "Linguagens", "Ciências Humanas", "Ciências da Natureza", "Redação"]
        if all(col in df_alunos.columns for col in colunas_esperadas):
            X_novo = df_alunos[colunas_esperadas]
            previsoes = prever_dificuldade(model, X_novo)
            df_alunos["Risco de dificuldade"] = previsoes

            st.write("📝 Resultado da análise:")
            st.dataframe(df_alunos)

            # Armazena as dificuldades por aluno em session_state
            st.session_state.dificuldades = {}
            for idx, row in df_alunos.iterrows():
                difs = []
                for mat in colunas_esperadas:
                    if row[mat] < 500:  # Critério para dificuldade
                        difs.append(mat)
                st.session_state.dificuldades[idx] = difs

                st.markdown("---")
                st.subheader(f"Aluno {idx + 1}")

                if row["Risco de dificuldade"] == 1:
                    st.warning(f"⚠️ Risco de dificuldade nas áreas: {', '.join(difs)}")
                    st.markdown("📌 Recomendações:")
                    for d in difs:
                        if d in recomendacoes:
                            st.markdown(recomendacoes[d], unsafe_allow_html=True)
                else:
                    st.success("✅ Sem risco de dificuldade detectado.")
        else:
            st.error(f"Arquivo deve conter as colunas: {', '.join(colunas_esperadas)}")

elif pagina == "Cronograma":
    st.title("📅 Cronograma Personalizado")

    if not st.session_state.dificuldades:
        st.warning("⚠️ Faça o diagnóstico antes de criar o cronograma.")
    else:
        aluno_selecionado = st.number_input(
            "Selecione o número do aluno para criar o cronograma (ex: 1 para primeiro aluno)",
            min_value=1, max_value=len(st.session_state.dificuldades)
        )

        tempo_diario = st.number_input("Horas disponíveis para estudo por dia", min_value=1, max_value=12)

        if st.button("Gerar cronograma"):
            dificuldades_aluno = st.session_state.dificuldades[aluno_selecionado - 1]

            if not dificuldades_aluno:
                st.success("✅ Aluno sem dificuldades detectadas, mantenha os estudos!")
            else:
                st.subheader(f"Cronograma para o Aluno {aluno_selecionado}")

                # Dividir o tempo diário proporcionalmente entre as matérias com dificuldade
                tempo_por_materia = tempo_diario / len(dificuldades_aluno)

                for mat in dificuldades_aluno:
                    st.write(f"- {mat}: {tempo_por_materia:.2f} horas por dia")
