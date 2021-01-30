# COVID-19 Vaccine website (New Jersey)

## What is this?

This is a website that publishes where and when you can get a COVID-19 vaccine if you live in New Jersey.

## FAQ

* **Why New Jersey in particular?** Information varies quite a bit state-by-state and I can help the most in New Jersey.

* **I want to help!** If you're building something similar and there's anything I can do to help, please don't hesitate to contact me by opening an issue in this repository, email, etc.

--

## How to run the code

You will need python version 3.8.

* Create the venv: `python3.8 -m venv venv`

* To install from requirements.txt: `pip install -r requirements.txt`

* Activating the environment: `source venv/bin/activate`

* Run `export FLASK_APP=main.py`

* To run the server: `flask run` or `python main.py`

## Updating the requirements.txt file

* `pip freeze > requirements.txt`
