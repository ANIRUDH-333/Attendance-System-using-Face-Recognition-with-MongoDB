import streamlit as st 
import streamlit_authenticator as stauth
import numpy as np
from pymongo import MongoClient
from pathlib import Path
import pickle
import pandas as pd



def getData():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.AttendanceSystem
    col = db.Attendance
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
        total_date = col.aggregate([{"$group" : {"_id" : "$Date",  "total" : {"$sum" : 1}}}])
        total = col.aggregate([{"$group" : {"_id" : "$RollNumber",  "total" : {"$sum" : 1}}}])
        count = 0
        for i in total_date:
            count = count + 1
        if option == "RollNumber":
            rollNumber = st.text_input("Roll Number")
            if rollNumber:
                qry = col.find_one({"RollNumber":rollNumber})
                name  = qry['Name']
            for i in total:
                if i["_id"] == rollNumber:
                    Total = i["total"]
                
            if st.button("Check Attendance"):
                if rollNumber == "":
                    st.caption("Enter RollNumber")
                tb = pd.DataFrame({"Name" : name,"Roll Number":rollNumber,"Number of Classes Present" : Total, "Total Number of Classes" : count,"Percentage" : (int(Total)*100)/int(count)},index=[0])
                hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
                st.markdown(hide_table_row_index, unsafe_allow_html=True)
                st.table(tb)

        if option == "Percentage":
            p_options = st.selectbox("Select a option",("Greater than","Less than"))
            percent = st.number_input("Percent",step=None)
            rn_list = []
            days_list = []
            name_list = []
            percent_list = []
            absent_list_rn = []
            absent_list_names = []
            absent_list_percent = []

            for i in total:
                rn = i["_id"]
                qry = col.find_one({"RollNumber":rn})
                nme  = qry["Name"]  
                name_list.append(nme)
                Total_ = i["total"]
                rn_list.append(rn)
                days_list.append(Total_)
                percent_ = (100*int(Total_))/int(count)
                qry = col.find_one({"RollNumber":rn})
                nm  = qry["Name"] 
                if p_options == "Less than":
                    if percent_ <= percent:
                        absent_list_rn.append(rn)           
                        absent_list_names.append(nm)
                        absent_list_percent.append(percent_)
                
                elif p_options == "Greater than":
                    if percent_ >= percent:
                        absent_list_rn.append(rn)
                        absent_list_names.append(nm)
                        absent_list_percent.append(percent_)
                percent_list.append(percent_)

            absent_data = pd.DataFrame({"Name" : absent_list_names,"Roll Number ":absent_list_rn,"Percentage":absent_list_percent})
            data = pd.DataFrame({"Name":name_list,"Roll Number": rn_list,"No of Classes Present": days_list,"Total No of Classes" : count,"Percentage" : percent_list})
            if st.button("Show"):
                hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
                st.markdown(hide_table_row_index, unsafe_allow_html=True)
                st.table(absent_data)
            if st.button("Show all"):
                st.markdown("### Attendance Summary")
                hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
                st.markdown(hide_table_row_index, unsafe_allow_html=True)
                st.table(data)
    
def main():
    getData()
  
if __name__ == '__main__' :
    main()