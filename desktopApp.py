import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFileDialog, QTextEdit, 
                             QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem, 
                             QProgressBar, QGridLayout, QScrollArea)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize

from resume_parser import parse_resume
from job_analyzer import analyze_job_description
from app import match_resume_to_job

class StyledButton(QPushButton):
    def __init__(self, text, icon=None):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background-color: #76ABAE;
                color: #EEEEEE;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 8px;
                transition: background-color 0.3s;
            }
            QPushButton:hover {
                background-color: #5C9A9D;
            }
            QPushButton:pressed {
                background-color: #4B868A;
            }
        """)
        if icon:
            self.setIcon(QIcon(icon))

class ResumeAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Resume Analyzer")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #222831;
            }
            QLabel {
                font-size: 14px;
                color: #EEEEEE;
            }
            QTextEdit {
                background-color: #31363F;
                border: 1px solid #ddd;
                border-radius: 5px;
                color: #EEEEEE;
            }
        """)
        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Tabs for different views
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Upload Tab
        upload_tab = QWidget()
        upload_layout = QVBoxLayout()
        upload_tab.setLayout(upload_layout)
        
        # Resume Upload Section
        resume_layout = QHBoxLayout()
        resume_label = QLabel("Resume:")
        self.resume_path = QLabel("No file selected")
        resume_upload_btn = StyledButton("Upload Resume")
        resume_upload_btn.clicked.connect(self.upload_resume)
        
        resume_layout.addWidget(resume_label)
        resume_layout.addWidget(self.resume_path)
        resume_layout.addWidget(resume_upload_btn)
        upload_layout.addLayout(resume_layout)
        
        # Job Description Upload Section
        job_layout = QHBoxLayout()
        job_label = QLabel("Job Description:")
        self.job_path = QLabel("No file selected")
        job_upload_btn = StyledButton("Upload Job Description")
        job_upload_btn.clicked.connect(self.upload_job_description)
        
        job_layout.addWidget(job_label)
        job_layout.addWidget(self.job_path)
        job_layout.addWidget(job_upload_btn)
        upload_layout.addLayout(job_layout)
        
        # Analyze Button
        analyze_btn = StyledButton("Analyze Match")
        analyze_btn.clicked.connect(self.analyze_match)
        upload_layout.addWidget(analyze_btn)
        
        # Results Tab
        results_tab = QWidget()
        results_layout = QVBoxLayout()
        results_tab.setLayout(results_layout)
        
        # Match Score Progress Bar
        match_score_layout = QHBoxLayout()
        match_score_label = QLabel("Match Score:")
        self.match_score_progress = QProgressBar()
        self.match_score_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
                background-color: #31363F;
                color: #EEEEEE;
            }
            QProgressBar::chunk {
                background-color: #76ABAE;
                width: 10px;
                margin: 0.5px;
            }
        """)
        match_score_layout.addWidget(match_score_label)
        match_score_layout.addWidget(self.match_score_progress)
        results_layout.addLayout(match_score_layout)
        
        # Skills Table
        self.skills_table = QTableWidget()
        self.skills_table.setColumnCount(2)
        self.skills_table.setHorizontalHeaderLabels(["Skill", "Status"])
        self.skills_table.setStyleSheet("""
            QTableWidget {
                background-color: #31363F;
                color: #EEEEEE;
                gridline-color: #76ABAE;
            }
            QHeaderView::section {
                background-color: #76ABAE;
                color: #222831;
            }
        """)
        results_layout.addWidget(self.skills_table)
        
        # Recommended Improvements
        improvements_label = QLabel("Recommended Improvements:")
        self.improvements_display = QTextEdit()
        self.improvements_display.setReadOnly(True)
        results_layout.addWidget(improvements_label)
        results_layout.addWidget(self.improvements_display)
        
        # Add tabs
        self.tab_widget.addTab(upload_tab, "Upload")
        self.tab_widget.addTab(results_tab, "Results")
        
        # Initialize file paths
        self.resume_file_path = None
        self.job_description_file_path = None
    
    def upload_resume(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Resume", "", 
                                                   "PDF Files (*.pdf);;Word Files (*.docx)")
        if file_path:
            self.resume_file_path = file_path
            self.resume_path.setText(os.path.basename(file_path))
    
    def upload_job_description(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Job Description", "", 
                                                   "Text Files (*.txt);;PDF Files (*.pdf)")
        if file_path:
            self.job_description_file_path = file_path
            self.job_path.setText(os.path.basename(file_path))
    
    def analyze_match(self):
        if not self.resume_file_path or not self.job_description_file_path:
            QMessageBox.warning(self, "Upload Error", "Please upload both resume and job description.")
            return
        
        try:
            # Parse resume
            resume_data = parse_resume(self.resume_file_path)
            
            # Analyze job description
            job_description = analyze_job_description(self.job_description_file_path)
            
            # Match resume to job
            match_result = match_resume_to_job(resume_data, job_description)
            
            # Update match score progress bar
            self.match_score_progress.setValue(int(match_result['match_score']))
            
            # Populate skills table
            self.skills_table.setRowCount(0)
            
            # Separate matched and missing skills
            matched_skills = match_result['matched_skills']
            missing_skills = match_result['recommended_improvements']
            
            # Add matched skills first
            for skill in matched_skills:
                row = self.skills_table.rowCount()
                self.skills_table.insertRow(row)
                self.skills_table.setItem(row, 0, QTableWidgetItem(skill.capitalize()))
                self.skills_table.setItem(row, 1, QTableWidgetItem("Matched"))
            
            # Add missing skills
            for skill in missing_skills:
                row = self.skills_table.rowCount()
                self.skills_table.insertRow(row)
                self.skills_table.setItem(row, 0, QTableWidgetItem(skill.capitalize()))
                self.skills_table.setItem(row, 1, QTableWidgetItem("Missing"))
            
            # Resize columns to content
            self.skills_table.resizeColumnsToContents()
            
            # Update improvements display
            improvements_text = "To improve your resume, consider adding the following skills:\n\n"
            improvements_text += "\n".join(f"• {skill.capitalize()}" for skill in missing_skills)
            
            # Add context from job description
            job_description_text = job_description.get('raw_text', '')
            improvements_text += f"\n\nJob Description Context:\n{job_description_text}"
            
            self.improvements_display.setText(improvements_text)
            
            # Switch to Results tab
            self.tab_widget.setCurrentIndex(1)

        except Exception as e:
            QMessageBox.critical(self, "Analysis Error", f"Error during analysis: {str(e)}")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern, cross-platform style
    analyzer_app = ResumeAnalyzerApp()
    analyzer_app.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()