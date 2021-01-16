from typing import Any

from flask import render_template, request, redirect
from pandas import Series, DataFrame

from app import app
import pandas as pd


current_question_id = 0
previous_responses = {}  # map previous question texts to previous answers.
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
    global current_question_id
    current_question_id = 0
    global previous_responses
    previous_responses = {}
    return redirect('/', code=302)


@app.route('/', methods = ['POST', 'GET'])
def questionnaire():
    global current_question_id

    if request.method == 'POST':
        assert len(list(request.form.values())) == 1
        user_answer = list(request.form.values())[0] # string "Yes", "No", or "Unsure"
        # Update the responses so far
        current_question_row = get_row_from_id(questions_df, current_question_id)
        current_question_text = get_cell_contents_from_single_row(
            current_question_row, 'question_text')
        previous_responses[current_question_text] = user_answer
        current_question_id = get_cell_contents_from_single_row(current_question_row, user_answer + '_response_next')
        # Need to update the other information now that we have a new current question
        if current_question_id < 0:
            # need to exit this loop and immediately go to an ending screen
            result_id = current_question_id
            result_row = get_row_from_id(results_df, result_id)
            status = get_cell_contents_from_single_row(result_row, 'status')
            more_status_information = get_cell_contents_from_single_row(result_row, 'More information')
            return render_template('result.html', status=status, more_status_information=more_status_information)

    current_question_text, more_information, yes_response_text = get_current_question_info(current_question_id)
    return render_template('questionnaire.html',
                           current_question_text=current_question_text,
                           yes_response_text=yes_response_text,
                           more_information=more_information,
                           previous_responses=previous_responses)
