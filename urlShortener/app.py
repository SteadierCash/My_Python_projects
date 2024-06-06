from flask import Flask, request, redirect, jsonify
import string
import random
import json
import os

app = Flask(__name__)

# File to store URL mappings
STORAGE_FILE = 'url_mappings.json'
BASE_URL = "n.abl/"
MAX_URL = 100

# Load URL mappings from file or initialize an empty dictionary
if os.path.exists(STORAGE_FILE):
    with open(STORAGE_FILE, 'r') as f:
        url_mapping = json.load(f)
else:
    url_mapping = {}


def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


def save_url_mappings():
    with open(STORAGE_FILE, 'w') as f:
        json.dump(url_mapping, f)


def shorten_and_store_url(original_url):
    # Ensure we don't exceed the maximum number of URLs
    if len(url_mapping) >= MAX_URL:
        return None

    short_url = generate_short_url()

    #check if there is no duplicates
    while short_url in url_mapping:
        short_url = generate_short_url()

    url_mapping[short_url] = original_url
    save_url_mappings()

    return BASE_URL + short_url


@app.route('/shorten', methods=['GET'])
def shorten_url():
    original_url = request.args.get('url')
    if not original_url:
        return jsonify({"error": "URL is required"}), 400

    short_url = shorten_and_store_url(original_url)
    if short_url:
        return jsonify({"short_url": short_url}), 200
    else:
        return jsonify({"message": "Insufficient Storage"}), 507


@app.route('/expand', methods=['GET'])
def expand_url():
    short_url = request.args.get('short_url')
    if not short_url:
        return jsonify({"error": "Short URL is required"}), 400

    # Remove base URL part to get the short code
    short_code = short_url.replace(BASE_URL, "")
    original_url = url_mapping.get(short_code)

    if original_url:
        return jsonify({"original_url": original_url}), 200
    else:
        return jsonify({"error": "URL not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
