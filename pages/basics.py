import streamlit as st

st.header("Basics Concepts")
st.write("From here we learn about basics of streamlit just by using form...")
accept = False
st.write("Fondamentals Streamlit")
form = st.form(key="user_form", clear_on_submit=True)
with form:
    name = st.text_input("username: ")
    rc, lc = st.columns(2)
    with lc:
        fname = st.text_input("first name:")
    with rc:
        lname = st.text_input("last name: ")
    email = st.text_input("email: ", placeholder="email@email.com")
    st.selectbox("background: ", ["Data Science", "Softwer Enginner", "DevOps"])
    passowrd = st.text_input("password", type="password")
    sex = st.radio("sex: ", ["male", "femal"], horizontal=True)
    accept = st.checkbox("Are you accept this inputs", key="accepted")
    submit = st.form_submit_button("submit", use_container_width=True)
