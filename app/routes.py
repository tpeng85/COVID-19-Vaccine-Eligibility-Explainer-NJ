from typing import Any

from flask import render_template, request
from pandas import Series, DataFrame

from app import app
import pandas as pd


current_question_id = 0
previous_responses = {}  # map previous question texts to previous answers.
df = pd.read_csv('questions.csv')


def get_cell_contents_from_single_row(row: Series, column_name: str) -> Any:
    return row.iloc[0][column_name]


def get_row_from_question_id(df: DataFrame, question_id: str) -> Series:
    return df.loc[df['question_id'] == question_id]


@app.route('/', methods = ['POST', 'GET'])
def index():
    global current_question_id
    current_question_row = get_row_from_question_id(df, current_question_id)
    current_question_text = get_cell_contents_from_single_row(
        current_question_row, 'question_text')

    if request.method == 'POST':
        assert len(list(request.form.values())) == 1
        user_answer = list(request.form.values())[0] # string "Yes", "No", or "Unsure"
        previous_responses[current_question_text] = user_answer
        current_question_id = get_cell_contents_from_single_row(current_question_row, user_answer + '_response_next')
        # Need to update the other information now that we have a new current question
        if current_question_id < 0:
            # need to exit this loop and immediately go to an ending screen
            return 'hi'
        current_question_row = get_row_from_question_id(df, current_question_id)
        current_question_text = get_cell_contents_from_single_row(
            current_question_row, 'question_text')

    more_information = get_cell_contents_from_single_row(
        current_question_row,
        'more information')
    yes_response_text = get_cell_contents_from_single_row(
        current_question_row,
        'yes_response_text')
    return render_template('index.html',
                           current_question_text=current_question_text,
                           yes_response_text=yes_response_text,
                           more_information=more_information,
                           previous_responses=previous_responses)
