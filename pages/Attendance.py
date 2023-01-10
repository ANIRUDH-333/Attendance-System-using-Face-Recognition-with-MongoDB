import streamlit as st
import numpy as np
from pymongo import MongoClient
import cv2
import face_recognition
import os
import base64
from datetime import date

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
def image_encode():
    known_image = face_recognition.load_image_file("BDMS/check_image/faces.jpg")
    img_encode = face_recognition.face_encodings(known_image)[0]
    return img_encode

def detectFace(picture):
    cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
    haar_model = os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_default.xml')
    facedetect = cv2.CascadeClassifier(haar_model)
    if picture:
        test = os.listdir("BDMS/check_image/")
        with open('BDMS/bbbbb.jpg','wb') as file:
            file.write(picture.getbuffer()) 
        img = cv2.imread('BDMS/bbbbb.jpg')
        faces = facedetect.detectMultiScale(img,1.6,5)
        for x,y,w,h in faces:
            img_ = img[y:y+h,x:x+w]
            for images in test:
                if images.endswith(".jpg"):
                    os.remove(os.path.join("BDMS/check_image/", images))
            cv2.imwrite("BDMS/check_image/faces.jpg",img_)

def getData():
    add_bg_from_local('back_grd.jpg')
    st.title("Attendance System")
    st.subheader("Take Attendance")
    rollNumber = st.text_input("Roll Number")
    picture = st.camera_input("Take a picture")
    return rollNumber,picture

def checkAttendance(rollNumber,img_code):
    # client = MongoClient("mongodb+srv://dineshilla:dineshilla@cluster0.1tzkrhf.mongodb.net/?retryWrites=true&w=majority")
    client = MongoClient("mongodb://localhost:27017/")
    db = client.AttendanceSystem
    if st.button("Login"):
        col1 = db.UserData
        userData = col1.find_one({"RollNumber" : rollNumber})
        print(userData)
        print([np.array(list(userData['Face Code']))],)
        print(img_code)
        result = face_recognition.compare_faces([np.array(list(userData['Face Code']))], img_code)
        print(result)
        if result[0]:
            attendance = "Present"
            col2 = db.Attendance
            col2.insert_one({"Name" : userData['Name'],"RollNumber" : rollNumber,"Date": str(date.today()) ,"Attendance" : attendance })
            st.success(f"{userData['Name']} Present")
        if result[0] == False:
            attendance = "Absent"
            st.success("Face Not Matched")

def main():
    rollNumber,picture = getData()
    detectFace(picture)
    img_code = image_encode()
    if picture:
        checkAttendance(rollNumber,img_code)
    
if __name__ == '__main__' :
    main()
