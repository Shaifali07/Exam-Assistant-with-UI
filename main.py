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
   Insturctions=st.text_area("Enter the Instructions   (if any)",height=150, value= '''Enter any additional rules or preferences for generating the question paper.
                             Example:
                             1) All questions in Q.1 must be from CO2.
                             2) Both options in Q.3 must have the same CO(s) Allowed: Option 1 → CO4 + CO5, Option 2 → CO4 + CO5, Not allowed: Option 1 → CO3 + CO5, Option 2 → CO2 + CO4
                             ''')

   submitted = st.form_submit_button("Submit")
   if submitted:
            generated_paper=generate_paper(SUBJECT, COs,Examination, Syllabus,Insturctions)
            df = pd.DataFrame(generated_paper)
            st.table(df)
