import pandas as pd
import numpy as np
import sys
import os

#Load data to memory
def load_data():

    '''
    Output: Pandas DataFrames to this Data Transformation
    '''

    students_answers = pd.read_csv('Data/Students_Answers.csv')
    answers = pd.read_csv('Data/Answers.csv')
    subjects_map = pd.read_csv('Data/Subjects.csv')
    students_info = pd.read_csv('Data/Students_info.csv')


    return students_answers, answers, subjects_map, students_info


#Correct the test
def correct_test(students_answers, answers):

    '''
    Input: Pandas dataframe with students id's, (q)uestion and students answers.
    Output: Pandas dataframe with students id's, question and boolean with correct or false answer
    '''

    corrected_test = students_answers.merge(answers, how='left', right_on='Question', left_on='Question')
    corrected_test['Score'] = np.where(corrected_test['Student_Answer']==corrected_test['Right_Answer'],1,0)


    return corrected_test


#Add aditional information
def add_info(subjects_map, students_info, corrected_test):
    
    '''
    Input: 
        -Subjects for all the questions
        -Students general info
    Output: DataFrame with both informations
    '''

    corrected_test = corrected_test.merge(students_info, how='left', right_on='Id', left_on='Id')
    corrected_test = corrected_test.merge(subjects_map, how='left', right_on='Question', left_on='Question')

    corrected_test.fillna(value=0,axis=0, inplace=True)

    return corrected_test


#Export data
def export_data(corrected_test):

    '''
    Input: General filepath for saving data
    Output: None
    '''

    #Create output directory
    try:
        os.makedirs('Corrected_test')

    except OSError:
        None 

    corrected_test.to_csv('Corrected_test/corrected_test.csv', index=False)

    return None

#Execute the script
def main():

    
    #Load data
    print("\nLoading data... \n")
    students_answers, answers, subjects_map, students_info = load_data()

    #Transform data
    print("Transforming data... \n")
    corrected_test = correct_test(students_answers, answers)
    corrected_test_full = add_info(subjects_map, students_info, corrected_test) 

    #Export Data
    print("Exporting data... \n")
    export_data(corrected_test_full)


if __name__ == "__main__":
    main()

    
