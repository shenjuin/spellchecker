"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import FlaskWebProject.views

def autocorrect(word):
    """Checks if input word is in corpus: if not, measures word distance and provides nearest word suggestions (if any)"""
	return word+"s"