import os
from flask import Flask, jsonify
from flask_cors import CORS
from MatchaScript import scrape_matchas


app = Flask('Matcha_Watch')
CORS(app ,origins=["https://stkieu.github.io"])

@app.route('/matcha', methods=['GET'])
def get_matcha():
    matcha_stock = scrape_matchas()
    return jsonify(matcha_stock)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)