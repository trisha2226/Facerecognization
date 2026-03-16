import streamlit as st
import cv2
import tempfile
from deepface import DeepFace
from PIL import Image


# BACKGROUND IMAGE
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://media.newindianexpress.com/newindianexpress%2F2025-11-23%2F3m0d6xxz%2FPU-teachers.jpg?w=1024&auto=format%2Ccompress&fit=max");
            background-size: cover;
            background-position: center;
            background-attsachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_url()


st.title("Face Verification System")

st.write("Upload a reference image and verify using your webcam")

uploaded_file = st.file_uploader("Upload Reference Image", type=["jpg","png","jpeg"])

if uploaded_file:

    ref_image = Image.open(uploaded_file)

    temp_ref = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    ref_image.save(temp_ref.name)

    if st.button("Start Camera Verification"):

        cap = cv2.VideoCapture(0)

        stframe = st.empty()

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            temp_frame = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            cv2.imwrite(temp_frame.name, frame)

            try:
                result = DeepFace.verify(
                    img1_path=temp_ref.name,
                    img2_path=temp_frame.name,
                    enforce_detection=False
                )

                if result["verified"]:
                    text = "MATCH"
                    color = (0,255,0)
                else:
                    text = "NOT MATCH"
                    color = (0,0,255)

            except:
                text = "FACE NOT DETECTED"
                color = (255,0,0)

            cv2.putText(frame, text, (50,50),
                        cv2.FONT_HERSHEY_SIMPLEX,1,color,2)

            stframe.image(frame, channels="BGR")

            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()