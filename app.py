from flask import Flask, jsonify
from MatchaScript import scrape_matchas

app = Flask('Matcha_Watch')

@app.route('/matcha', methods=['GET'])
def get_matcha():
    matcha_stock = scrape_matchas()
    return jsonify(matcha_stock)

if __name__ == '__main__':
    app.run(debug=True)