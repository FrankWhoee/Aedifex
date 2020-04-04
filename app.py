import requests
import os
import json
import datetime
import time
from flask import Flask, request, render_template, send_from_directory, session, flash, redirect, Response
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

app.secret_key = 'Zli6WMDUEboJnp34fzwK'.encode('utf8')

recipes = []
icons = []

schema = Schema(title=TEXT(stored=True), path=ID(stored=True), group=TEXT(stored=True), type=KEYWORD(stored=True),
                icon=ID(stored=True), pattern=STORED, key=STORED, result=STORED, ingredients=STORED,
                count=NUMERIC(stored=True))
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


def itemToRecipePath(item: str):
    return item[item.find(":") + 1:] + ".json"


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
            ingredients = data['ingredients'] if 'ingredients' in data else (
                data['ingredient'] if 'ingredient' in data else "")
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
    if 'user_items' not in session:
        try:
            session['user_items'] = {request.args.get("item"): int(request.args.get("amount"))}
        except:
            session['user_items'] = {request.args.get("item"): 1}
    else:
        try:
            if request.args.get("item") not in session['user_items']:
                session['user_items'][request.args.get("item")] = int(request.args.get("amount"))
            else:
                session['user_items'][request.args.get("item")] += int(request.args.get("amount"))
        except:
            if request.args.get("item") not in session['user_items']:
                session['user_items'][request.args.get("item")] = 1
            else:
                session['user_items'][request.args.get("item")] += 1

    update_ingredients()
    response = {"items": [], "ingredients": []}
    for i in session['user_items'].keys():
        response["items"].append({"data": getRecipe("recipes/" + i), "amount": session['user_items'][i]})
    for i in session['ingredients'].keys():
        response["ingredients"].append({"data": getRecipe("recipes/" + i), "amount": session['ingredients'][i]})
    return json.dumps(response)

@app.route('/delete_all', methods=['GET', 'POST'])
def delete_all_items():
    session['user_items'] = {}
    session['ingredients'] = {}
    return Response(status=204)

def getRecipe(path):
    with open(path) as json_file:
        data = json.load(json_file)
        title = " ".join([x.capitalize() for x in path[path.rfind("/") + 1:].replace(".json", "").split("_")])
        group = data['group'] if 'group' in data else "None"
        type = data['type'] if 'type' in data else "None"

        icon_path = "icons/" + path[path.rfind("/") + 1:].replace(".json", ".png")
        icon = icon_path if os.path.exists(icon_path) else ""

        key = data['key'] if 'key' in data else {}
        result = data['result'] if 'result' in data else {}
        pattern = data['pattern'] if 'pattern' in data else []
        ingredients = data['ingredients'] if 'ingredients' in data else (
            data['ingredient'] if 'ingredient' in data else "")
        count = data['count'] if 'count' in data else -1
        return {
            "title": title,
            "path": path,
            "pattern": pattern,
            "key": key,
            "result": result,
            "group": group,
            "type": type,
            "ingredients": ingredients,
            "count": count,
            "icon": icon,
        }


def update_ingredients():
    session['ingredients'] = {}
    if 'user_items' not in session:
        session['user_items'] = {}
    else:
        session['ingredients'] = {}
        for item in session['user_items'].keys():
            if os.path.exists("recipes/" + item):
                data = getRecipe('recipes/' + item)
                if data["ingredients"] != "":
                    for ingredient in data["ingredients"]:
                        if itemToRecipePath(ingredient['item']) not in session['ingredients']:
                            session['ingredients'][itemToRecipePath(ingredient['item'])] = 1
                        else:
                            session['ingredients'][itemToRecipePath(ingredient['item'])] += 1
                elif data["key"]:
                    keys = {}
                    for key in data["key"].keys():
                        keys[key] = 0
                    for row in data["pattern"]:
                        for character in row:
                            if character in keys:
                                keys[character] += 1

                    for key in keys.keys():
                        print(itemToRecipePath(data["key"][key]["item"]))
                        if itemToRecipePath(data["key"][key]["item"]) not in session['ingredients']:
                            session['ingredients'][itemToRecipePath(data["key"][key]["item"])] = keys[key] * session['user_items'][item]
                        else:
                            session['ingredients'][itemToRecipePath(data["key"][key]["item"])] += keys[key] * session['user_items'][item]
                    print(session['ingredients'])

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
