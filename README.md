# Resume-Parser-Screener
This project is a web application built using spaCy, PyPDF2, re, scikit-learn, and Streamlit. It is designed to assist users in analyzing resumes by extracting relevant details and matching them against specified job requirements using advanced NLP techniques.

## Overview
The Resume Reading & Job Matching Web App processes uploaded resumes to extract key details such as contact information and skills. It then performs a similarity analysis, providing an overall match score and percentage, indicating how well the resume aligns with the specified job requirements.

## Features
* **Resume Upload**: Users can upload a resume in PDF format.
* **Detail Extraction**: The app extracts contact details, skills, and other relevant information using NLP.
* **Job Matching**: Analyzes and matches the resume content against predefined job requirements, generating an overall score and match percentage.
* **User-Friendly Interface**: Built with Streamlit to ensure ease of use and interactivity.

## Usage
1. Run the Streamlit app: `streamlit run webapp.py`
2. Upload your resume in PDF format.
3. The app will extract and display your contact details.
4. Enter or load the job requirements.
5. View the overall score and match percentage to evaluate how well your resume fits the job.

## Technologies Used
* **Natural Language Processing**: spaCy for text parsing and named entity recognition.
* **PDF Processing**: PyPDF2 for reading PDF files.
* **Text Processing**: re for regular expressions to clean and extract text data.
* **Machine Learning**: scikit-learn for calculating similarity scores.
* **Web Framework**: Streamlit for creating a user-friendly web interface.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
