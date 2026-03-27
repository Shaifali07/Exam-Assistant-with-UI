def generate_paper(SUBJECT,COs,syllabus,instructions=' '):
    from langchain_groq import ChatGroq
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
    import os
    from dotenv import load_dotenv
    from pydantic import BaseModel, Field

    # Load environment variables from .env file
    load_dotenv()

    # Get the API key
    groq_api_key = os.environ.get("GROQ_API_KEY")
    llm=ChatGroq(
    model_name="openai/gpt-oss-120b",
    temperature=0)

    class Question_Formation(BaseModel):
        Question: str = Field(description="Question number like Q.1 a, Q.1 b,Q.2 c")
        CO:str=Field(description="course outcome CO like CO1,CO2,CO3")
        Taxonomy:str=Field(description="Blooms taxonomy A for apply, N for analysis, E for evaluate, R for remember, U for understand")
        Content:str=Field(description="Question formed")
        Marks:int=Field(description="Marks for question")
    parser=JsonOutputParser(pydantic_object=Question_Formation)
    format_instructions = parser.get_format_instructions()
    prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert academic question paper setter. Generate the questions from the all over syllabus." ),
            ("human",'''Generate a university-level question paper based on the following details:
            INPUTS
            Subject: {SUBJECT}
            Course Outcomes {COs}
            Syllabus: {syllabus}
            STRICT RULE:
            All the question must be from the syllabus
            
            
            
            EXAM STRUCTURE
            Total Marks = 36
            Total Questions = 3 (Q.1, Q.2, Q.3) Each Question = 12 Marks
            IMPORTANT CO RULES
            Q.1 (Objective Type – 12 Marks) - 6 sub-questions (a–f),
            each 2 marks - Must be numerical / analytical / problem-solving/ Evaluation- true/false and justification
            CO Assignment: - Either all from same CO OR mixed COs - Prefer maximum CO coverage ---
            
            
            Q.2 (Attempt ANY TWO out of THREE – 12 Marks) - Each question = 6 marks
            Format: (6) OR (4+2) OR (3+3)
            
            STRICT RULE:
            ALL THREE questions MUST belong to SAME CO
            Example: Q.2(a) → CO2 Q.2(b) → CO2 Q.2(c) → CO2
            Do NOT mix COs
            Each question must: - Be numerical / application / algorithm-based - Have all sub-parts from SAME CO
            
            Q.3 (Attempt ANY ONE option – 12 Marks)
            Two options: Option 1 Option 2
            Each option contains: - Two questions (6 marks each) OR structured. If structured, structure must be same in both options
            Example:
            Option 1 → CO3 (6 marks) + CO4 (2 marks)+ CO5 (2 marks)
            Option 2 → CO3 + CO4
            
            STRICT RULE: - COs can be mixed WITHIN an option
            BUT both options MUST have SAME SET of COs
            
            VERY VERY STRICT RULE:
            {instructions}
            
            Example:
            Option 1 → CO3 + CO4
            Option 2 → CO3 + CO4
            NOT allowed:
            Option 1 → CO2 + CO3
            Option 2 → CO1 + CO4
            MANDATORY REQUIREMENTS
            Each question must include: - Course Outcome (CO) - Bloom’s Level (Apply / Analyze / Evaluate)
            Maintain: - University-level difficulty - Balanced syllabus coverage
            Focus on: - Numericals, application based questions, Problem-solving
            Avoid: - Pure theory-only questions
            
            
            OUTPUT FORMAT - Clean, exam-ready format
            Clearly labeled Q.1, Q.2, Q.3
            Marks for each question - CO + Bloom’s level mentioned
            give images if necessary
            
            GOAL Generate a fully structured, strictly CO-compliant, numerical-focused university question paper following ALL rules above. follow {format_instructions} ''')])
    chain = prompt | llm | parser
    result = chain.invoke({"SUBJECT": SUBJECT,"COs":COs,"syllabus":syllabus, "format_instructions":format_instructions, "instructions":instructions})
    return result
