#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import streamlit as st
from app import ResumeReader,ResumeScreener

st.set_page_config(page_title="ResumeReader", page_icon=":books:")

#defining reader and screener
reader=ResumeReader()
screener=ResumeScreener()

#Streamlit Interface
st.markdown('<h1 style="text-align: center;">Resume Screening Web App</h1>', unsafe_allow_html=True)

#get input
st.subheader("Upload resume here:")
uploaded_file = st.file_uploader(" ",type=['pdf','docx','txt'])

if uploaded_file is not None:
    resume_text=reader.extract_text_from_resume(uploaded_file)

    #extracting details from resume
    extracted_resume={
        'contact_info':reader.extract_contact_details(resume_text),
        'education':reader.extract_education(resume_text),
        'skills':reader.extract_skills(resume_text),
        'experience':reader.extract_experience(resume_text)
        }

#-----------------------------------job requirements-----------------------------------------------#
#*****************************UPDATE JOB REQUIREMENTS HERE*****************************************#
    job_requirements={
        'required_skills':['Python', 'SQL', 'Machine Learning'],
        'required_education':'Bachelor',
        'job_description':"""
        Looking for a Python developer with strong SQL skills and 
        experience in machine learning. Bachelor's degree required.
        """
    }

    #screening resume
    screening_results=screener.screen_resume(extracted_resume,job_requirements)

    #calculate similarity score
    match_percentage=screener.match_score(resume_text,job_requirements['job_description'])

    #screening results
    st.subheader("Screening Results")

    #creating a dictionary of results
    results={
        'Email':[extracted_resume['contact_info']['email']],
        'Phone Number':[extracted_resume['contact_info']['phone_number']],
        'Overall Score':[screening_results['overall_score']],
        'Match Percentage':[f"{match_percentage}%"]
    }

    #converting dictionary to dataframe
    results_df=pd.DataFrame(results)

    #displaying dataframe
    st.table(results_df)