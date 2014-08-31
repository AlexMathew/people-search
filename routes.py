from flask import Flask, render_template, redirect
from scrape import scrape_page

app = Flask(__name__) 

@app.route('/')
def home():
	return render_template('home.html')

