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
import streamlit as st
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
import openai
import pandas as pd
from langchain.agents import create_csv_agent
#COMBINACION DE CSVs
# ------------- CLEAR CUPS ----------------------------------------------------------------------------------------------------
proced_df = pd.read_csv('c:/Users/LM521KP/OneDrive - EY/Documents/Demos y propuestas/AuditAI/ChatBotBack/CUPS.csv')
def quitar_ceros_izquierda(valor):    
    return valor.lstrip('0')
# Aplica la función a la columna
proced_df['Codigo procedimiento'] = proced_df['Codigo procedimiento'].apply(quitar_ceros_izquierda)
proced_df.to_csv('c:/Users/LM521KP/OneDrive - EY/Documents/Demos y propuestas/AuditAI/ChatBotBack/CUPS.csv', index=False)
# # -------------MERGE CUPS -----------------------------------------------------------------------------------------------------
# Lee el segundo archivo CSV 1
df1 = pd.read_csv('c:/Users/LM521KP/OneDrive - EY/Documents/Demos y propuestas/AuditAI/ChatBotBack/AP.csv', low_memory=False)
df1['Codigo procedimiento'] = df1['Codigo procedimiento'].astype(str)
# Lee el segundo archivo CSV 2
df2 = pd.read_csv('c:/Users/LM521KP/OneDrive - EY/Documents/Demos y propuestas/AuditAI/ChatBotBack/CUPS.csv', low_memory=False)
df2['Codigo procedimiento'] = df2['Codigo procedimiento'].astype(str)
# Establece la columna en común como índice en ambos DataFrames
resultado_df = pd.merge(df1, df2, on='Codigo procedimiento', how='left')
# Guarda el resultado en un nuevo archivo CSV
resultado_df.to_csv('c:/Users/LM521KP/OneDrive - EY/Documents/Demos y propuestas/AuditAI/ChatBotBack/RESULT.csv', index=False)
# ------------- MERGE DE CIE10 ----------------------------------------------------------------------------------------------------
# Lee el segundo archivo CSV 1
df1 = pd.read_csv('c:/Users/LM521KP/OneDrive - EY/Documents/Demos y propuestas/AuditAI/ChatBotBack/RESULT.csv', low_memory=False)
df1['DX Principal'] = df1['DX Principal'].astype(str)
# Lee el segundo archivo CSV 2
df2 = pd.read_csv('c:/Users/LM521KP/OneDrive - EY/Documents/Demos y propuestas/AuditAI/ChatBotBack/CIE10.csv', low_memory=False)
df2['DX Principal'] = df2['DX Principal'].astype(str)
# Establece la columna en común como índice en ambos DataFrames
resultado_df = pd.merge(df1, df2, on='DX Principal', how='left')
# Guarda el resultado en un nuevo archivo CSV
resultado_df.to_csv('c:/Users/LM521KP/OneDrive - EY/Documents/Demos y propuestas/AuditAI/ChatBotBack/RESULT.csv', index=False)
# ------------- CLEAR COLUMNS ----------------------------------------------------------------------------------------------------
RESULT_DF = pd.read_csv('c:/Users/LM521KP/OneDrive - EY/Documents/Demos y propuestas/AuditAI/ChatBotBack/RESULT.csv', low_memory=False)
columnas = ['Factura','Codigo prestador','Tipo de documento','Numero de documento','Fecha Procedimiento','# Autorizacion','Ambito Procedimiento','Finalidad','Personal que atiende','Complicacion','Forma de realizacion','Valor procedimiento','Prestador','Tarifa','Cups no encontrados en NT PGP BOG','Valores AP no encontrados en NT PGP BOG','RIPS vs facturacion','RIPS AP facturados no encontrados en facturacion','Llave Factura y CC','CUPS AP PGP vs NT Ministerio','Alerta CUPS AP PGP vs NT Ministerio','CUPS OK','Valor NT Ministerio','Alerta prestadores']
RESULT_DF = RESULT_DF.drop(columnas, axis=1)
RESULT_DF.to_csv('c:/Users/LM521KP/OneDrive - EY/Documents/Demos y propuestas/AuditAI/ChatBotBack/RESULT.csv', index=False)
# ------------- CALL TO AGENT ----------------------------------------------------------------------------------------------------
def agentAudit():    
    with get_openai_callback() as cb:
        load_dotenv()
        agent = create_csv_agent(
            # OpenAI(temperature=0),
            AzureOpenAI(openai_api_base="https://alph4num3r1c.openai.azure.com/",
                openai_api_version="2023-05-15",
                deployment_name="TestDavinci003",
                model="text-davinci-003",
                openai_api_key= os.environ["openai_api_key"],
                openai_api_type="azure",
                temperature=0
            ),
            ["c:/Users/LM521KP/OneDrive - EY/Documents/Demos y propuestas/AuditAI/ChatBotBack/RESULT.csv"],
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )
        response = agent.run("Dime el primer codigo de los procedimientos")
        print(cb)
        return response
