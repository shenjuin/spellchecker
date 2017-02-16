"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, url_for, jsonify
from FlaskWebProject import app

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
    )
	
@app.route('/check')
def check():
	"""Renders the addition sum page"""
	word = request.args.get('word', 0, type=string)
	return jsonify(result = word)
	#word=request.form['word']
	#return render_template(
	#	'check.html',
	#	title='Spell Check',
	#	word=word,
	#)