#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st 
import pymongo
# from pymongo import MongoClient
import numpy as np

# def get_data():
#     #@st.experimental_singleton(suppress_st_warning=True)
#     client = MongoClient("mongodb+srv://dineshilla:dineshilla@cluster0.nv83pxi.mongodb.net/?retryWrites=true&w=majority")
#     db = client.sample 
#     items = db.test.find() 
#     items = list(items)        
#     return items


def main():
    st.title("test")
    num1 = st.text_input("Enter Number 1 ")
    num2 = st.text_input("Enter Number 2 ")

    conn_str = "mongodb+srv://dineshilla:dineshilla@cluster0.1tzkrhf.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
    db = client.new
    col = db.sample.find({sum : 4})
    
    if st.button("sum"):
        result = int(num1) + int(num2)
        st.success(str(col))
    
if __name__ == '__main__' :
    main()

