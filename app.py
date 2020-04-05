import os
import json
from flask import Flask, request, render_template, send_from_directory, session, flash, redirect, Response
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from os import walk
import math

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
    item = request.args.get("item")
    amount = request.args.get("amount")
    if 'user_items' not in session:
        try:
            session['user_items'] = {item: int(amount)}
        except Exception as e:
            session['user_items'] = {item: 1}
    else:
        try:
            if item not in session['user_items']:
                session['user_items'][item] = int(amount)
            else:
                session['user_items'][item] += int(amount)
        except ValueError:
            try:
                if item not in session['user_items']:
                    session['user_items'][item] = math.floor(float(amount))
                else:
                    session['user_items'][item] += math.floor(float(amount))
            except:
                if item not in session['user_items']:
                    session['user_items'][item] = 1
                else:
                    session['user_items'][item] += 1

    update_ingredients()
    return compile_all()


@app.route('/remove', methods=['GET', 'POST'])
def remove_item():
    item = request.args.get("item")
    if 'user_items' not in session:
        session['user_items'] = {}
    elif item in session['user_items']:
        session['user_items'].pop(item, None)
    update_ingredients()
    return compile_all()


@app.route('/delete_all', methods=['GET', 'POST'])
def delete_all_items():
    session['user_items'] = {}
    session['ingredients'] = {}
    return Response(status=204)


def compile_all(format: str = 'str', type=None):
    response = {"items": [], "ingredients": []}
    if type == "items" or type is None:
        for i in session['user_items'].keys():
            response["items"].append({"data": getRecipe("recipes/" + i), "amount": session['user_items'][i]})
    if type == "ingredients" or type is None:
        for i in session['ingredients'].keys():
            response["ingredients"].append({"data": getRecipe("recipes/" + i), "amount": session['ingredients'][i]})
    if format != 'str' and format == 'dict':
        return response
    elif format == "str":
        return json.dumps(response)


@app.route('/get', methods=['GET', 'POST'])
def get_all():
    requested_data = request.args.get("type")
    if requested_data is None:
        return compile_all()
    elif requested_data == "items":
        return compile_all(type="items")
    elif requested_data == "ingredients":
        return compile_all(type="ingredients")
    else:
        return Response(status=400)


def getRecipe(path):
    if os.path.exists(path):
        with open(path) as json_file:
            data = json.load(json_file)
            title = " ".join([x.capitalize() for x in path[path.rfind("/") + 1:].replace(".json", "").split("_")])
            group = data['group'] if 'group' in data else "None"
            type = data['type'] if 'type' in data else "None"
            id = path[path.rfind("/") + 1:]
            icon_path = "icons/" + path[path.rfind("/") + 1:].replace(".json", ".png")
            icon = icon_path if os.path.exists(icon_path) else ""

            key = data['key'] if 'key' in data else {}
            result = data['result'] if 'result' in data else {}
            pattern = data['pattern'] if 'pattern' in data else []
            ingredients = data['ingredients'] if 'ingredients' in data else (
                [data['ingredient']] if 'ingredient' in data else [])
            count = data['result']['count'] if result and 'count' in data['result'] else -1
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
                "id": id
            }
    else:
        title = " ".join([x.capitalize() for x in path[path.rfind("/") + 1:].replace(".json", "").split("_")])
        group = "None"
        type = "base_item"

        icon_path = "icons/" + path[path.rfind("/") + 1:].replace(".json", ".png")
        icon = icon_path if os.path.exists(icon_path) else ""
        id = path[path.rfind("/") + 1:]
        key = {}
        result = {}
        pattern = []
        ingredients = []
        count = -1
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
            "id": id
        }


def idToName(id):
    return " ".join([x.capitalize() for x in id[id.rfind("/") + 1:].replace(".json", "").split("_")])


def nametoId(name):
    return "_".join(x.lower() for x in name.split(" ")) + ".json"


@app.route('/import', methods=['POST'])
def import_list():
    data = request.get_data().decode()
    data = data.split("\n")
    delete_all_items()
    for line in data:
        item = nametoId(line[0:line.find("[")].strip())
        amount = line[line.find("[") + 1: line.rfind("]")]
        try:
            amount = int(amount)
        except:
            try:
                amount = eval(amount.replace("x","*"))
            except:
                print("Found invalid line in import.")
                continue
        session['user_items'][item] = amount
    update_ingredients()
    return compile_all()


def recipe_exists(file):
    return os.path.exists("recipes/" + file)


def update_ingredients():
    session['ingredients'] = {}
    if 'user_items' not in session:
        session['user_items'] = {}
    else:
        session['ingredients'] = {}
        for item in session['user_items'].keys():
            if os.path.exists("recipes/" + item):
                data = getRecipe('recipes/' + item)
                if data["ingredients"]:
                    for ingredient in data["ingredients"]:
                        try:
                            if itemToRecipePath(ingredient['item']) not in session['ingredients']:
                                session['ingredients'][itemToRecipePath(ingredient['item'])] = session['user_items'][
                                    item]
                            else:
                                session['ingredients'][itemToRecipePath(ingredient['item'])] += session['user_items'][
                                    item]
                        except KeyError:
                            if itemToRecipePath(ingredient['tag']) not in session['ingredients']:
                                session['ingredients'][itemToRecipePath(ingredient['tag'])] = session['user_items'][
                                    item]
                            else:
                                session['ingredients'][itemToRecipePath(ingredient['tag'])] += session['user_items'][
                                    item]
                elif data["key"]:
                    keys = {}
                    for key in data["key"].keys():
                        keys[key] = 0
                    for row in data["pattern"]:
                        for character in row:
                            if character in keys:
                                keys[character] += 1

                    for key in keys.keys():
                        ingKey = 'item' if 'item' in data["key"][key] else 'tag'
                        if itemToRecipePath(data["key"][key][ingKey]) not in session['ingredients']:
                            session['ingredients'][itemToRecipePath(data["key"][key][ingKey])] = keys[key] * \
                                                                                                 session['user_items'][
                                                                                                     item]
                        else:
                            session['ingredients'][itemToRecipePath(data["key"][key][ingKey])] += keys[key] * \
                                                                                                  session['user_items'][
                                                                                                      item]
            else:
                if item not in session['ingredients']:
                    session['ingredients'][item] = session['user_items'][item]
                else:
                    session['ingredients'][item] += session['user_items'][item]


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
