import os
import json
from flask import Flask, request, render_template, send_from_directory, session, flash, redirect, Response
from os import walk
import math

app = Flask(__name__)

app.secret_key = 'Zli6WMDUEboJnp34fzwK'.encode('utf8')

recipes = []
icons = []

search_index = []

@app.route('/icons/<path>')
def send_icons(path):
    return send_from_directory('icons', path)


@app.route('/assets/<path>')
def send_assets(path):
    return send_from_directory('assets', path)

@app.route('/style/<path>')
def send_style(path):
    return send_from_directory('style', path)

@app.route('/js/<path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/version')
def get_version():
    with open('config.json','r') as file:
        data = json.load(file)
        return data["version"]


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
    for recipe in recipes:
        search_index.append(getRecipe(recipe))



@app.route('/search', methods=['GET', 'POST'])
def ajaxSearch():
    if 'limit' in request.args:
        return json.dumps(search(request.args.get("term"), limit=int(request.args.get("limit"))))
    else:
        return json.dumps(search(request.args.get("term")))


@app.route('/add', methods=['GET', 'POST'])
def add_item():
    session['tier'] = 0
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
    session['tier'] = 0
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
        if 'user_items' not in session:
            session['user_items'] = {"oak_wood.json": 420, "redstone.json": 64, "repeater.json": 2,
                                     "sticky_piston.json": 12}
            update_ingredients()
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
            alt_icon_path = "icons/" + path[path.rfind("/") + 1:].replace(".json", "") + "_front.png"
            alt_alt_icon_path = "icons/" + path[path.rfind("/") + 1:].replace(".json", "") + "_side.png"
            icon = icon_path if os.path.exists(icon_path) else (alt_icon_path if os.path.exists(alt_icon_path) else (alt_alt_icon_path if os.path.exists(alt_alt_icon_path) else ""))

            key = data['key'] if 'key' in data else {}
            result = data['result'] if 'result' in data else {}
            pattern = data['pattern'] if 'pattern' in data else []
            ingredients = data['ingredients'] if 'ingredients' in data else (
                [data['ingredient']] if 'ingredient' in data else [])
            count = data['result']['count'] if result and 'count' in data['result'] else 1
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
        alt_icon_path = "icons/" + path[path.rfind("/") + 1:].replace(".json", "") + "_side.png"
        icon = icon_path if os.path.exists(icon_path) else (alt_icon_path if os.path.exists(alt_icon_path) else "")

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
    session['tier'] = 0
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
                amount = eval(amount.replace("x", "*"))
            except:
                print("Found invalid line in import.")
                continue
        session['user_items'][item] = amount
    update_ingredients()
    return compile_all()


def recipe_exists(file):
    return os.path.exists("recipes/" + file)


@app.route('/cata', methods=['GET', 'POST'])
def cata():
    if 'tier' not in session or session['tier'] == 0:
        session['original_list'] = session['user_items'].copy()
        session["tier"] = 0
    if session['user_items'] != session['ingredients']:
        session["tier"] += 1
    session['user_items'] = session['ingredients']
    update_ingredients()
    return compile_all()


@app.route('/ana', methods=['GET', 'POST'])
def ana():
    if 'tier' not in session or session['tier'] == 0:
        session['original_list'] = session['user_items'].copy()
        session["tier"] = 0
        return Response(status=204)
    else:
        session['user_items'] = session['original_list'].copy()
        session["tier"] -= 1
        for i in range(0, session['tier']):
            update_ingredients()
            session['user_items'] = session['ingredients'].copy()

        update_ingredients()
    return compile_all()

@app.route('/ana_complete', methods=['GET', 'POST'])
def ana_complete():
    session['user_items'] = session['original_list'].copy()
    session["tier"] = 0
    update_ingredients()
    return compile_all()


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
                    if len(data["ingredients"]) <= 1:
                        ingKey = 'item' if 'item' in data["ingredients"][0] else 'tag'
                        result = getRecipe("recipes/" + itemToRecipePath(data["ingredients"][0][ingKey]))
                        if result["key"] and len(result["key"]) == 1:
                            valid_continue = False
                            for key in result["key"].keys():
                                if result["key"][key]["item"] == data["result"]["item"]:
                                    if item not in session['ingredients']:
                                        session['ingredients'][item] = session['user_items'][item]
                                    else:
                                        session['ingredients'][item] += session['user_items'][item]
                                    valid_continue = True
                            if valid_continue:
                                continue

                    for ingredient in data["ingredients"]:
                        ingKey = 'item' if 'item' in ingredient else 'tag'
                        recipe_path = itemToRecipePath(ingredient[ingKey])
                        added_value = math.ceil(session['user_items'][item]/data["count"])
                        if recipe_path not in session['ingredients']:
                            session['ingredients'][recipe_path] = added_value
                        else:
                            session['ingredients'][recipe_path] += added_value
                elif data["key"]:
                    keys = {}
                    for key in data["key"].keys():
                        keys[key] = 0
                    for row in data["pattern"]:
                        for character in row:
                            if character in keys:
                                keys[character] += 1

                    for key in keys.keys():
                        recipe_path = ""
                        added_value = keys[key] * math.ceil(math.ceil((keys[key] * session['user_items'][item])/data["count"])/keys[key])
                        if type(data["key"][key]) == dict:
                            ingKey = 'item' if 'item' in data["key"][key] else 'tag'
                            recipe_path = itemToRecipePath(data["key"][key][ingKey])
                        elif type(data["key"][key]) == list:
                            ingKey = 'item' if 'item' in data["key"][key][0] else 'tag'
                            recipe_path = itemToRecipePath(data["key"][key][0][ingKey])
                        if recipe_path not in session['ingredients']:
                            session['ingredients'][recipe_path] = added_value
                        else:
                            session['ingredients'][recipe_path] += added_value
            else:
                if item not in session['ingredients']:
                    session['ingredients'][item] = session['user_items'][item]
                else:
                    session['ingredients'][item] += session['user_items'][item]

@app.route("/last_search", methods=['GET'])
def get_last_search():
    if 'last_search' not in session:
        return ""
    return session['last_search']

@app.route("/show_warning",methods=['GET','POST'])
def warning_status():
    if 'show_warning' not in session:
        session['show_warning'] = True
    elif request.args.get("set") == "show":
        session['show_warning'] = True
    elif request.args.get("set") == "hide":
        session['show_warning'] = False
    return str(session['show_warning'])

@app.route("/tier", methods=['GET'])
def get_tier():
    if 'tier' not in session:
        session['tier'] = 0
    return str(session['tier'])

def search(term, limit=50):
    session['last_search'] = term

    if term == "":
        return []

    output = []
    scores = {}
    for recipe in recipes:
        score = 0
        if term in recipe:
            score += 20
        for s in recipe:
            if s in term:
                score += 1
            else:
                score -= 1
        if score > 0:
            scores[recipe] = score
    scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    i = 0
    for path,score in scores:
        if i > limit:
            break
        output.append(getRecipe(path))
        i += 1
    return output

load_icons()
load_recipes()
load_search_engine()

if __name__ == '__main__':
    app.run(debug=True)
