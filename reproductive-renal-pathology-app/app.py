import streamlit as st
import json
import pandas as pd
from datetime import datetime
import os

# Set page config
st.set_page_config(
    page_title="Reproductive & Renal Pathology Exam Prep",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 30px;
    }
    .question-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border-left: 4px solid #3498db;
    }
    .correct-answer {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .incorrect-answer {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .note-container {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .problem-container {
        background-color: #e7f3ff;
        border-left: 4px solid #0066cc;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .footer {
        text-align: center;
        color: #666;
        font-size: 12px;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #ddd;
    }
    </style>
""", unsafe_allow_html=True)

# Load questions data
@st.cache_data
def load_questions():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'questions_database.json')
    with open(json_path, 'r') as f:
        return json.load(f)

questions_data = load_questions()

# Initialize session state
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'selected_answer' not in st.session_state:
    st.session_state.selected_answer = None
if 'show_explanation' not in st.session_state:
    st.session_state.show_explanation = False
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}

# Sidebar
with st.sidebar:
    st.title("🔬 Navigation")
    page = st.radio("Select Page", ["Home", "MCQ Questions", "SBA Questions", "Clinical Problems", "Study Notes", "About"])

# Main content
if page == "Home":
    st.markdown('<div class="main-header"><h1>🔬 Reproductive & Renal Pathology</h1><h3>Basic Science Exam Preparation</h3></div>', unsafe_allow_html=True)
    
    st.write("Comprehensive pathology question bank focusing on **Reproductive** and **Renal Pathology** based on basic science human pathology curriculum.")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("MCQ Questions", len(questions_data.get("mcq", [])))
    with col2:
        st.metric("SBA Questions", len(questions_data.get("sba", [])))
    with col3:
        st.metric("Clinical Problems", len(questions_data.get("problems", [])))
    with col4:
        st.metric("Study Notes", len(questions_data.get("shortNotes", [])))
    
    st.markdown("---")
    
    st.subheader("📖 Content Coverage")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 🔴 Renal Pathology")
        st.write("""
        - Glomerular diseases (nephrotic & nephritic syndromes)
        - Tubular and interstitial diseases
        - Vascular diseases
        - Renal tumors
        - Acute and chronic kidney injury
        """)
    
    with col2:
        st.write("### 🔵 Reproductive Pathology")
        st.write("""
        - **Cervix**: HPV, CIN, cervical carcinoma
        - **Vagina**: VAIN, vaginal tumors
        - **Endometrium**: Hyperplasia, carcinoma types
        - **Ovaries**: Surface epithelial, germ cell, sex cord-stromal tumors
        - **Prostate**: BPH, adenocarcinoma, Gleason grading
        """)
    
    st.markdown("---")
    
    st.subheader("✨ Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**📝 MCQ Questions**")
        st.write("40 multiple choice questions with detailed explanations covering all major topics")
    
    with col2:
        st.write("**🎯 SBA Questions**")
        st.write("Single best answer questions with clinical scenarios and comprehensive explanations")
    
    with col3:
        st.write("**🧪 Clinical Problems**")
        st.write("Case-based problems with detailed answers and key concepts")
    
    st.markdown("---")
    
    st.info("💡 **Tip**: Start with Study Notes to review key concepts, then test yourself with MCQs and SBA questions!")
    
    # Footer
    st.markdown('<div class="footer">', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Developed By:")
    st.markdown("**Dr. Yousra Abdelatti**")
    st.markdown("**Dr. Mohammedelnagi Mohammed**")
    st.markdown("© 2025 Reproductive & Renal Pathology Exam Prep. All rights reserved.")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "MCQ Questions":
    st.title("📝 MCQ Questions")
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        system = st.selectbox(
            "Select System",
            ["All", "Renal", "Reproductive"],
            key="mcq_system_select"
        )
    
    with col2:
        show_answers = st.checkbox("Show Answers", value=False)
    
    # Get filtered questions
    all_mcqs = questions_data.get("mcq", [])
    
    if system != "All":
        all_mcqs = [q for q in all_mcqs if q.get("system") == system]
    
    if not all_mcqs:
        st.warning("No questions found for the selected filters.")
    else:
        st.info(f"Found {len(all_mcqs)} question(s)")
        
        # Display questions
        for idx, question in enumerate(all_mcqs):
            with st.container():
                st.markdown(f'<div class="question-container">', unsafe_allow_html=True)
                
                st.markdown(f"### Question {idx + 1} - {question.get('system', 'Unknown')}")
                st.write(question.get("question", ""))
                
                options = question.get("options", [])
                selected = st.radio(
                    "Select your answer:",
                    options=range(len(options)),
                    format_func=lambda x: f"{chr(65+x)}. {options[x]}",
                    key=f"mcq_{question.get('id')}"
                )
                
                if st.button("Submit Answer", key=f"submit_mcq_{question.get('id')}") or show_answers:
                    correct_answer = question.get("correct_answer", "")
                    user_answer = chr(65 + selected)
                    
                    if user_answer == correct_answer:
                        st.markdown(
                            f'<div class="correct-answer"><strong>✓ Correct!</strong><br><strong>Explanation:</strong> {question.get("explanation", "")}</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="incorrect-answer"><strong>✗ Incorrect</strong><br><strong>Correct Answer:</strong> {correct_answer}<br><strong>Explanation:</strong> {question.get("explanation", "")}</div>',
                            unsafe_allow_html=True
                        )
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("---")

elif page == "SBA Questions":
    st.title("🎯 Single Best Answer (SBA) Questions")
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        system = st.selectbox(
            "Select System",
            ["All", "Renal", "Reproductive"],
            key="sba_system_select"
        )
    
    with col2:
        show_answers = st.checkbox("Show Answers", value=False)
    
    # Get filtered questions
    all_sbas = questions_data.get("sba", [])
    
    if system != "All":
        all_sbas = [q for q in all_sbas if q.get("system") == system]
    
    if not all_sbas:
        st.warning("No questions found for the selected filters.")
    else:
        st.info(f"Found {len(all_sbas)} question(s)")
        
        # Display questions
        for idx, question in enumerate(all_sbas):
            with st.container():
                st.markdown(f'<div class="question-container">', unsafe_allow_html=True)
                
                st.markdown(f"### Question {idx + 1} - {question.get('system', 'Unknown')}")
                st.write(question.get("question", ""))
                
                options = question.get("options", [])
                selected = st.radio(
                    "Select your answer:",
                    options=range(len(options)),
                    format_func=lambda x: f"{chr(65+x)}. {options[x]}",
                    key=f"sba_{question.get('id')}"
                )
                
                if st.button("Submit Answer", key=f"submit_sba_{question.get('id')}") or show_answers:
                    correct_answer = question.get("correct_answer", "")
                    user_answer = chr(65 + selected)
                    
                    if user_answer == correct_answer:
                        st.markdown(
                            f'<div class="correct-answer"><strong>✓ Correct!</strong><br><strong>Explanation:</strong> {question.get("explanation_correct", "")}</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="incorrect-answer"><strong>✗ Incorrect</strong><br><strong>Correct Answer:</strong> {correct_answer}<br><strong>Why this is correct:</strong> {question.get("explanation_correct", "")}<br><br><strong>Why others are incorrect:</strong> {question.get("explanation_incorrect", "")}</div>',
                            unsafe_allow_html=True
                        )
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("---")

elif page == "Clinical Problems":
    st.title("🧪 Clinical Problems")
    
    # Filters
    system = st.selectbox(
        "Select System",
        ["All", "Renal", "Reproductive"],
        key="problem_system_select"
    )
    
    # Get filtered problems
    all_problems = questions_data.get("problems", [])
    
    if system != "All":
        all_problems = [p for p in all_problems if p.get("system") == system]
    
    if not all_problems:
        st.warning("No problems found for the selected filters.")
    else:
        st.info(f"Found {len(all_problems)} problem(s)")
        
        # Display problems
        for idx, problem in enumerate(all_problems):
            with st.container():
                st.markdown(f'<div class="problem-container">', unsafe_allow_html=True)
                
                st.markdown(f"### Problem {idx + 1} - {problem.get('system', 'Unknown')}")
                st.write(problem.get("question", ""))
                
                if st.button("Show Answer", key=f"show_answer_{problem.get('id')}"):
                    st.markdown("### Answer:")
                    st.write(problem.get("answer", ""))
                    
                    if "key_concepts" in problem:
                        st.markdown("### Key Concepts:")
                        for concept in problem.get("key_concepts", []):
                            st.write(f"• {concept}")
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("---")

elif page == "Study Notes":
    st.title("📖 Study Notes")
    
    system = st.selectbox(
        "Select System",
        ["All", "Renal", "Reproductive"]
    )
    
    notes = questions_data.get("shortNotes", [])
    
    if system != "All":
        notes = [n for n in notes if n.get("system") == system]
    
    if not notes:
        st.warning("No study notes found for the selected system.")
    else:
        st.info(f"Found {len(notes)} note(s)")
        for note in notes:
            with st.expander(f"📝 {note.get('title', '')} - {note.get('system', '')}"):
                st.markdown(f'<div class="note-container">', unsafe_allow_html=True)
                st.markdown(note.get("content", ""))
                st.markdown('</div>', unsafe_allow_html=True)

elif page == "About":
    st.title("ℹ️ About This Platform")
    
    st.write("""
    ### Reproductive & Renal Pathology Exam Preparation
    
    This comprehensive question bank is designed specifically for medical students studying **basic science human pathology**, 
    with focus on Reproductive and Renal systems.
    
    #### Content Overview
    
    - **40 MCQ Questions** with detailed explanations
    - **6 SBA Questions** with clinical scenarios
    - **4 Clinical Problems** with comprehensive answers
    - **9 Study Notes** covering key topics
    
    #### Reproductive Pathology Topics
    
    - **Cervix**: HPV infection, CIN, cervical carcinoma
    - **Vagina**: VAIN, vaginal tumors, DES-related pathology
    - **Endometrium**: Hyperplasia, Type I & II carcinomas
    - **Ovaries**: Epithelial, germ cell, and sex cord-stromal tumors
    - **Prostate**: BPH, adenocarcinoma, Gleason grading
    
    #### Renal Pathology Topics
    
    - Glomerular diseases (nephrotic and nephritic syndromes)
    - Tubular and interstitial diseases
    - Acute tubular necrosis
    - Renal cell carcinoma types
    - Diabetic nephropathy
    - IgA nephropathy and other glomerulonephritides
    
    #### Features
    
    ✓ Based on basic science pathology curriculum
    ✓ Detailed explanations for all questions
    ✓ Clinical correlation and key concepts
    ✓ Comprehensive study notes
    ✓ Filter by system for focused study
    
    """)
    
    st.markdown("---")
    
    st.subheader("Medical Content Developed By:")
    st.write("**Dr. Yousra Abdelatti**")
    st.write("**Dr. Mohammedelnagi Mohammed**")
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 12px;">
    © 2025 Reproductive & Renal Pathology Exam Prep. All rights reserved.<br>
    All rights reserved to Dr. Yousra Abdelatti and Dr. Mohammedelnagi Mohammed.<br>
    <br>
    Designed for medical students studying basic science human pathology.
    </div>
    """, unsafe_allow_html=True)

# Footer on all pages
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 11px; margin-top: 30px;">
© 2025 Reproductive & Renal Pathology Exam Prep. All rights reserved to Dr. Yousra Abdelatti and Dr. Mohammedelnagi Mohammed.
</div>
""", unsafe_allow_html=True)
