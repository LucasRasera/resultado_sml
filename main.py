import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

st.title('Analise de Tabulações - Vendas Ativo')

de_para_cpc = pd.read_excel("DE-PARA CPC.xlsx")
uploaded_file = st.file_uploader("Arquivo de tabulações")

if uploaded_file is not None:
    # Aceita o arquivo enviado e mostra a tabela
    st.subheader('Base de tabulações', divider=True)
    tabulacoes = pd.read_csv(uploaded_file, sep=";")
    tabulacoes["OPERADOR"] = tabulacoes["OPERADOR"].str.title()
    tabulacoes = tabulacoes.drop(["DATA AGENDADA", "VALOR_VENDA", "VALOR", "ALO", "CPC", "CPCA", "VENDA"], axis=1)
    tabulacoes['NOME DO FILTRO'] = tabulacoes['NOME DO FILTRO'].str.split('CWB_').str[1]
    tabulacoes = pd.merge(tabulacoes, de_para_cpc, on="OCORRENCIA")
    st.write(tabulacoes)
    #-------------------------------------------

    #Criar a tabela com as principais ocorrencias e cria o grafico de barra
    max_length = 18
    top_ocorrencias = tabulacoes.groupby("OCORRENCIA").size().reset_index(name='TOTAL')
    top_ocorrencias['OCORRENCIA_short'] = top_ocorrencias['OCORRENCIA'].str.slice(0, max_length)

    total_ocorrencias = top_ocorrencias['TOTAL'].sum()
    top_ocorrencias['% IMPACTO'] = ((top_ocorrencias['TOTAL'] / total_ocorrencias) * 100).round(2)
    top_ocorrencias = top_ocorrencias.sort_values(by='TOTAL', ascending=False).head(10)

    st.subheader('Principais Tabulações', divider=True)
    graf_ocorrencias =px.bar(
        top_ocorrencias, 
        x="OCORRENCIA_short", 
        y="TOTAL",  
        text='TOTAL',
        labels={
            'TOTAL': 'Numero de ocorrencias',
            'OCORRENCIA_short': 'Ocorrencias'   
            },
        color_discrete_sequence=px.colors.qualitative.Plotly,
        title= "TOP 10 Tabulações"
        )
    graf_ocorrencias.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    graf_ocorrencias.update_yaxes(range=[0, top_ocorrencias['TOTAL'].max() * 1.2])
    graf_ocorrencias.update_yaxes(showticklabels=False)
    graf_ocorrencias.update_layout(xaxis_tickangle=-45)
    graf_ocorrencias.update_layout(xaxis=dict(tickfont=dict(size=10)))
    #-------------------------------------------------------------------


    #Criar um filtro para selecionar as tabulações e cria o grafico com os principais 
    st.plotly_chart(graf_ocorrencias, use_container_width=True)
    opcoes_tabulacoes = tabulacoes["OCORRENCIA"].unique()
    option = st.selectbox("Tabulações", opcoes_tabulacoes)

    n_tabuladas = tabulacoes.loc[tabulacoes['OCORRENCIA'] == option]
    n_tabuladas = n_tabuladas.groupby("OPERADOR").size().reset_index(name='TOTAL')
    n_tabuladas = n_tabuladas.sort_values(by='TOTAL', ascending=False)
    n_tabuladas['OPERADOR'] = n_tabuladas['OPERADOR'].str.slice(0, max_length)

    graf_n_tabuladas =px.bar(
        n_tabuladas, 
        x="OPERADOR", 
        y="TOTAL",  
        text='TOTAL',
        title= 'Operadores com mais recorencia na tabulação',
        labels={
            'TOTAL': 'Numero de ocorrencias',
            'OPERADOR': 'Operador'   
            },
        color_discrete_sequence=px.colors.qualitative.Plotly
        )
    graf_ocorrencias.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    graf_ocorrencias.update_yaxes(range=[0, top_ocorrencias['TOTAL'].max() * 1.5])
    graf_ocorrencias.update_yaxes(showticklabels=False)
    graf_ocorrencias.update_layout(xaxis_tickangle=-45)
    graf_ocorrencias.update_layout(xaxis=dict(tickfont=dict(size=10)))

    graf_n_tabuladas
    #------------------------------------------------------------------------


    st.subheader('CPC - Por Filtro / Operador', divider=True)
    option_cpc = st.selectbox("Selecione a visualização do CPC", ["NOME DO FILTRO", "OPERADOR"])
    cpc_filtro = tabulacoes.pivot_table(index=option_cpc, columns="CPC REAL", aggfunc='size', fill_value=0)
    
    cpc_filtro.columns = ["Não CPC", "CPC"]
    cpc_filtro.reset_index(inplace=True)
    cpc_filtro['% CPC'] = round((cpc_filtro["CPC"] / (cpc_filtro["Não CPC"] + cpc_filtro["CPC"])) * 100, 2)
    cpc_filtro = cpc_filtro.sort_values(by=['% CPC'], ascending=False)
    cpc_filtro[option_cpc] = cpc_filtro[option_cpc].str.slice(0, max_length)
    st.dataframe(cpc_filtro)

    graf_cpc_filtro =px.bar(
        cpc_filtro, 
        x= option_cpc, 
        y='CPC',  
        text='CPC',
        title= 'Quantidade de CPC',
        color_discrete_sequence=px.colors.qualitative.Plotly
        )
    graf_cpc_filtro.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    graf_cpc_filtro.update_yaxes(range=[0, cpc_filtro['CPC'].max() * 1.5])
    graf_cpc_filtro.update_yaxes(showticklabels=False)
    graf_cpc_filtro.update_layout(xaxis_tickangle=-45)
    graf_cpc_filtro.update_layout(xaxis=dict(tickfont=dict(size=10)))
    graf_cpc_filtro
    #-------------------------------------------------------------
    
    st.subheader('CPC por Filtro e Hora', divider=True)
    tabulacoes['HORA'] = tabulacoes['HORA'].str.split(':').str[0]
    tabela_pivot = tabulacoes.pivot_table(index="NOME DO FILTRO", columns="HORA", aggfunc='size', fill_value=0)
    tabela_pivot = tabela_pivot.reset_index()
    st.dataframe(tabela_pivot)

    #teste
    
        