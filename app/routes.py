from typing import Any

from flask import render_template, request, redirect
from pandas import Series, DataFrame
import uuid
from app import app
import pandas as pd

class SurveyState():
    # Maybe there's something involving sessions but I'm not too familiar with how it works. TODO: ??
    def __init__(self):
        self.current_question_id = 0
        self.previous_responses = {}  # map previous question texts to previous answers.

active_surveys = {}  # map string version of uuid4s to SurveyState objects
questions_df = pd.read_csv('questions.csv')
results_df = pd.read_csv('results.csv')

def get_cell_contents_from_single_row(row: Series, column_name: str) -> Any:
    return row.iloc[0][column_name]


def get_row_from_id(df: DataFrame, id: int) -> Series:
    return df.loc[df['id'] == id]


def get_current_question_info(current_question_id: int):
    # Returns a tuple (current_question_text, more_information, yes_response_text) for the current question
    current_question_row = get_row_from_id(questions_df, current_question_id)
    current_question_text = get_cell_contents_from_single_row(
        current_question_row, 'question_text')
    more_information = get_cell_contents_from_single_row(
        current_question_row,
        'more information')
    yes_response_text = get_cell_contents_from_single_row(
        current_question_row,
        'yes_response_text')
    return (current_question_text, more_information, yes_response_text)


@app.route('/restart', methods=['POST'])
def restart():
    survey_id = request.form['survey_id']
    global active_surveys
    del active_surveys[survey_id]
    return redirect('questionnaire')

@app.route('/questionnaire', methods = ['POST', 'GET'])
def questionnaire():
    global active_surveys
    # only the first request to start the survey will be a GET request-- everything after will be POST
    if request.method == 'GET':
        survey_id = str(uuid.uuid4())
        active_surveys[survey_id] = SurveyState()
    elif request.method == 'POST':
        survey_id = request.form['survey_id']
    current_survey_object = active_surveys[survey_id]

    if request.method == 'POST':
        # Update the responses so far
        current_question_row = get_row_from_id(questions_df, current_survey_object.current_question_id)
        current_question_text = get_cell_contents_from_single_row(
            current_question_row, 'question_text')
        user_answer = request.form['user_answer'] # string "Yes", "No", or "Unsure"
        current_survey_object.previous_responses[current_question_text] = user_answer
        current_survey_object.current_question_id = get_cell_contents_from_single_row(current_question_row, user_answer + '_response_next')
        if current_survey_object.current_question_id < 0:
            # need to exit this loop and immediately go to an ending screen
            result_id = current_survey_object.current_question_id
            result_row = get_row_from_id(results_df, result_id)
            status = get_cell_contents_from_single_row(result_row, 'status')
            more_status_information = get_cell_contents_from_single_row(result_row, 'More information')
            return render_template('result.html', status=status, more_status_information=more_status_information, survey_id=survey_id)

    current_question_text, more_information, yes_response_text = get_current_question_info(current_survey_object.current_question_id)
    return render_template('questionnaire.html',
                           current_question_text=current_question_text,
                           yes_response_text=yes_response_text,
                           more_information=more_information,
                           previous_responses=current_survey_object.previous_responses,
                           survey_id=survey_id)

@app.route('/')
def index():
    return render_template('index.html')
