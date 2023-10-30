import sqlite3
import pandas as pd

import streamlit as st
from streamlit_chat import message

from langchain import OpenAI, SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate
from langchain.agents import ZeroShotAgent
from langchain.agents import AgentExecutor


# from scripts.sql_connector import convert_df_to_sql, read_sql_query
import mysql.connector   #using
from sqlalchemy.dialects.mysql import mysqlconnector
import psycopg2
from sqlalchemy import create_engine, MetaData, select, Table,text
# from sqlalchemy import text

from dotenv import load_dotenv
import dotenv
# import pyodbc

key = st.secrets['key']


def sql_table(input,input_db):

    from langchain.chat_models import ChatOpenAI
    from langchain.chains import create_sql_query_chain
    llm = OpenAI(temperature=0,openai_api_key = key)
    # prom = """
    #     safety stock = max value * max val delay - avg val * avg val delay
    # """
    chain = create_sql_query_chain(llm, input_db)

    response = chain.invoke({"question":input})

    return response





def main():
    load_dotenv()

    with st.sidebar:
        db_type = st.radio("Select Database Type", ["MySQL", "PostgreSQL"])
        db_host = st.text_input("Enter Database Host", placeholder="Enter Database Host")
        db_port = st.text_input("Enter Database Port", placeholder="Enter Database Port", 
                                help="Default port is 5432 for PostgreSQL and 3306 for MySQL")
        db_name = st.text_input("Enter Database Name", placeholder="Enter Database Name")
        db_user = st.text_input("Enter Database User", placeholder="Enter Database User")
        db_password = st.text_input("Enter Database Password", "", type="password")
        connect_button = st.button("Connect")

        
        if db_type == "MySQL":
            #sql_uri = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            # sql_uri = f"mysql+mysqlconnector://root:localadmin@localhost:3306/classicmodels"
            sql_uri = "mysql+mysqlconnector://yusuf121:Satwik121@sqldatabase.mysql.database.azure.com:3306/chatbotdb"

        elif db_type == "PostgreSQL":
            sql_uri = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        
    try:
        if connect_button:
            input_db = SQLDatabase.from_uri(sql_uri)
            st.session_state.input_db = input_db
            st.sidebar.success("Connected")
            
            # connection = engine.connect()
            # engine = create_engine(sql_uri)

            
            # metadata = MetaData()
            # metadata.reflect(bind=engine)
            # list_of_tables = list(metadata.tables.keys())
            # m = 1
            st.success("You can start your exploration now!")
    except:
        st.error("Invalid Database Credentials")
        
    # from sqlalchemy import create_engine, MetaData, select, Table,text    
    try:
        if st.sidebar.checkbox("Data Preview"):
            engine = create_engine(sql_uri)

            metadata = MetaData()
            metadata.reflect(bind=engine)

            list_of_tables = list(metadata.tables.keys())

            with st.container():
                col1, col2 = st.columns([0.4, 0.9])
                with col1:
                    st.image('db.png', width=300)
                    #st.image('./data/2.png', width=300)
                with col2:
                    st.markdown("""
                        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 35vh;">
                            <h1>  DataBase  Query </h1>
                            <!-- Additional content goes here -->
                        </div>
                    """, unsafe_allow_html=True)


            selected_table_name = st.sidebar.selectbox("Select table", list_of_tables)
            table = Table(selected_table_name, metadata, autoload_with=engine)

            
            connection = engine.connect()
            result = connection.execute(table.select())
            rows = result.fetchall()

            st.write("Selected Table:", selected_table_name)
            df = pd.DataFrame(rows, columns=table.columns.keys())
            select_num_records = st.number_input("Select Number of Records :", min_value=5, max_value=len(df), value=5, step=5)
            st.dataframe(df.head(select_num_records))  # Displaying only the top 5 rows
            st.divider()

    except:
        st.warning("Select Tables from Sidebar")

    # response = df_agent_response(df)
    # st.write(response)
    
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(
            memory_key="chat_history"
        )

    # Check and initialize other session state variables
    if 'user_input' not in st.session_state:
        st.session_state.user_input = None
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [
            {'role': 'system', 'content': 'You are a helpful ChatBot!'}
        ]

    # Create containers
    response_container = st.container()
    container = st.container()

    # Chat input form
    with container:
        with st.form(key='my_form', clear_on_submit=True):
            st.session_state.user_input = st.text_area(label='You', key='input', height=20)
            submit_button = st.form_submit_button(label='Send')
            # prompt = propmt_template()

    # Reset conversation button
    reset_button = st.button("Start New Conversation")
    if reset_button:
        st.session_state['generated'] = []
        st.session_state['past'] = []

    # Process user input
    if submit_button and st.session_state.user_input:

        input_db = st.session_state.get('input_db', None)
        # st.write(input_db)


        # query = sql_table(user_input, input_db)
        # st.write(query)

        # engine = create_engine(sql_uri)
        # connection = engine.connect()
        # output = pd.read_sql(query, connection)
        # st.write(output)

        # Method - 2
        conn = mysql.connector.connect(user='yusuf121', password='Satwik121', host='sqldatabase.mysql.database.azure.com', port=3306, database='chatbotdb')
        cursor = conn.cursor()

        # Define your SQL query
        query = sql_table(st.session_state.user_input, input_db)
        # sql_query = "SELECT * FROM receipt "
        st.write(query)


        # Execute the query
        cursor.execute(query)

        # Fetch the results, if needed
        results = cursor.fetchall()
        # Convert the results to a Pandas DataFrame
        df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])

        # st.write(type(results))
        st.write(df)

        
        # print(output)
        # connection.close()
        
        

        st.session_state['past'].append(st.session_state.user_input)
        # st.session_state['generated'].append(output)

        # Display conversation
        if st.session_state['generated']:
            with response_container:
                for i in range(len(st.session_state['generated'])):
                    # Display user message
                    message(st.session_state['past'][i], is_user=True, key=str(i) + '_user1')

                    # Display bot message
                    # message(st.session_state['generated'][i], key=str(i))
                
        

    
