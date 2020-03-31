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

schema = Schema(title=TEXT(stored=True), path=ID(stored=True), group=TEXT(stored=True), type=KEYWORD(stored=True), icon=ID(stored=True), pattern=STORED, key=STORED, result=STORED)
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
            print(recipe)
            group = data['group'] if 'group' in data else "None"
            type = data['type'] if 'type' in data else "None"
            icon_path = "icons/" + recipe.replace(".json",".png")
            icon = icon_path if os.path.exists(icon_path) else ""
            key = data['key'] if 'key' in data else "None"
            result = data['result']
            pattern = data['pattern']
        writer.add_document(title=" ".join([x.capitalize() for x in recipe.replace(".json", "").split("_")]),
                            path=recipe, pattern=pattern, key=key, result=result, group=group, type=type)
    writer.commit()


def search(term):
    output = []
    with ix.searcher() as searcher:
        query = QueryParser("title", ix.schema).parse(term)
        results = searcher.search(query, limit=100)
        for result in results:
            output.append({
                "title": result['title'],
                "path": result['path'],
                "group": result['group'],
                "type": result['type']
            })
    return output


if __name__ == '__main__':
    load_icons()
    load_recipes()
    load_search_engine()
    print(search("boat"))
    # app.run(debug=True)
