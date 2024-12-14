import spacy
from typing import Dict, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class JobAnalyzer:
    def __init__(self, nlp=None):
        self.nlp = nlp if nlp else spacy.load("en_core_web_sm")
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def extract_requirements(self, job_description: str) -> Dict[str, List[str]]:
        """Extract key requirements from job description"""
        doc = self.nlp(job_description)
        
        requirements = {
            "required_skills": [],
            "preferred_skills": [],
            "experience": [],
            "education": []
        }
        
        # Process each sentence
        for sent in doc.sents:
            sent_text = sent.text.lower()
            
            # Check for required skills
            if any(keyword in sent_text for keyword in ["required", "must have", "essential"]):
                requirements["required_skills"].append(sent.text.strip())
            
            # Check for preferred skills
            elif any(keyword in sent_text for keyword in ["preferred", "nice to have", "desirable"]):
                requirements["preferred_skills"].append(sent.text.strip())
            
            # Check for experience requirements
            elif any(keyword in sent_text for keyword in ["experience", "years"]):
                requirements["experience"].append(sent.text.strip())
            
            # Check for education requirements
            elif any(keyword in sent_text for keyword in ["degree", "education", "qualification"]):
                requirements["education"].append(sent.text.strip())
        
        return requirements

    def calculate_match_score(self, resume_text: str, job_description: str) -> Tuple[float, Dict]:
        """Calculate match score between resume and job description"""
        # Vectorize texts
        texts = [resume_text, job_description]
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Get important terms from job description
        job_doc = self.nlp(job_description)
        important_terms = [token.text for token in job_doc if token.pos_ in ["NOUN", "PROPN"]]
        
        # Calculate term presence
        term_scores = {}
        resume_doc = self.nlp(resume_text.lower())
        resume_text_lower = resume_text.lower()
        
        for term in important_terms:
            term_lower = term.lower()
            if term_lower in resume_text_lower:
                term_scores[term] = 1.0
            else:
                term_scores[term] = 0.0
        
        return similarity, term_scores

    def analyze_skill_gaps(self, resume_skills: List[str], job_requirements: Dict[str, List[str]]) -> Dict:
        """Analyze skill gaps between resume and job requirements"""
        required_skills = set()
        for req in job_requirements["required_skills"]:
            doc = self.nlp(req.lower())
            required_skills.update([token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]])
        
        resume_skills_set = set(skill.lower() for skill in resume_skills)
        
        missing_skills = required_skills - resume_skills_set
        matching_skills = required_skills.intersection(resume_skills_set)
        
        return {
            "missing_skills": list(missing_skills),
            "matching_skills": list(matching_skills),
            "match_percentage": len(matching_skills) / len(required_skills) if required_skills else 0
        }

    def generate_improvement_suggestions(self, skill_gaps: Dict) -> List[str]:
        """Generate suggestions for improvement based on skill gaps"""
        suggestions = []
        
        if skill_gaps["missing_skills"]:
            suggestions.append("Consider adding the following skills to your resume:")
            for skill in skill_gaps["missing_skills"]:
                suggestions.append(f"- {skill}")
        
        if skill_gaps["match_percentage"] < 0.5:
            suggestions.append("Your resume might need significant improvements to match this job's requirements.")
        elif skill_gaps["match_percentage"] < 0.8:
            suggestions.append("Your resume matches some requirements but could be improved.")
        
        return suggestions
