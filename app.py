import os
from flask import Flask, jsonify
from MatchaScript import scrape_matchas
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask('Matcha_Watch')

@app.route('/matcha', methods=['GET'])
def get_matcha():
    matcha_stock = scrape_matchas()
    return jsonify(matcha_stock)
scheduler = BackgroundScheduler()
scheduler.add_job(scrape_data, 'interval', minutes=1)
scheduler.start()
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)