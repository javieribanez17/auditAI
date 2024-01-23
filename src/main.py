from dotenv import load_dotenv
import os
import pandas as pd
# from langchain.llms import AzureOpenAI
from langchain.agents.agent_types import AgentType
#from langchain.agents import create_csv_agent
from langchain_experimental.agents.agent_toolkits import create_csv_agent, create_pandas_dataframe_agent
from langchain_community.callbacks import get_openai_callback
from langchain_openai import AzureOpenAI, OpenAI
#from langchain.llms import OpenAI

load_dotenv()
# model = AzureOpenAI(
#     openai_api_base=os.environ["openai_api_base"],
#     openai_api_version="2023-05-15",
#     deployment_name="TestDavinci003",
#     model="text-davinci-003",
#     openai_api_key= os.environ["openai_api_key"],
#     openai_api_type="azure",
#     temperature=0
# )

#COMBINACION DE CSVs
# ------------- QUITAR CEROS A CUPS ----------------------------------------------------------------------------------------------------

def cleanCsv():
    # ------------- AGREGAR COLUMNAS A LOS ARCHIVOS ----------------------------------------------------------------------------------------------------
    # Agregar columnas a CIE10
    dff = pd.read_csv('./data/CIE10.csv', low_memory=False, header=None)
    dff.columns = ['Codigo del diagnostico', 'Nombre del diagnostico','Sexo del diagnostico']
    dff.to_csv('./data/CIE10.csv', index=False)
    # Agregar columnas a CUPS
    dff = pd.read_csv('./data/CUPS.csv', low_memory=False, header=None)
    dff.columns = ['Codigo del procedimiento', 'Nombre del procedimiento', 'Sexo del procedimiento']
    dff.to_csv('./data/CUPS.csv', index=False)
    # Agregar columnas a AP
    dff = pd.read_csv('./data/AP.csv', low_memory=False, header=None)
    dff.columns = ['Factura','Codigo prestador','Tipo de documento','Numero de identificacion','Fecha Procedimiento','# Autorizacion','Codigo del procedimiento','Ambito Procedimiento','Finalidad','Personal que atiende','Codigo del diagnostico','DX Relacionado','Complicacion','Forma de realizacion','Valor procedimiento']
    dff.to_csv('./data/AP.csv', index=False)
    # Agregar columnas a AC
    dff = pd.read_csv('./data/US.csv', low_memory=False, header=None)
    dff.columns = ['Tipo de doc','Numero de identificacion','Codigo entidad','Tipo de usuario','Apellido','Apellido 2','Nombre','Nombre 2','Edad','Unidad de medida','Sexo del usuario','Departamento','Municipio','Zona']
    dff.to_csv('./data/US.csv', index=False)
    # ------------- MERGE DE AP y US ----------------------------------------------------------------------------------------------------
    df1 = pd.read_csv('./data/US.csv', low_memory=False)
    df1['Numero de identificacion'] = df1['Numero de identificacion'].astype(str)
    df2 = pd.read_csv('./data/AP.csv', low_memory=False)
    df2['Numero de identificacion'] = df2['Numero de identificacion'].astype(str)
    resultado_df = pd.merge(df1, df2, on='Numero de identificacion', how='left')
    columnas = ['Tipo de doc','Codigo entidad','Tipo de usuario','Apellido 2','Nombre 2','Edad','Unidad de medida','Departamento','Municipio','Zona','Factura','Codigo prestador','Tipo de documento','Fecha Procedimiento','# Autorizacion','Ambito Procedimiento','Finalidad','Personal que atiende','DX Relacionado','Complicacion','Forma de realizacion','Valor procedimiento']
    # ------------- MERGE DE CUPS ----------------------------------------------------------------------------------------------------
    resultado_df['Codigo del procedimiento'] = resultado_df['Codigo del procedimiento'].astype(str)
    df2 = pd.read_csv('./data/CUPS.csv', low_memory=False)
    df2['Codigo del procedimiento'] = df2['Codigo del procedimiento'].astype(str)
    resultado_df = pd.merge(resultado_df, df2, on='Codigo del procedimiento', how='left')
    # ------------- MERGE DE CIE10 ----------------------------------------------------------------------------------------------------
    resultado_df['Codigo del diagnostico'] = resultado_df['Codigo del diagnostico'].astype(str)
    df2 = pd.read_csv('./data/CIE10.csv', low_memory=False)
    df2['Codigo del diagnostico'] = df2['Codigo del diagnostico'].astype(str)
    resultado_df = pd.merge(resultado_df, df2, on='Codigo del diagnostico', how='left')
    # ------------- MERGE DE Tarifarios ----------------------------------------------------------------------------------------------------
    resultado_df['Codigo del procedimiento'] = resultado_df['Codigo del procedimiento'].astype(str)
    df2 = pd.read_csv('./data/TarifarioContrato.csv', low_memory=False)
    df2['Codigo del procedimiento'] = df2['Codigo del procedimiento'].astype(str)
    resultado_df = pd.merge(resultado_df, df2, on='Codigo del procedimiento', how='left')
    resultado_df['Codigo del procedimiento'] = resultado_df['Codigo del procedimiento'].astype(str)
    df2 = pd.read_csv('./data/TarifarioMinisterio.csv', low_memory=False)
    df2['Codigo del procedimiento'] = df2['Codigo del procedimiento'].astype(str)
    resultado_df = pd.merge(resultado_df, df2, on='Codigo del procedimiento', how='left')
    # # ------------- CLEAR COLUMNS ----------------------------------------------------------------------------------------------------
    RESULT_DF = resultado_df.drop(columnas, axis=1)
    column = "Sexo del procedimiento"
    gen = 'Z'
    RESULT_DF['Sexo del procedimiento'] = RESULT_DF.apply(changeGen, args=(column, gen), axis=1)
    column = 'Sexo del diagnostico'
    gen = 'A'
    RESULT_DF['Sexo del diagnostico'] = RESULT_DF.apply(changeGen, args=(column, gen), axis=1)
    RESULT_DF.to_csv('./data/RESULT.csv', index=False)
    
# ------------- CALL TO AGENT ----------------------------------------------------------------------------------------------------

def changeGen(row, column, gen):
    if row[column] == gen:
        return row['Sexo del usuario']
    else:
        return row[column]
    

def agentAudit(question):  
    df = pd.read_csv('./data/RESULT.csv')
    with get_openai_callback() as cb:
        load_dotenv()
        agent = create_pandas_dataframe_agent(
            OpenAI(temperature=0, 
                   openai_api_key=os.environ["OPENAI_API_KEY"]),
            # AzureOpenAI (
            #     openai_api_base=os.environ["openai_api_base"],
            #     openai_api_version="2023-05-15",
            #     deployment_name="TestDavinci003",
            #     model="text-davinci-003",
            #     openai_api_key= os.environ["openai_api_key"],
            #     openai_api_type="azure",
            #     temperature=0
            # ),
                df=df,
                verbose=True,
                agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                max_iterations = 7,
        )
        responseAgent = agent.invoke(question+'Debes traducir a español tu "Final Answer"')
        # response = gptModel(responseAgent, question).strip('.\n')
        print(cb)
        print(responseAgent)
        return responseAgent['output']