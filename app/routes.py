from typing import Any, List, Tuple

from flask import render_template, request, redirect, make_response, url_for, send_from_directory
from pandas import Series, DataFrame
import json
from app import app
import pandas as pd
import os

questions_df = pd.read_csv('questions.csv')
results_df = pd.read_csv('results.csv')
contact_form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSfI-ozQYUJ1QnrFwuVbKEkK3n-LBke1g0PDkQH_D5fXHXP1UA/viewform?embedded=true'

def get_cell_contents_from_single_row(row: Series, column_name: str) -> Any:
    cell_contents = row.iloc[0][column_name]
    if isinstance(cell_contents, str) and cell_contents == '-':
        cell_contents = ''  # can't have blank cells? not sure what happened here
    return cell_contents


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

def pretty_print_previous_responses(previous_responses):
    # using the browser back/forward arrows to navigate history causes weird things with previous_responses because going back doesn't actually delete the change-- there might be a clean way to fix it but I haven't found anything. Instead, we'll just hack around this by only displaying the most recent possible response for each given question. TODO: maybe worth looking into this.
    question_ids_seen = set()
    responses_to_display = []
    for i, response in enumerate(previous_responses[::-1]):
        question_id, user_answer = response
        if question_id in question_ids_seen:
            # this is an outdated response
            continue
        question_ids_seen.add(question_id)
        question_text = (get_cell_contents_from_single_row(get_row_from_id(questions_df, question_id), 'question_text'))
        responses_to_display.append((question_text, user_answer))
    return responses_to_display[::-1]

def get_questionnaire_template(current_question_id: int, previous_responses: List[Tuple[int, str]]):
    # assumes this survey isn't at a result page, i.e. active_surveys[survey_id].current_question_id isn't negative.
    current_question_text, more_information, yes_response_text = get_current_question_info(current_question_id)

    return render_template('questionnaire.html',
                           current_question_text=current_question_text,
                           yes_response_text=yes_response_text,
                           more_information=more_information,
                           previous_responses=pretty_print_previous_responses(previous_responses),
                           current_question_id=current_question_id,
                           title="COVID-19 vaccine eligibility questionnaire")

@app.route('/restart', methods=['POST'])
def restart():
    resp = make_response(redirect('/'))
    resp.set_cookie('previous_responses', json.dumps([]))
    return resp

@app.route('/questionnaire/<int:current_question_id>', methods = ['POST', 'GET'])
def questionnaire(current_question_id):
    previous_responses = json.loads(request.cookies.get('previous_responses', '[]'))
    if request.method == 'GET':
        resp = make_response(get_questionnaire_template(current_question_id, previous_responses))
        resp.set_cookie('previous_responses', json.dumps(previous_responses))
        return resp
    elif request.method == 'POST':
        user_answer = request.form['user_answer'] # string "Yes", "No", or "Unsure"
        question_row = get_row_from_id(questions_df, current_question_id)
        next_question_id = get_cell_contents_from_single_row(question_row, user_answer + '_response_next')
        if next_question_id < 0:
            return redirect(url_for('result', result_id=next_question_id))
        previous_responses.append((current_question_id, user_answer))
        current_question_id = next_question_id
        resp = make_response(redirect(url_for('questionnaire', current_question_id=current_question_id)))
        resp.set_cookie('previous_responses', json.dumps(previous_responses))  # Ensure that previous responses gets passed along when we send the user to the new page
        return resp

@app.route('/result/<string:result_id>')
def result(result_id):
    result_id = int(result_id)  # string in the url because flask only accepts nonnegative integers: https://github.com/pallets/flask/issues/2643
    result_row = get_row_from_id(results_df, result_id)
    status = get_cell_contents_from_single_row(result_row, 'status')
    more_status_information = get_cell_contents_from_single_row(result_row,
                                                                'More information')
    return render_template('result.html',
                           status=status,
                           more_status_information=more_status_information,
                           title="COVID-19 vaccine eligibility status",
                           contact_form_url=contact_form_url)

@app.route('/')
def index():
    return render_template('index.html', title="Home")

@app.route('/preregister')
def preregister():
    return render_template('preregister.html', title="Preregistration")

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact', contact_form_url=contact_form_url)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')