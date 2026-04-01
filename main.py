import streamlit as st
from llm import generate_paper, regenerate_question
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
if "generated" not in st.session_state:
    st.session_state["generated"] = False
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
   button_label = "Generate" if not st.session_state["generated"] else " 🔄 Regenerate"
   submitted = st.form_submit_button(button_label)

   if submitted:
            status_placeholder = st.empty()
            with st.spinner("Generating question paper... please wait ⏳"):
                generated_paper = generate_paper(SUBJECT, COs, Examination, Syllabus, Insturctions, status_placeholder)
            
            df = pd.DataFrame(generated_paper)
            st.session_state["generated"] = True
            st.session_state["df"] = df
            st.session_state["SUBJECT"] = SUBJECT
            st.session_state["COs"] = COs
            st.session_state["Syllabus"] = Syllabus
            st.rerun()
            # print("result returned")
            # st.table(df)
# Create download button
if "df" in st.session_state:
    df = st.session_state["df"]
    cols = st.columns([2, 1, 2, 6, 2, 2])
    headers = ["Question", "CO", "Taxonomy", "Content", "Marks", "Regenerate"]

    for col, header in zip(cols, headers):
        col.markdown(f"**{header}**")

    # Rows
    for i, row in df.iterrows():
        cols = st.columns([2, 1, 2, 6, 2, 2])

        cols[0].write(row["Question"])
        cols[1].write(row["CO"])
        cols[2].write(row["Taxonomy"])
        cols[3].write(row["Content"])
        cols[4].write(row["Marks"])

        if cols[5].button("🔄", key=f"regen_{i}"):
            st.session_state["regen_index"] = i
if "regen_index" in st.session_state:
    idx = st.session_state["regen_index"]

    with st.spinner(f"Regenerating {st.session_state['df'].loc[idx, 'Question']}..."):
        new_q = regenerate_question(
            st.session_state["df"].loc[idx],
            st.session_state["SUBJECT"],
            st.session_state["COs"],
            st.session_state["Syllabus"]
        )

    st.session_state["df"].loc[idx] = new_q
    # print(new_q)
    del st.session_state["regen_index"]
    st.rerun()
if "df" in st.session_state:
            st.download_button(
                label="Download Excel",
                data=to_excel(df),
                file_name='data.xlsx',
                mime='application/vnd.ms-excel'
            )
