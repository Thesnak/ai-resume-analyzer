import spacy
import re
from typing import Dict, List, Set
import textract
from pathlib import Path

class ResumeParser:
    def __init__(self, nlp=None):
        self.nlp = nlp if nlp else spacy.load("en_core_web_sm")
        self.skill_patterns = self._load_skill_patterns()

    def _load_skill_patterns(self) -> Set[str]:
        """Load common technical skills and frameworks"""
        return {
            # Programming Languages
            "python", "java", "javascript", "c++", "ruby", "php", "swift", "kotlin",
            # Web Technologies
            "html", "css", "react", "angular", "vue.js", "node.js", "django", "flask",
            # Data Science
            "machine learning", "deep learning", "tensorflow", "pytorch", "pandas",
            "numpy", "scikit-learn", "data analysis", "sql", "mysql", "postgresql",
            # Cloud Platforms
            "aws", "azure", "google cloud", "docker", "kubernetes",
            # Other Skills
            "git", "agile", "scrum", "rest api", "graphql"
        }

    def extract_text(self, file_path: str) -> str:
        """Extract text from various file formats"""
        try:
            text = textract.process(file_path).decode('utf-8')
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from file: {str(e)}")

    def extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information from text"""
        doc = self.nlp(text)
        
        # Initialize contact info
        contact_info = {
            "email": "",
            "phone": "",
            "linkedin": ""
        }
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info["email"] = emails[0]
        
        # Phone pattern
        phone_pattern = r'\b(?:\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact_info["phone"] = phones[0]
        
        # LinkedIn pattern
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin = re.findall(linkedin_pattern, text)
        if linkedin:
            contact_info["linkedin"] = linkedin[0]
        
        return contact_info

    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text"""
        doc = self.nlp(text.lower())
        skills = set()
        
        # Extract skills based on pattern matching
        for token in doc:
            if token.text in self.skill_patterns:
                skills.add(token.text)
            
            # Check for compound skills (e.g., "machine learning")
            if token.i < len(doc) - 1:
                bigram = token.text + " " + doc[token.i + 1].text
                if bigram in self.skill_patterns:
                    skills.add(bigram)
        
        return list(skills)

    def extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education information"""
        doc = self.nlp(text)
        education = []
        
        # Common education keywords
        edu_keywords = {"degree", "bachelor", "master", "phd", "bsc", "msc", "b.tech", "m.tech"}
        
        for sent in doc.sents:
            sent_text = sent.text.lower()
            if any(keyword in sent_text for keyword in edu_keywords):
                education.append({"description": sent.text.strip()})
        
        return education

    def extract_experience(self, text: str) -> List[Dict[str, str]]:
        """Extract work experience information"""
        doc = self.nlp(text)
        experience = []
        
        # Common work experience keywords
        work_keywords = {"work", "experience", "employed", "job", "position"}
        
        for sent in doc.sents:
            sent_text = sent.text.lower()
            if any(keyword in sent_text for keyword in work_keywords):
                experience.append({"description": sent.text.strip()})
        
        return experience

    def parse_resume(self, file_path: str) -> Dict:
        """Main method to parse resume and extract all information"""
        text = self.extract_text(file_path)
        
        return {
            "contact_info": self.extract_contact_info(text),
            "skills": self.extract_skills(text),
            "education": self.extract_education(text),
            "experience": self.extract_experience(text),
            "raw_text": text
        }
