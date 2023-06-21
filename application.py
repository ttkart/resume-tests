"""THIS FILE RUNS THE APPLICATION"""

# import required modules
import streamlit as st
import pdfplumber
import Resume_scanner


# global values
comp_pressed = False
score = 0

#Sidebar
flag = 'HuggingFace-BERT'
with st.sidebar:
    st.markdown('**Which embedding do you want to use**')
    options = st.selectbox('Which embedding do you want to use',
                            ['HuggingFace-BERT', 'Doc2Vec (doesnt work)'],
                            label_visibility="collapsed")
    flag = options

#main content
tab1, tab2 = st.tabs(["**Home**","**Results**"]) #tabs array

# Tab Home
with tab1:
    """
    This is the Home tab where we can add many resumes as we and compare it with the
    job description
    """
    st.title("Resume - Job Comparison Metrics")
    uploaded_files = st.file_uploader('**Choose your resume.pdf file:** ', type="pdf", accept_multiple_files = True)
    #st.write(uploaded_files)
    st.write("")
    JD = st.text_area("**Enter the job description:**")
    comp_pressed = st.button("Compare the both for similarity!")
    if comp_pressed:
        #st.write(uploaded_files[0].name)
        score = Resume_scanner.compare(uploaded_files, JD, flag) #this is where we are getting the resume input


# Tab Results
"""In this tab we can have multiple resumes with scores"""
with tab2:
    st.header("Results")
    my_dict = {}
    if comp_pressed:
        for i in range(len(score)):
            my_dict[uploaded_files[i].name] = score[i]
        print(my_dict)
        sorted_dict = dict(sorted(my_dict.items()))
        print(sorted_dict)
        for i in sorted_dict.items():
            with st.expander(str(i[0])):
                st.write("Score is: ", i[1])
    else:
        st.write("#### Throw in some Resumes to see the score :)")
