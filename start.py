from flask import Flask, render_template, session, request, jsonify, Response, flash, redirect, url_for
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/allergies')
def allergies():
    return render_template('allergies.html')

@app.route('/recipes')
def recipes():
    return render_template('recipes.html')

@app.route('/signing')
def signing():
    return render_template('signing.html')

@app.route('/product')
def product():
    return render_template('product.html')

if __name__ == '__main__':
    app.run()