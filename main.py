import streamlit as st
import pandas as pd
import mysql.connector as connection
import matplotlib.pyplot as plt

header = st.container()
modelo = st.container()

hash_funcs={'_thread.RLock' : lambda _: None, 
                '_thread.lock' : lambda _: None, 
                'builtins.PyCapsule': lambda _: None, 
                '_io.TextIOWrapper' : lambda _: None, 
                'builtins.weakref': lambda _: None,
                'builtins.dict' : lambda _:None}

@st.cache(allow_output_mutation=True, hash_funcs=hash_funcs)
def init_connection():
    return connection.connect(**st.secrets["mysql"])

result_dataFrame = pd.DataFrame()

try:
    mydb = init_connection()
    query = "Select * from Resumo order by DataCalendario"
    result_dataFrame = pd.read_sql(query, mydb)
    mydb.close() #close the connection
    print("Consultou")
except Exception as e:
    mydb.close()
    print(str(e))

#conn = init_connection()

# Perform query.
# Uses st.cache to only rerun when the query changes or after 10 min.
#@st.cache(ttl=600)
#def run_query(query):
    #with conn.cursor() as cur:
     #   cur.execute(query)
      #  return cur.fetchall()

#query = "select ChuvasDiario.`Data`, ChuvasValue, Niveis.Volume, ifnull((SELECT SUM(Vazoes.Media) FROM Vazoes WHERE `Data`=Niveis.`Data`), 0) as SumVazaoMedia from ChuvasDiario left join Niveis on Niveis.`Data` = ChuvasDiario.`Data` where ChuvasDiario.Data>='2008-01-01';"

#a = run_query("select ChuvasDiario.`Data`, ChuvasValue, Niveis.Volume, ifnull((SELECT SUM(Vazoes.Media) FROM Vazoes WHERE `Data`=Niveis.`Data`), 0) as SumVazaoMedia from ChuvasDiario left join Niveis on Niveis.`Data` = ChuvasDiario.`Data` where ChuvasDiario.Data>='2008-01-01' limit 10;")

#df = pd.read_sql_query(query, conn)

# Caso a ideia seja consultar o csv diretamente
@st.cache
def get_data():
    dados = pd.read_csv('')
    return dados

def grafico():
    # multiple line plots
    #plt.figure(figsize=(20,8))
    #plt.plot( 'Data', 'ChuvasValue', data=result_dataFrame, markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
    #plt.plot( 'Data', 'Volume', data=result_dataFrame, color='red', linewidth=2)
    #plt.plot( 'Data', 'SumVazaoMedia', data=result_dataFrame, color='olive', linewidth=2, linestyle='dashed', label="Vazao")

    # show legend
    #plt.legend()

    # show graph
    #plt.show()

    st.line_chart(result_dataFrame)

with header:
    st.title('Previsão de níveis hidrológicos - Projeto Integrador Digital House')
    st.header('Descrição')
    st.text('A partir de dados de séries históricas de medições de vazões, chuvas e clima na bacia afluente à UHE Pedra do Cavalo (BA) prever o nível desse reservatório. Esta informação tem impacto no abastecimento da região metropolitana de Salvador.')
    st.header('Time')
    st.text('Alessandro Esequiel Moreira de Lima')
    st.text('Dan Scremi Lau')
    st.text('Daniela Ribeiro Bragança Silva')
    st.text('Emerson Massaiti Haro')
    st.text('Pedro Vitor Lima Cavalcante')
    st.text('Renata de Souza Silva')


with modelo:
    #sel_col, disp_col = st.columns(2)

    #max_depth = sel_col.slider('asfasdfsa?', min_value=10, max_value=20, value=14, step=2)

    #n_estimators = sel_col.selectbox('sadasdf?', options=[10, 20, 30, 40], index=0)

    #input_feature = sel_col.text_input('asdfasfs')
    result_dataFrame = result_dataFrame.set_index('DataCalendario')
    st.write(grafico())