from flask import Flask, render_template, session, request, jsonify, Response, flash, redirect, url_for
import requests
import time
from sklearn.metrics import pairwise_kernels
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/allergies')
def allergies():
    return render_template('allergies.html')

@app.route('/allergies_response', methods = ['POST'])
def allergies_response():
    allergy_name = request.form['One']
    recipe_name = request.form['Two']
    ingredient_preferences = request.form['Three']
    edamam_response = requests.get("https://api.edamam.com/search?app_id=6e3a1c55&app_key=979f4ea3d3c1014ffa5de338accf640b")

    url = 'https://api.edamam.com/search?'
    edamam_id = 'app_id=6e3a1c55'
    edamam_key = 'app_key=979f4ea3d3c1014ffa5de338accf640b'
    q = 'q='
    health = 'health='

    allergy_dict = {'peanut': 'peanut-free', 'peanuts': 'peanut-free', 'tree nut': 'tree-nut-free',
                    'dairy': 'dairy-free', 'milk' : 'dairy-free', 'alcohol': 'alcohol-free',
                    'celery' : 'celery-free', 'eggs' : 'egg-free', 'fish' : 'fish-free',
                    'gluten' : 'gluten-free', 'mustard' : 'mustard-free', 'pork' : 'pork-free',
                    'sesame' : 'sesame-free', 'shellfish' : 'shellfish-free', 'soy' : 'soy-free',
                    'tree nuts' : 'tree-nut-free', 'wheat' : 'wheat-free'}

    health_arg = ""
    allergen_found = False
    for key,val in allergy_dict.items():
        if(allergy_name == key):
            health_arg = val
            allergen_found = True

    link = ""
    if allergen_found:
        link = url + q + recipe_name + "&" + edamam_id + "&" + edamam_key + "&" + q + recipe_name + "&" + health + health_arg
    else:
        link = url + q + recipe_name  + "&" + edamam_id + "&" + edamam_key + "&" + q + recipe_name + "&" + "excluded" + "=" + allergy_name

    #print(link)
    x = requests.get(link).json()

    listing = []
    for i in range(0, int(x['to'])):
        listing.append(x['hits'][i]['recipe']['ingredientLines'])

    secondlist = []


    for smalllist in listing:
        xlist = " ".join(smalllist)
        secondlist.append(xlist)

    #print(secondlist)

    if ingredient_preferences == "":

        tfidf_vectorizer=TfidfVectorizer()

        X_train_counts = tfidf_vectorizer.fit_transform(secondlist)
        similarities = cosine_similarity(X_train_counts) 


        final_list = []

        list0 = similarities[0].tolist()

        list1 = similarities[0].tolist()

        list1.sort(reverse = True)

        list3 = []

        for i in range(0,6):
            list3.append(list1[i])

        indices = []

        for element in list3:
            index = list0.index(element)
            indices.append(index)

        #print(indices)


        images = []
        urls = []

        for i in indices:
            images.append(x['hits'][i]['recipe']['image'])
            urls.append(x['hits'][i]['recipe']['url'])

    else:
        
        tokenized_secondlist = [doc.split(" ") for doc in secondlist]
        bm25 = BM25Okapi(tokenized_secondlist)
        tokenized_query = ingredient_preferences.split(" ")
        scores = bm25.get_scores(tokenized_query)
        finalized_list = bm25.get_top_n(tokenized_query, secondlist, n=6)

        indices = []

        for element in finalized_list:
            index = secondlist.index(element)
            indices.append(index)

        
        images = []
        urls = []

        for i in indices:
            images.append(x['hits'][i]['recipe']['image'])
            urls.append(x['hits'][i]['recipe']['url'])



    return render_template('output_recipe.html', images = images, urls = urls)

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