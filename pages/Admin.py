import streamlit as st 
import streamlit_authenticator as stauth
import numpy as np
from pymongo import MongoClient
from pathlib import Path
import pickle

def getData():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.AttendanceSystem
    names = ["dinesh","kumar"]
    usernames = ["dinesh13","kumar13"]
    file_path =  Path(__file__).parent / "hashed_pwd.pkl"
    with file_path.open("rb") as file:
        hashed_passwords = pickle.load(file)
    authenticator =stauth.Authenticate(names,usernames,hashed_passwords,"new_page","abcdef")
    name,authetication_status,username = authenticator.login("Login","main")
    if authetication_status == False:
        st.error("Username/Password is incorrect")
    if authetication_status == None:
        st.warning("Please enter your Username and Password")
    if authetication_status:
        authenticator.logout('Logout', 'main')
        st.markdown(f"Welcome {name}")
        option = st.selectbox("Select a option",("RollNumber","Percentage"))
        if option == "RollNumber":
            rollNumber = st.text_input("Roll Number")
        if option == "Percentage":
            percent = st.text_input("Percent")
            col = db.Attendance
            
            
    
def main():
    getData()
  
if __name__ == '__main__' :
    main()