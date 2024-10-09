import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from MatchaScript import scrape_matchas


app = Flask('Matcha_Watch')
CORS(app ,origins=["https://stkieu.github.io"])

@app.route('/', methods=['GET'])
def get_matcha():
    try:
        matcha_stock = scrape_matchas()
        return jsonify(matcha_stock)
    except Exception as e:
        return jsonify({'error': str(e)}), 500