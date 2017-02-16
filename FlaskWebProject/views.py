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
	
@app.route('/add', methods=['POST'])
def add():
	"""Renders the addition sum page"""
	a=request.form['int_a']
	b=request.form['int_b']
	c=a+b
	return render_template(
		'add.html',
		title='Addition',
		a=a,
		b=b,
		sum=c,
	)