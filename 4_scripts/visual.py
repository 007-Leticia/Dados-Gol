import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, inspect
import plotly.express as px

st.title("DADOS GOL")
st.write("Estes são gráficos sobre a empresa GOL")
engine = create_engine('sqlite:///banco.db', echo=True)

def check_table_exists(engine, table_name):
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()
def load_data():
    if check_table_exists(engine, 'dados'):
        try:
            df = pd.read_sql('SELECT * FROM dados', con=engine)
            return df
        except Exception as e:
            st.error(f"Erro ao carregar dados do banco de dados: {e}")
            return None
    else:
        st.error("A tabela 'dados' não existe no banco de dados.")
        return None

# Carregar dados
df = load_data()

# Verificar se os dados foram carregados corretamente
if df is not None:
    st.write("Colunas do DataFrame:", df.columns)

    st.header("Análise dos Dados")
    col1, col2 = st.columns(2)

    # Ajuste para verificar e corrigir o nome da coluna
    if 'Dia' in df.columns:
        df_media = df.groupby('Dia')['Preco'].mean().reset_index()
    else:
        st.error("A coluna 'Dia' não foi encontrada no banco de dados. Verifique a estrutura do banco.")
        df_media = None

    if df_media is not None:
        col1.header("Tabela com média de preços por dia")
        col1.write(df_media)

    col2.header("Opções")
    operacao = col2.radio("Escolha a operação:", ["Média", "Mediana", "Desvio Padrão"])

    if operacao == "Média":
        media = df['Preco'].mean()
        col2.write(f"A média dos preços é: {media:.2f}")
    elif operacao == 'Mediana':
        mediana = df['Preco'].median()
        col2.write(f"A mediana dos preços é: {mediana:.2f}")
    else:
        dp = df['Preco'].std()
        col2.write(f"O desvio padrão dos preços é: {dp:.2f}")

    if "Partida_horario" in df.columns:
        st.title("Análise Univariada dos Dados")
        with st.expander("Clique aqui para visualizar a análise univariada"):
            st.write("Aqui estão análises gráficas realizadas com os dados fornecidos:")
            fig1 = px.histogram(df, x="Preco", title="Distribuição de Preços", nbins=4)
            st.plotly_chart(fig1)

            df["Partida_horario"] = df["Partida_horario"].str.strip()
            df["Partida_horario"] = pd.to_datetime(df["Partida_horario"], format="%H:%M").dt.time

            def categorizar_periodo(horario):
                if horario >= pd.to_datetime("06:00", format="%H:%M").time() and horario < pd.to_datetime("12:00", format="%H:%M").time():
                    return "Manhã"
                elif horario >= pd.to_datetime("12:00", format="%H:%M").time() and horario < pd.to_datetime("18:00", format="%H:%M").time():
                    return "Tarde"
                else:
                    return "Noite"

            df["Periodo"] = df["Partida_horario"].apply(categorizar_periodo)

            fig2 = px.bar(df, x="Periodo", title="Frequência de Voos por Período", labels={"Periodo": "Período do Dia"})
            st.plotly_chart(fig2)

            fig3 = px.pie(df, names="Dia", title="Distribuição por dias de Voo")
            st.plotly_chart(fig3)

            fig4 = px.box(df, y="Preco", title="Boxplot dos Preços", points="all")
            st.plotly_chart(fig4)

    st.title("Análise Multivariada dos Dados")
    with st.expander("Clique aqui para visualizar a análise multivariada"):
        if "Partida_horario" in df.columns:
            fig5 = px.scatter(df, x="Partida_horario", y="Preco", title="Relação entre Preço e Hora de Partida",
                              labels={"Partida_horario": "Hora de Partida", "Preco": "Preço"})
            st.plotly_chart(fig5)

        fig6 = px.box(df, x="Periodo", y="Preco", title="Distribuição dos Preços por Período", points="all",
                      labels={"Periodo": "Período do Dia", "Preco": "Preço"})
        st.plotly_chart(fig6)

        fig7 = px.bar(df_media, x="Dia", y="Preco",
                      title="Variação do Preço Médio por Dia",
                      labels={"Partida_horario": "Data", "Preco": "Preço Médio"},
                      color="Dia",
                      barmode="group")
        st.plotly_chart(fig7)

else:
    st.warning("Sem dados disponíveis para análise. Certifique-se de que a tabela 'dados' existe no banco de dados.")
