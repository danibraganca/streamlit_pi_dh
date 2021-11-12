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
        query = "Select DataCalendario, prev_nivel, Volume from Predicao left join Niveis on CAST(Niveis.Data AS DATE) = Predicao.DataCalendario order by Predicao.DataCalendario"
        #, ARIMA_Predict

        result_dataFrame = pd.read_sql(query, mydb)
        mydb.close() 
        print("Consultou geral")
        return (result_dataFrame)
    except Exception as e:
        mydb.close()
        print(str(e))
        
        
@st.cache(allow_output_mutation=True, hash_funcs=hash_funcs)
def get_data_chuvas():
    try:
        mydb = init_connection()
        query = "Select * from ChuvasDiario order by DataCalendario limit 100"
        result_dataFrame = pd.read_sql(query, mydb)
        mydb.close() 
        print("Consultou chuvas")
        return (result_dataFrame)
    except Exception as e:
        mydb.close()
        print(str(e))


@st.cache(allow_output_mutation=True, hash_funcs=hash_funcs)
def get_data_niveis():
    try:
        mydb = init_connection()
        query = "SELECT CAST(Data AS DATE) AS DataCalendario, Volume from Niveis where WEEKDAY(Data) = 6 order by Data;"
        result_dataFrame = pd.read_sql(query, mydb)
        mydb.close() 
        print("Consultou níveis")
        return (result_dataFrame)
    except Exception as e:
        mydb.close()
        print(str(e))


get_data_geral()
get_data_niveis()
get_data_chuvas()

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


def main():

    page = st.sidebar.selectbox(
        "Select a Page",
        [
            "Homepage",
            "Resumo variáveis",
            "Chuvas",
            "Níveis",
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
            
        #st.header('Time')
        #st.text('Alessandro Esequiel Moreira de Lima')
        #st.text('Dan Scremin Lau')
        #st.text('Daniela Ribeiro Bragança Silva')
        #st.text('Emerson Massaiti Haro')
        #st.text('Pedro Vitor Lima Cavalcante')
        #st.text('Renata de Souza Silva')
        
    elif page == "Resumo variáveis":
        graficoGeral()

    elif page == "Chuvas":
        horizontal_bar()

    elif page == "Níveis":
        graficoNiveis()

    elif page == "Previsão":
        st.header("Previsão")
        histogram()


def filtrar_datas(df):
    # Transformamos a coluna date, que anteriormente era texto para formato datetime
    df.DataCalendario = pd.to_datetime(df.DataCalendario)
    
    # Atribuimos a essas variáveis o dia inicial e final do dataframe completo
    start_date_dataframe = df.DataCalendario[0]
    end_date_dataframe = df.DataCalendario[df.shape[0] - 1]
    
    # Atribuimos a essas variáveis o filtro de data, passando como parâmetros
    # nome do campo, data selecionada ao clicar pela primeira vez, valores mínimos e máximos permitidos
    start_date = st.sidebar.date_input('Dia inicial', start_date_dataframe, min_value=start_date_dataframe,
                                       max_value=end_date_dataframe)
    end_date = st.sidebar.date_input('Dia final', end_date_dataframe, min_value=start_date_dataframe,
                                     max_value=end_date_dataframe)
    
    # Exibimos um aviso exibindo a data inicial e final selecionadas
    st.sidebar.success('Data inicial: `%s`\n\nData final: `%s`' % (start_date, end_date))
    
    # Convertemos as datas para o formato YYYY-MM-DD
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    
    # Transformamos o index do dataframe para as datas, visto que somente possuímos uma entrada por dia
    # e também para realizarmos o filtro no comando a seguir
    df = df.set_index(['DataCalendario'])
    
    # Realizamos um filtro com o comando loc passando a data inicial e final selecionadas anteriormente
    # nos filtros, e passamos o dataframe filtrado para a variável df
    df = df.loc[start_date:end_date]
    
    # Retornamos o método com a variável df modificada pelo filtro
    return df

def graficoGeral():
    # multiple line plots
    #plt.figure(figsize=(20,8))
    #plt.plot( 'Data', 'ChuvasValue', data=result_dataFrame, markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
    #plt.plot( 'Data', 'Volume', data=result_dataFrame, color='red', linewidth=2)
    #plt.plot( 'Data', 'SumVazaoMedia', data=result_dataFrame, color='olive', linewidth=2, linestyle='dashed', label="Vazao")

    # show legend
    #plt.legend()

    # show graph
    #plt.show()
    result = get_data_geral()
    st.line_chart(filtrar_datas(result))
    
    
def graficoNiveis():
    # multiple line plots
    #plt.figure(figsize=(20,8))
    #plt.plot( 'Data', 'ChuvasValue', data=result_dataFrame, markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
    #plt.plot( 'Data', 'Volume', data=result_dataFrame, color='red', linewidth=2)
    #plt.plot( 'Data', 'SumVazaoMedia', data=result_dataFrame, color='olive', linewidth=2, linestyle='dashed', label="Vazao")

    # show legend
    #plt.legend()

    # show graph
    #plt.show()
    result = get_data_niveis()
    result_dataFrame = result.set_index('DataCalendario')
    st.line_chart(result_dataFrame)
    
    
def bar_chart():
    fig = plt.figure(figsize=(12, 5))
    plt.xticks(rotation=80)
    bar_data = df.sort_values(by="views", ascending=False)
    bar_data = bar_data.head(20)
    plt.ticklabel_format(style="plain")
    plt.bar(bar_data["event"], bar_data["views"])
    plt.xlabel("Event")
    plt.ylabel("Views")
    plt.title("Event and Views Plot")
    st.pyplot(fig)


def horizontal_bar():
    fig = plt.figure(figsize=(12, 5))
    plt.xticks(rotation=80)
    bar_data = df.sort_values(by="views", ascending=False)
    bar_data = bar_data.head(20)
    plt.ticklabel_format(style="plain")
    plt.barh(bar_data["event"], bar_data["views"])
    plt.xlabel("Event")
    plt.ylabel("Views")
    plt.title("Event and Views Plot")
    st.pyplot(fig)


def visualize_scatter():
    fig = plt.figure(figsize=(10, 8))
    plt.scatter(
        x=df["comments"],
        y=df["views"],
        marker="*",
        s=df["languages"],
        c=df["languages"],
        alpha=0.5,
    )
    st.pyplot(fig)


def histogram():
    fig = plt.figure(figsize=(12, 5))
    plt.hist(df["languages"], color="y", bins=50)
    st.pyplot(fig)


def pie_chart():
    days_data = (
        df.groupby("published_day")["views"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig = plt.figure(figsize=(10, 8))
    explode = (0.1, 0, 0, 0, 0, 0, 0)
    plt.pie(
        days_data["views"],
        labels=days_data["published_day"],
        shadow=True,
        explode=explode,
        autopct="%1.1f%%",
    )
    st.pyplot(fig)


  
if __name__ == "__main__":
    main()