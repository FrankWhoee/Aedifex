import requests
import os
import json
import datetime
import time
from flask import Flask, request, render_template, send_from_directory, session, flash, redirect
from flask_wtf import FlaskForm
from whoosh.query import Every
from wtforms import SelectMultipleField, TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired
from os import environ
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from os import walk

app = Flask(__name__)

recipes = []
icons = []

schema = Schema(title=TEXT(stored=True), path=ID(stored=True), group=TEXT(stored=True), type=KEYWORD(stored=True),
                icon=ID(stored=True), pattern=STORED, key=STORED, result=STORED, ingredients=STORED, count=NUMERIC(stored=True))
if not os.path.exists("whoosh"):
    os.mkdir("whoosh")
ix = create_in("whoosh", schema)


@app.route('/icons/<path>')
def send_icons(path):
    return send_from_directory('icons', path)


@app.route('/assets/<path>')
def send_assets(path):
    return send_from_directory('assets', path)


@app.route('/')
def index():
    return render_template("index.html")


def load_recipes():
    for (dirpath, dirnames, filenames) in walk("recipes"):
        recipes.extend(filenames)
        break


def load_icons():
    for (dirpath, dirnames, filenames) in walk("icons"):
        icons.extend(filenames)
        break

def load_search_engine():
    writer = ix.writer()
    for recipe in recipes:
        with open('recipes/' + recipe) as json_file:
            data = json.load(json_file)
            group = data['group'] if 'group' in data else "None"
            type = data['type'] if 'type' in data else "None"

            icon_path = "icons/" + recipe.replace(".json", ".png")
            icon = icon_path if os.path.exists(icon_path) else ""

            key = data['key'] if 'key' in data else {}
            result = data['result'] if 'result' in data else {}
            pattern = data['pattern'] if 'pattern' in data else []
            ingredients = data['ingredients'] if 'ingredients' in data else (data['ingredient'] if 'ingredient' in data else "")
            count = data['count'] if 'count' in data else -1
        writer.add_document(title=" ".join([x.capitalize() for x in recipe.replace(".json", "").split("_")]),
                            path=recipe, pattern=pattern, key=key, result=result, group=group, type=type,
                            ingredients=ingredients, count=count, icon=icon)
    writer.commit()

@app.route('/search', methods=['GET', 'POST'])
def ajaxSearch():
    return json.dumps(search(request.args.get("term")))

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    item = request.args.get("item")
    amount = request.args.get("amount")
    if 'user_items' not in session:
        session['user_items'] = [{'item': item, 'amount':amount}]
    else:
        session['user_items'].append({'item': item, 'amount':amount})

def search(term):
    output = []
    with ix.searcher() as searcher:
        query = QueryParser("title", ix.schema).parse(term)
        results = searcher.search(query, limit=100)
        for result in results:
            output.append({
                "title": result['title'],
                "path": result['path'],
                "pattern": result['pattern'],
                "key": result['key'],
                "result": result['result'],
                "group": result['group'],
                "type": result['type'],
                "ingredients": result['ingredients'],
                "count": result['count'],
                "icon": result['icon'],
            })
    return output


if __name__ == '__main__':
    load_icons()
    load_recipes()
    load_search_engine()
    app.run(debug=True)