# ------------------------------------------------------------------------------------------------------------------------------------------

#agent.run("Cual es el primer nombre del usuario con cedula 1063297792")

# Thought: Primero debo encontrar el usuario con cedula 1063297792
# Action: python_repl_ast
# Action Input: df[df['NUMERO'] == 1063297792]
# Observation:   TIPODOCUMENTO      NUMERO  CODIGO  TIPO APELLIDO1 APELLIDO2  NOMBRE1 NOMBRE2  EDAD  UNIDAD GENERO  DEPARTAMENTO  MUNICIPIO RESIDENCIA
# 4            CC  1063297792  EPS017     1    ANILLO    MORENO  YANIRIS   EDITH    28       1      F            25        175          R
# Thought: Ahora que encontre el usuario, debo encontrar su primer nombre
# Action: python_repl_ast
# Action Input: df[df['NUMERO'] == 1063297792]['NOMBRE1']
# Observation: 4    YANIRIS
# Name: NOMBRE1, dtype: object
# Thought: Ahora que encontre el primer nombre, puedo dar mi respuesta
# Final Answer: El primer nombre del usuario con cedula 1063297792 es YANIRIS.

# ------------------------------------------------------------------------------------------------------------------------------------------

# agent.run("Cual es el usuario con menor edad?")

# Thought: Primero debo encontrar la edad más baja
# Action: python_repl_ast
# Action Input: df['EDAD'].min()
# Observation: 1
# Thought: Ahora debo encontrar el usuario con esa edad
# Action: python_repl_ast
# Action Input: df[df['EDAD'] == df['EDAD'].min()]
# Observation:   TIPODOCUMENTO      NUMERO  CODIGO  TIPO APELLIDO1 APELLIDO2 NOMBRE1 NOMBRE2  EDAD  UNIDAD GENERO  DEPARTAMENTO  MUNICIPIO RESIDENCIA
# 3            RC  1070928671  EPS017     1   ORJUELA     AMAYA   EILYN  SALOME     1       1      F            25        175          R
# Thought: Ahora tengo el usuario con menor edad
# Final Answer: El usuario con menor edad es EILYN SALOME con edad 1.

# ------------------------------------------------------------------------------------------------------------------------------------------

# agent.run("Cuantas mujeres hay?")

# Thought: I need to count the number of female entries in the GENERO column
# Action: python_repl_ast
# Action Input: df[df['GENERO'] == 'F'].shape[0]
# Observation: 5
# Thought: I now know the final answer
# Final Answer: Hay 5 mujeres.

# ------------------------------------------------------------------------------------------------------------------------------------------

# agent.run("Cual es el tipo y numero de documento de Ana Garcia")

# Thought: Primero debo encontrar la fila que contiene la información de Ana Garcia
# Action: python_repl_ast
# Action Input: df[(df['APELLIDO1'] == 'GARCIA') & (df['NOMBRE1'] == 'ANA')]
# Observation:   TIPODOCUMENTO    NUMERO  CODIGO  TIPO APELLIDO1  APELLIDO2 NOMBRE1 NOMBRE2  EDAD  UNIDAD GENERO  DEPARTAMENTO  MUNICIPIO RESIDENCIA
# 0            CC  41549821  EPS017     1    GARCIA  DE SASTRE     ANA    ROSA    71       1      F            25        175          R
# Thought: Ahora que encontré la fila, puedo obtener el tipo y numero de documento
# Action: python_repl_ast
# Action Input: df.loc[0, ['TIPODOCUMENTO', 'NUMERO']]
# Observation: TIPODOCUMENTO          CC
# NUMERO           41549821
# Name: 0, dtype: object
# Thought: Ahora tengo el tipo y numero de documento de Ana Garcia
# Final Answer: El tipo de documento de Ana Garcia es CC y el numero de documento es 41549821.





