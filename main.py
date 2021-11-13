import streamlit as st
import pandas as pd
import mysql.connector as connection
import matplotlib.pyplot as plt
import time

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

@st.cache(allow_output_mutation=True, hash_funcs=hash_funcs)
def get_data_geral():
    try:
        mydb = init_connection()
        #query = "Select * from Resumo order by DataCalendario limit 100"
        #query = "Select DataCalendario, ARIMA_Predict, prev_nivel from Predicao order by DataCalendario"
        query = "Select CAST(Predicao.`index` AS DATE) AS DataCalendario, prev_nivel AS `Nível previsto`, Volume AS `Volume real` from  Predicao left join Niveis on Niveis.`Data` = Predicao.`index` order by Predicao.`index`"
        

        result_dataFrame = pd.read_sql(query, mydb)
        mydb.close() 
        print("Consultou geral")
        return (result_dataFrame)
    except Exception as e:
        mydb.close()
        print(str(e))
        

get_data_geral()

def main():

    page = st.sidebar.selectbox(
        "Página",
        [
            "Homepage",
            "Previsão"
        ],
    )

    if page == "Homepage":
        #latest_iteration = st.empty()
        bar = st.progress(0)

        for i in range(100):
          #latest_iteration.text(f'Iteration {i+1}')
          bar.progress(i + 1)
          time.sleep(0.001)

        #'...and now we\'re done!'
            
        """
        # Previsão de níveis hidrológicos - Projeto Integrador Digital House
        A partir de dados de séries históricas de medições de vazões, chuvas e clima na bacia afluente à UHE Pedra do Cavalo (BA) prever o nível desse reservatório.
        Esta informação tem impacto no abastecimento da região metropolitana de Salvador.
        """
            
        st.header('Time')
        st.text('Alessandro Esequiel Moreira de Lima')
        st.text('Dan Scremin Lau')
        st.text('Daniela Ribeiro Bragança Silva')
        st.text('Emerson Massaiti Haro')
        st.text('Pedro Vitor Lima Cavalcante')
        st.text('Renata de Souza Silva')
        
    elif page == "Previsão":
        st.header("Previsão dos níveis do reservatório")
        graficoGeral()

#    elif page == "Chuvas":
#        horizontal_bar()

#    elif page == "Níveis":
#        graficoNiveis()

#    elif page == "Previsão":
#        st.header("Previsão")
#        histogram()


def filtrar_datas(df):
    df.DataCalendario = pd.to_datetime(df.DataCalendario)
    
    start_date_dataframe = df.DataCalendario[0]
    end_date_dataframe = df.DataCalendario[df.shape[0] - 1]
    
    start_date = st.sidebar.date_input('Dia inicial', start_date_dataframe, min_value=start_date_dataframe,
                                       max_value=end_date_dataframe)
    end_date = st.sidebar.date_input('Dia final', end_date_dataframe, min_value=start_date_dataframe,
                                     max_value=end_date_dataframe)
    
    st.sidebar.success('Data inicial: `%s`\n\nData final: `%s`' % (start_date, end_date))
    
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    
    df = df.set_index(['DataCalendario'])
    
    df = df.loc[start_date:end_date]
    
    return df

def graficoGeral():
    result = get_data_geral()
    st.line_chart(filtrar_datas(result))
    
    
def graficoNiveis():
    result = get_data_niveis()
    result_dataFrame = result.set_index('DataCalendario')
    st.line_chart(result_dataFrame)
    

  
if __name__ == "__main__":
    main()