from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://dragonball-api.com/api/characters"

# Hàm tìm kiếm nhân vật theo tên
def search_character_by_name(name):
    try:
        response = requests.get(API_URL)
        response.raise_for_status()

        data = response.json()
        characters = data.get("items", [])  # Lấy danh sách nhân vật từ key 'items'

        # Lọc theo tên nếu có nhập
        if name:
            filtered_characters = [char for char in characters if name.lower() in char.get('name', '').lower()]
        else:
            filtered_characters = characters

        return filtered_characters
    except Exception as e:
        print("Lỗi khi gọi API:", e)
        return []

@app.route("/", methods=["GET", "POST"])
def index():
    name = request.form.get("name", "") if request.method == "POST" else ""
    characters = search_character_by_name(name)
    
    error = None
    if not characters:
        error = "Không tìm thấy nhân vật!"

    return render_template("index.html", characters=characters, error=error)

@app.route("/character/<int:id>")
def character_detail(id):
    all_characters = search_character_by_name("")  # Lấy danh sách tất cả nhân vật
    character = next((char for char in all_characters if char.get('id') == id), None)
    
    if character:
        return render_template("character_detail.html", character=character)
    else:
        return "Nhân vật không tìm thấy!", 404

if __name__ == "__main__":
    app.run(debug=True)
