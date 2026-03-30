import streamlit as st
from llm import generate_paper
import pandas as pd
import json
from io import BytesIO

st.title("Your Exam Assistant 👩🏻‍💻")
st.caption("Generate question papers with CO mapping, Bloom's taxonomy distribution, and attainment-friendly design.")
@st.cache_data
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()
df = pd.DataFrame()

with st.form("paper_generator"):
   SUBJECT= st.text_input("Enter the Subject Name")
   COs=st.text_area("Enter Course Outcomes", height=150, help="Copy Paste your Course Outcomes here")
   Examination=st.radio("Select Examination",["Sessional","External"])
   Syllabus=st.text_area("Enter Subject Syllabus",height=400, help="Copy Paste your Syllabus here")
   Insturctions=st.text_area("Enter the Instructions (if any)",height=150, help= '''Enter any additional rules or preferences for generating the question paper.
                             Example:
                             1) All questions in Q.1 must be from CO2.
                             2) Both options in Q.3 must have the same CO(s) Allowed: Option 1 → CO4 + CO5, Option 2 → CO4 + CO5, Not allowed: Option 1 → CO3 + CO5, Option 2 → CO2 + CO4
                             ''')

   submitted = st.form_submit_button("Submit")
   if submitted:
            generated_paper=generate_paper(SUBJECT, COs,Examination, Syllabus,Insturctions)
            df = pd.DataFrame(generated_paper)
            st.table(df)
# Create download button
st.download_button(
                     label="Download Excel",
                     data=to_excel(df),
                     file_name='data.xlsx',
                     mime='application/vnd.ms-excel'
                     )
