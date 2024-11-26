import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine 


st.title('Trabalho Web: Dados Gol')
engine = create_engine('sqlite:///banco.db', echo=True)
try:
    df_lido = pd.read_sql('SELECT * FROM dados', con=engine)
    st.write("Dados carregados com sucesso!")
    st.write("Colunas disponíveis:", df_lido.columns)
except Exception as e:
    df_lido = None
    st.error("Erro ao carregar os dados do banco de dados:")
    st.error(e)
if st.button('Tela inicial', type='primary', key="home"):
    st.write("Bem-vindo à análise dos dados da Gol!")
if st.button("Média, Mediana e Desvio Padrão", key="estatisticas"):
    if df_lido is not None:
        media = df_lido['Preco'].mean()
        mediana = df_lido['Preco'].median()
        dp = df_lido['Preco'].std()
        st.write("Dados carregados:", df_lido)
        estatisticas = pd.DataFrame({
            'Estatística': ['Média', 'Mediana', 'Desvio Padrão'],
            'Valor': [media, mediana, dp]
        })
        fig = px.bar(estatisticas, x='Estatística', y='Valor', text='Valor', title='Estatísticas de Preços')
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        st.plotly_chart(fig)
    else:
        st.error("Erro: Dados não carregados.")

if st.button("Análise Univariada dos Dados", key="univariada"):
    if df_lido is not None:
        if 'Dia' in df_lido.columns:
            voos = df_lido['Dia'].value_counts().reset_index()
            voos.columns = ['Dia', 'Quantidade']

            st.write("Distribuição de voos por período do dia:", voos)

            fig2 = px.pie(voos, names='Dia', values='Quantidade', title="Frequência de Voos por Período")
            st.plotly_chart(fig2)
        else:
            st.write("A coluna 'Dia' não foi encontrada no banco de dados. Verifique o nome da coluna.")
    else:
        st.error("Erro: Dados não carregados.")

if st.button('Análise Multivariada dos Dados', key="multivariada"):
    if df_lido is not None:
        if 'Partida_horario' in df_lido.columns and 'Preco' in df_lido.columns:
            v2 = df_lido[['Partida_horario', 'Preco']]

            st.write("Dados para análise multivariada:", v2)

            fig3 = px.bar(v2, x='Partida_horario', y='Preco', title='Relação entre Preço e Hora de Partida')
            st.plotly_chart(fig3)
        else:
            st.write("As colunas 'Partida_horario' ou 'Preco' não foram encontradas no banco de dados.")
    else:
        st.error("Erro: Dados não carregados.")

if df_lido is not None and 'Preco' in df_lido.columns:
    fig4 = px.box(df_lido, y="Preco", title="Boxplot dos Preços", points="all")
    st.plotly_chart(fig4)
else:
    st.error("A coluna 'Preco' não foi encontrada ou os dados não foram carregados.")
