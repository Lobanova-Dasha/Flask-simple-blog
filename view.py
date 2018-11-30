from app import app
from flask import render_template


#root of website, 2 level domen
@app.route('/')
def index():
    name = 'Dasha'
    return render_template('index.html', name=name)