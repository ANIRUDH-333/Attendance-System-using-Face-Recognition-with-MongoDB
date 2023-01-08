import streamlit as st
import numpy as np
from pymongo import MongoClient

def getData():
    
    st.markdown("Click on Clear Button to Clear the Attendance Data")
    rollNumber = st.text_input("Roll Number")
    client = MongoClient('mongodb://localhost:27017/')
    db = client.AttendanceSystem
    col = db.Attendance
    if st.button("Clear"):
        if rollNumber == "":       
            col.drop()
            st.success("Done")
        else:
            col2 = db.UserData
            userdata = col2.find_one({"RollNumber" : rollNumber})
            col.find_one_and_update({"Name" : userdata["Name"]},{"$set" : {"Attendance" : "Absent"}})
    
def main():
    getData()
  
if __name__ == '__main__' :
    main()