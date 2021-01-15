from app import app
import pandas as pd

@app.route('/')
@app.route('/index')
def index():
    data = pd.read_csv('questions.csv')
    return str(data)