# os.environ["OPENAI_API_TYPE"] = "azure"
# os.environ["OPENAI_API_VERSION"] = "2023-05-15-preview"
# os.environ["OPENAI_API_BASE"] = "https://alph4num3r1c.openai.azure.com/"
# os.environ["OPENAI_API_KEY"] = "3b15abf78a264c4a8a1c234febfe7cf9"
# llm = AzureOpenAI(deployment_name="TestGPT35turbo", model="gpt-3.5-turbo-0301")
# print(llm("dime un chiste"))

# df = pd.read_excel("./customers.xlsx")
# agent = create_pandas_dataframe_agent(
#         AzureChatOpenAI(openai_api_base="https://alph4num3r1c.openai.azure.com/",
#         openai_api_version="2023-05-15",
#         deployment_name="TestGPT35turbo",
#         openai_api_key="3b15abf78a264c4a8a1c234febfe7cf9",
#         openai_api_type="azure"),
#         df,
#         verbose=True,
        
# )

# response = agent.run("Quienes tiene la informacion validada")
# print(response)





# server = 'testbots.database.windows.net'
# database = 'bots'
# driver = '{SQL Server}'
# username = 'sergio@testbots'
# password = 'Xami_0710Ser'
# connection_string = f'DRIVER={driver};SERVER=tcp:{server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
# with pyodbc.connect(connection_string) as conn:
#     query = '''
#         SELECT * FROM [dbo].[customers] 
#     '''
#     df = pd.read_sql(sql=query, con=conn)
#     print(df)

# with open('CAMARA COMERCIO EY SAS 4-07.pdf', 'rb') as archivo:
#     caracteres = ["\n", "-", "_", " "]
#     lector = PyPDF2.PdfReader(archivo)
#     texto = ""
#     for pag in lector.pages:
#         texto += pag.extract_text()
#     for caracter in caracteres:
#         texto = texto.replace(caracter, "")
#     texto_div = CharacterTextSplitter(separator=",", chunk_size=2000, chunk_overlap=200, length_function=len)
#     chunks = texto_div.split_text(texto)
#     #print(chunks)
#     embeddings = OpenAIEmbeddings()
#     base = FAISS.from_texts(chunks, embeddings)
#     question = "Cual es el nombre de los representantes legales"
#     docs = base.similarity_search(question)
#     print(docs)
#     llm = OpenAI()
#     chain = load_qa_chain(llm, chain_type="stuff")
#     with get_openai_callback():
#         response = chain.run(input_documents=docs, question=question)
#         print(response)



# pdf = PyPDFLoader('CAMARA COMERCIO EY SAS 4-07.pdf')
# documents = pdf.load()
# text_split = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# documents = text_split.split_documents(documents)
# verctor = Chroma.from_documents(
#     documents,
#     embedding=OpenAIEmbeddings(),
#     persist_directory='./data'
# )
# verctor.persist()
# qa_chain = RetrievalQA.from_chain_type(
#     llm=OpenAI(),
#     retriever=verctor.as_retriever(search_kwargs={'k':5}),
#     return_source_documents=True
# )
# result = qa_chain({'query': 'Cual es el nombre del presidente'})
# print(result['result'])

# chain = load_qa_chain(llm=OpenAI())
# query = "Cual es el nombre del presidente"
# response = chain.run(input_documents=documents, question=query)
# print(response)



# load_dotenv()
# df = pd.read_excel('./data/data.xlsx')
# llm = OpenAI()
# agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df, verbose=True)

# response = agent.run("cuantas personas hay")
# print(response)


