from flask import Flask

app = Flask(__name__)

@app.route('/')
def action_homepage():
    return "Homepage"

@app.route('/page-1/')
def action_page_1():
    return "Page 1"