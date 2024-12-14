# AI Resume Analyzer 🚀

An intelligent resume analysis tool that helps recruiters streamline their hiring process and provides valuable feedback to job seekers. Built with Python, Streamlit, and advanced NLP techniques.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.29.0-red.svg)
![spaCy](https://img.shields.io/badge/spacy-3.7.2-green.svg)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎯 Features

- **Resume Parsing**: Extract information from PDF and DOCX resumes
  - Contact information
  - Skills and technologies
  - Education history
  - Work experience

- **Job Description Analysis**:
  - Extract key requirements and qualifications
  - Identify required and preferred skills
  - Parse experience and education requirements

- **Smart Matching**:
  - Calculate resume-job description match scores
  - Identify skill gaps
  - Provide targeted improvement suggestions
  - Visualize matching metrics

- **Modern Web Interface**:
  - Clean and intuitive design
  - Real-time analysis
  - Interactive visualizations
  - Responsive layout

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/Thesnak/ai-resume-analyzer.git
cd ai-resume-analyzer
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download the spaCy model:
```bash
python -m spacy download en_core_web_sm
```

## 🚀 Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to `http://localhost:8501`

3. Use the sidebar to:
   - Upload a resume (PDF/DOCX)
   - Enter or paste a job description

4. View the analysis results:
   - Overall match score
   - Skill gap analysis
   - Improvement suggestions
   - Detailed resume breakdown

## 📁 Project Structure

```
ai-resume-analyzer/
├── app.py                 # Main Streamlit application
├── resume_parser.py       # Resume parsing functionality
├── job_analyzer.py        # Job description analysis
├── requirements.txt       # Project dependencies
├── README.md             # Project documentation
├── test_data/            # Sample data for testing
│   └── job_descriptions.txt
└── uploads/              # Temporary storage for uploads
```

## 🔧 Technical Details

- **Resume Parsing**: Uses textract for document text extraction and spaCy for NLP processing
- **Text Analysis**: Implements TF-IDF vectorization and cosine similarity for matching
- **Skill Extraction**: Custom NER and pattern matching for skill identification
- **Frontend**: Streamlit for the web interface with Plotly for visualizations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- spaCy for providing excellent NLP tools
- Streamlit for the amazing web framework
- The open-source community for various dependencies

## 📧 Contact

Mohamed Elsayed - [@Thesnak](https://github.com/Thesnak)

Project Link: [https://github.com/Thesnak/ai-resume-analyzer](https://github.com/Thesnak/ai-resume-analyzer)
