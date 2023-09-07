import PyPDF2
import re
from dotenv import load_dotenv
import pandas as pd
from langchain.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.document_loaders import GutenbergLoader
from langchain.vectorstores import Chroma
from langchain import LLMChain
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.agents import AgentExecutor, Tool, ZeroShotAgent
from langchain.memory import ConversationBufferMemory
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.llms import AzureOpenAI
import os
import pandas as pd
from langchain.agents import create_csv_agent

#COMBINACION DE CSVs
# ------------- CLEAR CUPS ----------------------------------------------------------------------------------------------------
# proced_df = pd.read_csv('./data/CUPS.csv')
# def quitar_ceros_izquierda(valor):    
#     return valor.lstrip('0')
# # Aplica la función a la columna
# proced_df['Codigo procedimiento'] = proced_df['Codigo procedimiento'].apply(quitar_ceros_izquierda)
# proced_df.to_csv('./CUPS.csv', index=False)
# # -------------MERGE CUPS -----------------------------------------------------------------------------------------------------

def cleanCsv():
    df1 = pd.read_csv('./data/AP.csv', low_memory=False)
    df1['Codigo procedimiento'] = df1['Codigo procedimiento'].astype(str)
    df2 = pd.read_csv('./data/CUPS.csv', low_memory=False)
    df2['Codigo procedimiento'] = df2['Codigo procedimiento'].astype(str)
    resultado_df = pd.merge(df1, df2, on='Codigo procedimiento', how='left')
    # ------------- MERGE DE CIE10 ----------------------------------------------------------------------------------------------------
    resultado_df['DX Principal'] = resultado_df['DX Principal'].astype(str)
    df2 = pd.read_csv('./data/CIE10.csv', low_memory=False)
    df2['DX Principal'] = df2['DX Principal'].astype(str)
    resultado_df = pd.merge(resultado_df, df2, on='DX Principal', how='left')
    # ------------- CLEAR COLUMNS ----------------------------------------------------------------------------------------------------
    #columnas = ['Factura','Codigo prestador','Tipo de documento','Numero de documento','Fecha Procedimiento','# Autorizacion','Ambito Procedimiento','Finalidad','Personal que atiende','Complicacion','Forma de realizacion','Valor procedimiento','Prestador','Tarifa','Cups no encontrados en NT PGP BOG','Valores AP no encontrados en NT PGP BOG','RIPS vs facturacion','RIPS AP facturados no encontrados en facturacion','Llave Factura y CC','CUPS AP PGP vs NT Ministerio','Alerta CUPS AP PGP vs NT Ministerio','CUPS OK','Valor NT Ministerio','Alerta prestadores']
    columnas = ['Factura','Codigo prestador','Fecha Procedimiento','# Autorizacion','Ambito Procedimiento','Finalidad','Personal que atiende','Complicacion','Forma de realizacion','Valor procedimiento','Prestador','Tarifa','Cups no encontrados en NT PGP BOG','Valores AP no encontrados en NT PGP BOG','RIPS vs facturacion','RIPS AP facturados no encontrados en facturacion','Llave Factura y CC','CUPS AP PGP vs NT Ministerio','Alerta CUPS AP PGP vs NT Ministerio','CUPS OK','Valor NT Ministerio','Alerta prestadores']
    RESULT_DF = resultado_df.drop(columnas, axis=1)
    RESULT_DF.to_csv('./data/RESULT.csv', index=False)

# ------------- CALL TO AGENT ----------------------------------------------------------------------------------------------------
def agentAudit():    
    with get_openai_callback() as cb:
        load_dotenv()
        agent = create_csv_agent(
            AzureOpenAI(openai_api_base="https://alph4num3r1c.openai.azure.com/",
                openai_api_version="2023-05-15",
                deployment_name="TestDavinci003",
                model="text-davinci-003",
                openai_api_key= os.environ["openai_api_key"],
                openai_api_type="azure",
                temperature=0
            ),
            ["./data/RESULT.csv"],
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )
        response = agent.run("Dime el número de identificación de los casos en los que el sexo del usuario sea F y el sexo apto sea M, "+
                             "también los casos donde el sexo del usuario sea M y el sexo apto sea F.")
        print(cb)
        return response
agentAudit()
# ------------------------------------------------------------------------------------------------------------------------------------------
 