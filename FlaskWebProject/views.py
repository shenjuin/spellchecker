"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import render_template, request, url_for
from FlaskWebProject import app

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
    )
	
@app.route('/check', methods=['POST'])
def check():
	"""Renders the spellcheck result page"""
	word=request.form['word']
	#word=autocorrect(word)
	return render_template(
		'check.html',
		title='Spell Check',
		word=word,
	)

def autocorrect(word):
    """Checks if input word is in corpus: if not, measures word distance and provides nearest word suggestions (if any)"""
	return word+"s"