#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import spacy
import PyPDF2
import docx
import re
import json
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# In[2]:


class ResumeReader:
    def __init__(self):
        #Loading SpaCy English model
        self.nlp=spacy.load('en_core_web_sm')

        #Initialize Regular Expression patterns for email and phone number
        self.email_pattern=r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
        self.phone_pattern=r"\+?\d{1,4}[\s-]?\(?\d{1,4}\)?[\s-]?\d{1,4}[\s-]?\d{1,4}[\s-]?\d{1,9}"

        #Initialize skill dictionary
        #---------------------------Add More Skills Here--------------------------------------------#
        self.skills_set={
            'programming':['python', 'java', 'javascript', 'c++', 'ruby', 'sql'],
            'frameworks':['react', 'django', 'flask', 'laravel','angular', 'spring'],
            'databases':['mysql', 'mongodb', 'postgresql', 'oracle'],
            'tools':['git', 'docker', 'kubernetes', 'aws', 'azure']
        }

    #function to extract text from pdf,docx and .txt files
    def extract_text_from_resume(self,file):
        text=""
        if file.name.endswith('.pdf'):
            reader=PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()+'\n'
        elif file.name.endswith('docx'):
            doc=docx.Document(file)
            for paragraph in doc.paragraphs:
                text=paragraph.text+'\n'
        elif file.name.endswith('.txt'):
            text=file.read()
        return text

    #extract contact details
    def extract_contact_details(self,text):
        #Regular expression to extract email addresss
        email_match=re.search(self.email_pattern,text)
        email=email_match.group(0) if email_match else None

        #Regular expression to extract phone number
        phone_match=re.search(self.phone_pattern,text)
        phone=phone_match.group(0) if phone_match else None

        return {
            "email":email,
            "phone_number":phone
        }

    #extract education
    def extract_education(self,text):
        doc=self.nlp(text)
        edu_keywords=['bsc','msc','bachelor','master','phd','degree','university','college']
        education=[]
        for sent in doc.sents:
            if any(keyword in sent.text.lower() for keyword in edu_keywords):
                education.append(sent.text.strip())
        return education

    #extract skills 
    def extract_skills(self,text):
        skills_found={category: [] for category in self.skills_set}
        text_lower=text.lower()

        for category,skills in self.skills_set.items():
            for skill in skills:
                if skill in text_lower:
                    skills_found[category].append(skill)
        return skills_found

    #extract experience
    def extract_experience(self,text):
        experience=[]
        doc=self.nlp(text)
        experience_Keywords=['experience', 'work', 'employment', 'job', 'position']

        for sent in doc.sents:
            if any(keyword in sent.text.lower() for keyword in experience_Keywords):
                experience.append(sent.text.strip())
        return experience


# In[3]:


class ResumeScreener:
    def __init__(self):
        self.vectorizer=TfidfVectorizer(stop_words='english')

    #calculate match score
    def match_score(self,resume_text,job_description):
        tfidf_matrix=self.vectorizer.fit_transform([resume_text,job_description])
        similarity=cosine_similarity(tfidf_matrix[0:1],tfidf_matrix[1:2])[0][0]
        return round(similarity * 100, 2)

    #evaluating extracted details with required qualifications
    def screen_resume(self,extracted_resume,job_requirements):
        matches={
            'skills_match':[],
            'education_match':[],
            'overall_score':0
        }

        #checking skills match
        required_skills=job_requirements.get('required_skills',[])
        for skill in required_skills:
            if any(skill.lower() in skills for skills in extracted_resume['skills'].values()):
                matches['skills_match'].append(skill)

        #checking education match
        required_education=job_requirements.get('required_education','').lower()
        education_extracted=' '.join(extracted_resume['education']).lower()
        matches['education_match']=required_education in education_extracted

        #calculate overall score
        matches['overall_score']=(
            (len(matches['skills_match'])/len(required_skills))*60 +    #weight for skills is 60%
            (matches['education_match'])*40    #weight for education is 40%
        )
        return matches