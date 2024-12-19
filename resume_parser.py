import os
import re
import logging
from typing import Dict, List, Set, Any
import textract
from pathlib import Path
import PyPDF2
import docx
import pdfplumber
import spacy

class ResumeParser:
    def __init__(self, nlp=None):
        self.nlp = nlp if nlp else spacy.load("en_core_web_sm")
        self.skill_patterns = self._load_skill_patterns()
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def _load_skill_patterns(self) -> Set[str]:
        """Load common technical skills and frameworks"""
        return {
            'Python', 'Java', 'JavaScript', 'C++', 'SQL', 
            'Machine Learning', 'Data Science', 'React', 
            'Node.js', 'Docker', 'Kubernetes', 'AWS'
        }

    def extract_text(self, file_path: str) -> str:
        """Extract text from various file formats"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_extension == '.pdf':
                return self._extract_pdf_text(file_path)
            elif file_extension in ['.docx', '.doc']:
                return self._extract_docx_text(file_path)
            else:
                return textract.process(file_path).decode('utf-8')
        
        except Exception as e:
            self.logger.error(f"Error extracting text: {e}")
            return ""

    def _extract_pdf_text(self, file_path):
        """
        Extract text from PDF using multiple methods for reliability
        """
        text = ""
        
        # Method 1: PyPDF2
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = " ".join(page.extract_text() for page in pdf_reader.pages)
        except Exception as e1:
            self.logger.warning(f"PyPDF2 extraction failed: {e1}")
            
            # Method 2: pdfplumber
            try:
                with pdfplumber.open(file_path) as pdf:
                    text = " ".join(page.extract_text() for page in pdf.pages if page.extract_text())
            except Exception as e2:
                self.logger.error(f"PDF text extraction failed: {e2}")
        
        return self._clean_text(text)

    def _extract_docx_text(self, file_path):
        """
        Extract text from DOCX files
        """
        try:
            doc = docx.Document(file_path)
            text = " ".join([paragraph.text for paragraph in doc.paragraphs])
            return self._clean_text(text)
        except Exception as e:
            self.logger.error(f"DOCX extraction error: {e}")
            return ""

    def _clean_text(self, text):
        """
        Clean and normalize extracted text
        """
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Optional: Remove non-printable characters
        text = ''.join(char for char in text if char.isprintable())
        
        return text

    def extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information from text"""
        contact_info = {}
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info['email'] = emails[0]
        
        # Extract phone number
        phone_pattern = r'\b(\+\d{1,2}\s?)?(\d{3}[-.]?)?\s?\d{3}[-.]?\d{4}\b'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact_info['phone'] = phones[0][0] + phones[0][1] + phones[0][2]
        
        return contact_info

    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        text_lower = text.lower()
        return [skill for skill in self.skill_patterns if skill.lower() in text_lower]

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

    def parse_resume(self, file_path: str) -> Dict[str, Any]:
        """
        Main method to parse resume and extract all information
        """
        # Extract text
        text = self.extract_text(file_path)
        
        # Extract skills
        skills = self.extract_skills(text)
        
        # Extract contact info
        contact_info = self.extract_contact_info(text)
        
        # Extract education
        education = self.extract_education(text)
        
        return {
            'raw_text': text,
            'skills': skills,
            'contact_info': contact_info,
            'file_path': file_path,
            'education': education
        }

def parse_resume(file_path: str) -> Dict[str, Any]:
    """
    Main function to parse resume
    
    Args:
        file_path (str): Path to the resume file
    
    Returns:
        Dict containing parsed resume information
    """
    parser = ResumeParser()
    
    return parser.parse_resume(file_path)
