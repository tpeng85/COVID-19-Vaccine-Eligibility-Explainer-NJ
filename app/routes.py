from typing import Any

from pandas import Series

from app import app
import pandas as pd


current_question_id = 0
previous_questions = {}  # map previous question id to previous answers.
df = pd.read_csv('questions.csv')


def get_cell_contents_from_single_row(row: Series, column_name: str) -> Any:
    return row.iloc[0][column_name]


@app.route('/')
@app.route('/index')
def index():
    current_question_row = df.loc[df['question_id'] == current_question_id]
    current_question_text = get_cell_contents_from_single_row(current_question_row, 'question_text')
    return current_question_text
