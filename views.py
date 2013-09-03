'''

An HTTP API for querying the status and capture RAMs of
the CTP6

'''

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/reset/<linkstring>')
def reset(linkstring=None):
    pass


@app.route('/status/<linkstring>')
def status(linkstring=None):
    pass
