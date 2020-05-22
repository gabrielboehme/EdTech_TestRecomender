import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

#Importing file
test = pd.read_csv('Corrected_test/corrected_test.csv')

#Number of students
nb_students = len(test.groupby('Id').count())

#Studens mean score
students_info = test[['Id','Score','Subject_Questions','Graduated_parents','Family_monthly_earnings','has_sibblings','has_internet','study_hours_per_week']].groupby(['Id']).agg({'Score':'sum',
                                                                            'Family_monthly_earnings':'max','has_sibblings':'max','has_internet':'max','study_hours_per_week':'max'})
only_sub = test[['Subject','Subject_Questions']].groupby('Subject').max()
total_questions = only_sub['Subject_Questions'].sum()

students_info['General Mean Score %'] = students_info['Score']/total_questions

#Generating new DataFrames

#Statistics for each subject
subjects = test.loc[:,['Subject','Score']].groupby('Subject').agg({'Score':['mean','std']}).reset_index()
subjects.columns = ['Subject','Mean Score','Standart Deviation']

#Statistics for each student
student_table = test.groupby(['Id','Subject']).agg({'Score':'sum','Subject_Questions':'max'}).reset_index()
student_table['Score %'] = student_table['Score']/student_table['Subject_Questions']
student_table = student_table.merge(subjects[['Mean Score','Subject']],how='left',right_on='Subject',left_on='Subject')
student_table.rename({'Mean Score':'General Mean Score %','Subject_Questions':'Number of Questions'}, axis=1, inplace=True)


#Page styling
h1 = '''
<div style="text-align:center;background-color:PaleTurquoise;padding:15px;border-radius:5px;width:775px"> 
	<p style="font-size:50px"> Mock Test Painel </p>
</div>

'''

h2 = '''
<div style="text-align:center"> 
	<p style="font-size:25px"> Welcome to the Mock Test Painel, with general statistics of the test! </p>
</div>

'''

st.markdown(h1,unsafe_allow_html=True)
st.markdown(h2,unsafe_allow_html=True)

report_list = ['General Report','Students Report','Students General Information','Recomendations']
sidebar_opt = st.sidebar.selectbox('Choose report style',report_list)

#General report
if sidebar_opt == 'General Report':

    st.markdown("# General Report!")

    formatacao_1 = {'Mean Score':"{:.2%}"}
    st.table(subjects.style.format(formatacao_1))

    subject_graph = subjects[['Subject','Mean Score']].set_index('Subject')
    st.bar_chart(subject_graph, height=500)

elif sidebar_opt == 'Students Report':

    #Titles
    st.markdown("# Students Report")
    st.text('Select desired student.')
    
    #Id Selector
    documents = list(set(test['Id']))
    selected_student = st.selectbox('Document number:', documents).strip()

    #Table Settings
    formatacao_2 = {'Score %':"{:.2%}",'General Mean Score %':"{:.2%}"}
    student_table.reset_index(drop=False,inplace=True)
    filter_student = student_table[student_table['Id'] == selected_student].reset_index(drop=True).drop('index',axis=1)
    st.table(filter_student.style.format(formatacao_2))

    #Chart
    students_graph = filter_student[['Subject','Score %','General Mean Score %']].set_index('Subject')
    st.line_chart(students_graph, height=500,width=1000)

    #Recomendations for that student
    st.markdown('# Recomendations')
    all_rec = pd.read_csv('Data/Recomendations.csv')
    rec_for_student = all_rec[all_rec['Id']==selected_student][['Recomendation','Date']]

    st.table(rec_for_student)


elif sidebar_opt == 'Students General Information':

    st.markdown('# Students General Information')
    st.text('This is a report focusing on correlation between students demographic \ninformation and their performance on the test.')

    #getting students info
    documents = list(set(test['Id']))
    selected_student_info = st.selectbox('Document number:', documents).strip()

    formatacao_3 = {'General Mean Score %':"{:.2%}"}
    students_info_final = students_info[students_info.index.isin([selected_student_info])]
    st.table(students_info_final.style.format(formatacao_3))
    
    #text
    st.markdown('# Correlation table')


    #Correlation map
    st.table(students_info.corr())
    st.line_chart(students_info.corr(), height=500,width=1100,use_container_width=False)

    #text
    st.markdown('# Histograms')

    for col in students_info.columns:
        
        #text
        st.text(f'Information: {col}')
        st.bar_chart(students_info[col],height=500,width=1100,use_container_width=False)


elif sidebar_opt == 'Recomendations':

    st.markdown('# Choose student to make recomendation:')
    documents = list(set(test['Id']))
    selected_student_info = st.selectbox('Document number:', documents).strip()

    recomendation = st.text_area('Recomend actions for the student')
    confirm = st.button('Confirm recomendation')
    all_rec = pd.read_csv('Data/Recomendations.csv')

    if confirm:
        
        st.text('confirmed')
        
        all_rec = all_rec.append({'Id':selected_student_info,'Recomendation':recomendation,'Date':date.today()},ignore_index=True)

        all_rec.to_csv('Data/Recomendations.csv')


    st.table(all_rec[['Id','Recomendation','Date']])