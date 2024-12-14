import streamlit as st
import spacy
import pandas as pd
import plotly.express as px
from pathlib import Path
import tempfile
import os
from resume_parser import ResumeParser
from job_analyzer import JobAnalyzer

# Load spaCy model
@st.cache_resource
def load_spacy_model():
    return spacy.load("en_core_web_sm")

def main():
    st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
    
    st.title("AI Resume Analyzer")
    
    # Initialize models and analyzers
    nlp = load_spacy_model()
    resume_parser = ResumeParser(nlp)
    job_analyzer = JobAnalyzer(nlp)
    
    # Sidebar
    st.sidebar.title("Upload Documents")
    
    # File upload
    uploaded_resume = st.sidebar.file_uploader("Upload Resume", type=["pdf", "docx"])
    
    # Job description input
    job_description = st.sidebar.text_area("Enter Job Description")
    
    if uploaded_resume and job_description:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_resume.name).suffix) as tmp_file:
            tmp_file.write(uploaded_resume.getvalue())
            temp_path = tmp_file.name
        
        try:
            # Parse resume
            resume_data = resume_parser.parse_resume(temp_path)
            
            # Analyze job description
            job_requirements = job_analyzer.extract_requirements(job_description)
            
            # Calculate match score
            match_score, term_scores = job_analyzer.calculate_match_score(
                resume_data["raw_text"], 
                job_description
            )
            
            # Analyze skill gaps
            skill_gaps = job_analyzer.analyze_skill_gaps(
                resume_data["skills"],
                job_requirements
            )
            
            # Generate suggestions
            suggestions = job_analyzer.generate_improvement_suggestions(skill_gaps)
            
            # Display results in columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Resume Analysis")
                
                # Contact Information
                st.write("### Contact Information")
                for key, value in resume_data["contact_info"].items():
                    if value:
                        st.write(f"**{key.title()}:** {value}")
                
                # Skills
                st.write("### Skills")
                skills_df = pd.DataFrame({"Skills": resume_data["skills"]})
                st.dataframe(skills_df)
                
                # Education
                st.write("### Education")
                for edu in resume_data["education"]:
                    st.write(f"- {edu['description']}")
            
            with col2:
                st.subheader("Job Match Analysis")
                
                # Overall match score
                st.metric("Overall Match Score", f"{match_score*100:.1f}%")
                
                # Skill gap analysis
                st.write("### Skill Gap Analysis")
                st.write(f"Match Percentage: {skill_gaps['match_percentage']*100:.1f}%")
                
                if skill_gaps["missing_skills"]:
                    st.warning("Missing Skills:")
                    for skill in skill_gaps["missing_skills"]:
                        st.write(f"- {skill}")
                
                # Improvement suggestions
                st.write("### Suggestions for Improvement")
                for suggestion in suggestions:
                    st.write(suggestion)
                
                # Visualize term matches
                st.write("### Keyword Match Analysis")
                term_df = pd.DataFrame(
                    {"Term": list(term_scores.keys()), 
                     "Match": list(term_scores.values())}
                )
                fig = px.bar(
                    term_df,
                    x="Term",
                    y="Match",
                    title="Keyword Matches"
                )
                st.plotly_chart(fig)
        
        finally:
            # Clean up temporary file
            os.unlink(temp_path)

if __name__ == "__main__":
    main()
