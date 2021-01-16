# COVID-19 Vaccine Phase Explainer website (New Jersey)

## What is this?

This is a website that makes it easier to learn when you can get a COVID-19 vaccine if you live in New Jersey.

The New Jersey [website](https://covid19.nj.gov/index.html) for COVID-19 tells us how the phased rollout for the vaccine works. Everybody who is 16 years or older is part of a phase. Some phases get vaccines before others. However, it's not easy to learn what phase you're in. Right now, the only way to find out your phase is to either read a [long website](https://covid19.nj.gov/faqs/nj-information/slowing-the-spread/who-is-eligible-for-vaccination-in-new-jersey-who-is-included-in-the-vaccination-phases) with lots of words or fill out a [long form](https://covidvaccine.nj.gov/) with lots of ways to accidentally make mistakes.

To make it easier, I made this website so you can quickly find the vaccine rollout information you need. You just need to answer a few short yes-or-no questions to find out. No sign-up, no login, no runaround, no complicated words.

## FAQ

* **Why New Jersey in particular?** I wasn't sure how complicated this is going to be and I can most easily get information for New Jersey. I want the information to be as accurate as possible (or else it'd be less helpful than what we already have), so I plan on focusing specifically on NJ for now.

* **I want to help!** If you're building something similar and there's anything I can do to help, please don't hesitate to contact me by opening an issue in this repository, email, etc.

--


Create the venv: `python3.8 -m venv venv`

Activating the environment: `source venv/bin/activate`

When in the environment:

* Run `export FLASK_APP=main.py`

* To run the server: `flask run` or `python main.py`

* To update requirements file: `pip freeze > requirements.txt`

* To install from requirements.txt: `pip install -r requirements.txt`
