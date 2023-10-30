
from sat.app import *
from sat.dp_inv import *
from sat.dp_rcpt import *
from sat.dp_pdf import *
# from htmlTemplates import css, bot_template, user_template

import numpy as np
from streamlit_option_menu import option_menu
import streamlit as st

if __name__ == '__main__':

    st.set_page_config(page_title="sqlchatbot", layout="wide", page_icon=":robot_face:")

    with st.sidebar:
        options = option_menu(
            menu_title=None,
            options=["Home", "Chatbot","Invoice","Reciept","Miner"],
            icons=["🏠", "💬","🏠","🏠","🏠"],
            )

    if options == "Home":
        with st.container():
            col1, col2 = st.columns([0.2, 0.9])
            with col1:
                st.image('./data/1.png', width=300)
                #st.image('./data/2.png', width=300)
            with col2:
                st.markdown("""
                    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 35vh;">
                        <h1> Welcome To DataBase  Chatbot!</h1>
                        <!-- Additional content goes here -->
                    </div>
                """, unsafe_allow_html=True)

        
        with st.container():
            col1, col2 = st.columns([0.05, 0.95])
            with col2:
                # st.write("Interact with databases using natural language!")

                # Description
                st.markdown(
                    """
                    This application allows you to interact with databases
                    using natural languages and get results in a conversational manner.
                    """
                )

                # Image or illustration (optional)
                # st.image("path_to_image_or_url", caption="SQL Chatbot", use_column_width=True)

                # Features section
                st.markdown("#### Key Features")
                st.markdown(
                    """
                    - **Natural Language Interface:** Communicate with your database using plain English.
                    - **SQL Query Execution:** Execute SQL queries seamlessly.
                    - **Interactive Responses:** Get interactive and insightful responses from the chatbot.
                    - **User-Friendly Interface:** Enjoy a simple and intuitive user interface.
                    """
                )

                # Get Started section
                st.markdown("### Get Started")
                st.markdown(
                    """
                    1. Connect to your database by providing the necessary credentials.
                    2. Start a conversation by typing your queries related to Database.
                    3. Explore and analyze the results in real-time.
                    """
                )


                # About Us section (optional)
                st.markdown("#### About Us")
                st.markdown(
                    """
                    This SQL Chatbot App is developed by [celebaltech.com](https://www.celebaltech.com/).
                    We aim to simplify database interactions and make data exploration more accessible.
                    """
                )






    elif options == "Chatbot":
        main()

    elif options == "Invoice":
        app()

    elif options == "Reciept":
        rcpt1()

    elif options == "Miner":
        pdf()
        


