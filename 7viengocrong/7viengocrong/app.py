from flask import Flask, render_template, request
import requests
from urllib.parse import unquote

app = Flask(__name__)
API_URL = "https://dragonball-api.com/api/characters"

# Hàm lấy nhân vật theo tên (dành cho index)
def search_character_by_name(name):
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        characters = data.get("items", [])
        if name:
            return [char for char in characters if name.lower() in char.get('name', '').lower()]
        return characters
    except Exception as e:
        print("Lỗi khi gọi API:", e)
        return []

# Trang chủ tìm kiếm
@app.route("/", methods=["GET", "POST"])
def index():
    name = request.form.get("name", "") if request.method == "POST" else ""
    characters = search_character_by_name(name)
    error = "Không tìm thấy nhân vật!" if not characters else None
    return render_template("index.html", characters=characters, error=error)

# Trang chi tiết nhân vật
@app.route("/character/<int:id>")
def character_detail(id):
    try:
        response = requests.get(f"{API_URL}/{id}")
        response.raise_for_status()
        character = response.json()
        return render_template("character_detail.html", character=character)
    except Exception as e:
        print("Lỗi khi gọi API:", e)
        return "Không tìm thấy nhân vật!", 404

# Trang chi tiết transformation
@app.route("/character/<int:character_id>/transformation/<trans_name>")
def transformation_detail(character_id, trans_name):
    try:
        response = requests.get(f"{API_URL}/{character_id}")
        response.raise_for_status()
        character = response.json()
        transformations = character.get("transformations", [])
        trans_name = unquote(trans_name).lower()
        transformation = next((t for t in transformations if t['name'].lower() == trans_name), None)

        if transformation:
            return render_template("transformation_detail.html", transformation=transformation, character=character)
        return "Không tìm thấy transformation!", 404
    except Exception as e:
        print("Lỗi:", e)
        return "Lỗi khi lấy dữ liệu!", 500

if __name__ == "__main__":
    app.run(debug=True)
