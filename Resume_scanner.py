"""THIS FILE IS FOR RESUME SCCANNING AND CALCULATING HOW SIMILAR A RESUME IS WITHH A JOB DESCCRIPTION"""

"""LIBRARY IMPORTS FOR RESUME SCANNING"""
import streamlit as st #importing our web framework
import pdfplumber  #importing our pdf python parser --> basically parses a pdf
from Models import get_HF_embeddings, cosine, get_doc2vec_embeddings # importing our NLP stuff


def extract_data(feed): 
    """This is to extract data from a resume pdf"""
    data = "" #empty string
    with pdfplumber.open(feed) as pdf: #opening a pdf using pdf plumber
        pages = pdf.pages
        for page in pages:
            data += page.extract_text() 
    
    """
    KNLU TO DO:
    - need to figure out a way to return the data in a pandas dataframe
    - have all the retured data frame as organized as you can
    """
    return data # returns the data extraccted from a PDF resume


def compare(uploaded_files, JD, flag = 'HuggingFace-BERT'):
    """We will take two thigns and compare
    Thing 1--> Resume PDF
    Thing 2--> Job description

    We will return how similar they are as a score 
    """

    if flag == 'HuggingFace-BERT': #if we are using the option 1 Huggingface-Bert Model 
        JD_embeddings = None  #initialize the job descriptio embeddingns as none
        resume_embeddings = [] #resume embeddings

        if JD is not None:
            JD_embeddings = get_HF_embeddings(JD) #we use hugginng faccemodel to get the job description embeddings
        if uploaded_files is not None:
            for i in uploaded_files:
                df = extract_data(i) #we extracct resume data
                resume_embeddings.append(get_HF_embeddings(df)) # we append the embeddings in the array
        
        """Now we have two arrays which are embeddings
        Think of it as two vectors:
        Vector 1: Job description
        Vector 2: Resume
        Now we will find similarity btwen these embeddings
        """
        if JD_embeddings is not None and resume_embeddings is not None:
            cos = cosine(resume_embeddings, JD_embeddings) #this gives us a numeric score on how similar the vectors are
            #it will gives us the score of how similar resume and job description are
            #st.write("Score is: ", cos)

    else:
        """The same steps as above except we are using different embeddigs"""
        df = []
        if uploaded_files is not None:
            for i in uploaded_files:
                data = extract_data(i)
                df.append(data)

        JD_embeddings, resume_embeddings = get_doc2vec_embeddings(JD, df)
        if JD_embeddings is not None and resume_embeddings is not None:
            cos = cosine(resume_embeddings, JD_embeddings)
        #st.write("Cosine similarity is: ", cos)

        """KNLU TO DO:
        - you need to figure out a better way to evaluate if a resume is fit for a job desccription """
    return cos
