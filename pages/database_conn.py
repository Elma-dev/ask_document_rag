import streamlit as st

st.header("Link Streamlit with db")
st.write("first of all we should to create a .toml and put all database configs on it.")

def connect_db():
    conn=st.connection("my_db_connection")
    data=conn.query("select * from data_rag_test")
    st.dataframe(data)
    st.write("connection established")

connect_db()