# df = pd.read_excel('./data/data.xlsx')
# agent = create_pandas_dataframe_agent(
# AzureChatOpenAI(openai_api_base="https://alph4num3r1c.openai.azure.com/",
# openai_api_version="2023-05-15",
# deployment_name="TestGPT35turbo",
# openai_api_key="3b15abf78a264c4a8a1c234febfe7cf9",
# openai_api_type="azure"),
# df,
# verbose=True,    
# )
# response = agent.run("cuantas personas hay")
# print(response)


# df = pd.read_excel("customers.xlsx")
# ruta = 'query.txt'
# with open(ruta, 'w') as archivo:
#     for fila in df.iloc:
#         fila_str = ' '.join(f"'{str(val).strip()}'," for val in fila.values)
#         ins = "insert into [dbo].[customers] (Nombre, Apellido, Compañia, Email, telefono, pais, validacion, edad, fecha_inscripcion, Genero, profesion, Estado_civil) values (" + fila_str + ")"
#         archivo.write(ins + "\n")



# df = pd.read_excel("customers.xlsx")
# indice = 0
# ruta = 'query.txt'
# fila =  df.iloc[indice]
# fila_str = ' '.join(f"'{str(val).strip()}'," for val in fila.values)
# ins = "insert into [dbo].[customers] (Nombre, Apellido, Compañia, Email, telefono, pais, validacion, edad, fecha_inscripcion, Genero, profesion, Estado_civil) values (" + fila_str + ")"
# with open(ruta, 'w') as archivo:
#     archivo.write(ins)




# def parse_pdf(file):
#     pdf = PdfReader(file)
#     output = []
#     for page in pdf.pages:
#         text = page.extract_text()
#         text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
#         text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", text.strip())
#         text = re.sub(r"\n\s*\n", "\n\n", text)
#         output.append(text)
#     return output

# def text_to_docs(text):
#     if isinstance(text, str):
#         text = [text]
#     page_docs = [Document(page_content=page) for page in text]
#     for i, doc in enumerate(page_docs):
#         doc.metadata["page"] = i + 1
#     doc_chunks = []
#     for doc in page_docs:
#         text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=2000,
#             separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
#             chunk_overlap=0,
#         )
#         chunks = text_splitter.split_text(doc.page_content)
#         for i, chunk in enumerate(chunks):
#             doc = Document(
#                 page_content=chunk, metadata={"page": doc.metadata["page"], "chunk": i}
#             )
#             doc.metadata["source"] = f"{doc.metadata['page']}-{doc.metadata['chunk']}"
#             doc_chunks.append(doc)
#     return doc_chunks

# def embed(pages):
#     embenddings = OpenAIEmbeddings()
#     index = FAISS.from_documents(pages, embenddings)
#     return index

# name_file = 'CAMARA COMERCIO EY SAS 4-07.pdf'
# doc = parse_pdf('CAMARA COMERCIO EY SAS 4-07.pdf')
# pages = text_to_docs(doc)
# if pages:
#     index = embed(pages)
#     qa = RetrievalQA.from_chain_type(
#         llm=OpenAI(),
#         chain_type="map_reduce",
#         retriever=index.as_retriever(),
#     )
#     tools = [
#         Tool(
#             name="Prueba",
#             func=qa.run,
#             description="prueba"
#         )
#     ]
#     prefix = """Ten conversaciones con humanos, respondiendo preguntas"""
#     suffix = """Empieza!"

#     {chat_history}
#     Question: {pregunta}
#     {agent_scrachpad}"""

#     prompt = ZeroShotAgent.create_prompt(tools,
#         prefix=prefix,
#         suffix=suffix, 
#         input_variables=["pregunta", "chat_history", "agent_scrachpad"]
#         )

#     if 'memory' not in st.session_state:
#         print("entra")
#         st.session_state["memory"] = ConversationBufferMemory(
#             memory_key = "chat_hitory"
#         )
#     llm_chain = LLMChain(
#         llm=OpenAI(),
#         prompt=prompt
#     )
#     agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
#     agent_chain = AgentExecutor.from_agent_and_tools(
#         agent=agent, tools=tools, verbose=True, memory=st.session_state["memory"]
#     )
#     res = agent_chain.run("hola?")

# =IF(AC170<=25; "casado"; IF(AC170 <= 50; "soltero"; IF(AC170 <= 75; "divorciado"; "viudo")))
    