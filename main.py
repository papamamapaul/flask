from flask import Flask, jsonify, render_template
import os
import requests

app = Flask(__name__)

STRAPI_URL = "https://railwayapp-strapi-production-25b3.up.railway.app/api/gifts"

@app.route('/')
def index():
    try:
        response = requests.get(STRAPI_URL)
        response.raise_for_status()
        gifts_data = response.json()
        # The gifts are directly in the data array
        gifts = gifts_data['data']
        return render_template('index.html', gifts=gifts)
    except requests.RequestException as e:
        return render_template('index.html', gifts=[], error=str(e))

@app.route('/api/gifts')
def get_gifts():
    try:
        response = requests.get(STRAPI_URL)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
