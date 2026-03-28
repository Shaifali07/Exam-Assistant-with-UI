import streamlit as st
from llm import generate_paper
import pandas as pd
import json

st.title("Your Exam Assistant 👩🏻‍💻")

with st.form("paper_generator"):
   SUBJECT= st.text_input("Enter the Subject Name")
   COs=st.text_area("Enter Course Outcomes", height=150)
   Examination=st.radio("Select Examination",["Sessional","External"])
   Syllabus=st.text_area("Enter Subject Syllabus",height=400)
   Insturctions=st.text_area("Enter the Instructions(if any)",height=150)

   submitted = st.form_submit_button("Submit")
   if submitted:
            generated_paper=generate_paper(SUBJECT, COs,Examination, Syllabus,Insturctions)
            df = pd.DataFrame(generated_paper)
            st.table(df)
