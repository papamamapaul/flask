from flask import Flask, jsonify, render_template
import os
import requests

app = Flask(__name__)

BASE_URL = "https://railwayapp-strapi-production-25b3.up.railway.app/api"
ITEMS_URL = f"{BASE_URL}/items?populate=categories"
CATEGORIES_URL = f"{BASE_URL}/categories"

@app.route('/')
def index():
    try:
        # Fetch items with their categories
        items_response = requests.get(ITEMS_URL)
        items_response.raise_for_status()
        items_data = items_response.json()
        
        # Get the items with their populated categories
        items = items_data['data']
        
        return render_template('index.html', items=items)
    except requests.RequestException as e:
        return render_template('index.html', items=[], error=str(e))

@app.route('/api/items')
def get_items():
    try:
        response = requests.get(ITEMS_URL)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/categories')
def get_categories():
    try:
        response = requests.get(CATEGORIES_URL)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
