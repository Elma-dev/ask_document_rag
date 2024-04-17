import streamlit as st

st.header("Advanceds Concepts")

def advancedConcepts():
    st.write("Advanced Concepts:")
    st.write("cache:")
    lc,rc=st.columns(2)
    with(lc):
        st.write("st.cache_data():")
        st.write("anything can store in data base")
        st.write("@st.cache_data")
    with(rc):
        st.write("st.cache_resource():")
        st.write("anything can't store in data base.")
        st.write("recommended way to cache global resources like ML models or database connections.")
        st.write("@st.cahe_data")
    st.image("images/img.png")
    st.write("session state:")
    st.write("""Session State provides a dictionary-like interface where you can save
     information that is preserved between script reruns""")
    st.write("st.session_state.my_key")
advancedConcepts()