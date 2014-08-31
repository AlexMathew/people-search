from flask import Flask, render_template, request
from scrape import scrape_page


app = Flask(__name__) 


@app.route('/')
def home():
	return render_template('home.html')


@app.route('/search', methods=['POST'])
def search():
	query = str(request.form['query'])
	print query, type(query)
	data = scrape_page(query)
	print data
	return render_template('result.html', data=data)

