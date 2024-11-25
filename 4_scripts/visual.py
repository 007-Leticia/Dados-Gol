import streamlit as st
import pandas as pd
import requests
from sqlalchemy import create_engine
import plotly.express as px

API = 'http://127.0.0.1:5000/' 
url = API + 'dados-brutos'  

st.title("DADOS GOL")
st.write("Estes são gráficos sobre a empresa GOL")
engine = create_engine('sqlite:///banco.db', echo=True)
def get_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()  
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao fazer a requisição: {e}")
        return None
dados = get_data(url)
if dados:
    df = pd.DataFrame(dados) 
    df.to_sql('dados', con=engine, if_exists='replace', index=False) 
    df = pd.read_sql('dados', con=engine) 
    col1, col2 = st.columns(2)
    df_media = df.groupby('Dia')['Preco'].mean().reset_index()
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

    st.title("Análise Univariada dos Dados")
    with st.expander("Clique aqui para visualizar a análise univariada"):
        st.write("Aqui estão três análises gráficas realizadas com os dados fornecidos:")
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
df['Dia'] = df['Dia'].str.strip()
df['Dia'] = pd.to_datetime(df['Dia'], format='%d/%m')

with st.expander("Clique aqui para visualizar a análise multivariada"):
        st.write("Aqui estão os gráficos multivariados com os dados fornecidos:")

        fig5 = px.scatter(df, x="Partida_horario", y="Preco", title="Relação entre Preço e Hora de Partida", labels={"Partida_horario": "Hora de Partida", "Preco": "Preço"})
        st.plotly_chart(fig5)

        fig6 = px.box(df, x="Periodo", y="Preco", title="Distribuição dos Preços por Período", points="all", labels={"Periodo": "Período do Dia", "Preco": "Preço"})
        st.plotly_chart(fig6)

        fig7 = px.bar(df_media, x="Dia", y="Preco", 
                      title="Variação do Preço Médio por Dia",
                      labels={"Dia": "Data", "Preco": "Preço Médio"},
                      color="Dia",  
                      barmode="group")
        st.plotly_chart(fig7)


