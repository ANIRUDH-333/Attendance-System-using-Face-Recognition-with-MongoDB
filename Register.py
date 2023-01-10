#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import numpy as np
from pymongo import MongoClient
import cv2
import face_recognition
import os
import base64
import pyautogui




# In[ ]:




def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

def streamlit_app():

    st.title("Attendance System")
    st.subheader("Register")
    add_bg_from_local('back_grd.jpg')
    name = st.text_input("Name")
    
    rollNumber = st.text_input("Roll Number ")
    branch = st.text_input("Branch Name ")
    emailID = st.text_input("Email ID ")
    phoneNumber = st.text_input("Phone Number ")
    picture = st.camera_input("Take a Picture")
    
    return name,rollNumber,branch,emailID,phoneNumber,picture

def detectFace(picture):
    cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
    haar_model = os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_default.xml')
    facedetect = cv2.CascadeClassifier(haar_model)
    if picture:
        test = os.listdir("BDMS/image_input/")
        with open('BDMS/aaaaa.jpg','wb') as file:
            file.write(picture.getbuffer()) 
        img = cv2.imread("BDMS/aaaaa.jpg")
        faces = facedetect.detectMultiScale(img,1.6,5)
        for x,y,w,h in faces:
            img_ = img[y:y+h,x:x+w]
            for images in test:
                if images.endswith(".jpg"):
                    os.remove(os.path.join("BDMS/image_input/", images))
            cv2.imwrite("BDMS/image_input/faces.jpg",img_)


    

def image_encode():
    known_image = face_recognition.load_image_file("BDMS/image_input/faces.jpg")
    img_encode = face_recognition.face_encodings(known_image)[0]
    img_code = list(img_encode)
    return img_code

def getData(name,rollNumber,branch,emailID,phoneNumber,img_code):
    client = MongoClient('mongodb://localhost:27017/')
    # db = client.test
    db = client.AttendanceSystem
    col = db.UserData
    if st.button("Register"):
        col.insert_one({"Name" : name,"RollNumber" : rollNumber,"Branch" : branch,"Email ID" : emailID,"Phone NUmber" : phoneNumber,"Face Code" : img_code})
        st.success("Successfully Registered")
    
def registerPage():
    name,rollNumber,branch,emailID,phoneNumber,picture = streamlit_app()
    detectFace(picture)
    img_code = image_encode() 
    getData(name,rollNumber,branch,emailID,phoneNumber,img_code)

def main():
    registerPage()
    
    
if __name__ == '__main__' :
    main()


# In[ ]:




