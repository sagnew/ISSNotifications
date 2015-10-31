import iss

from flask import Flask, request, render_template


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template()


@app.route('/subscribe', methods=['POST'])
def subscribe():
    number = request.form['number']
    lat = request.form['latitude']
    lon = request.form['longitude']
    iss.add_to_queue(number, lat, lon)
    return render_template()

app.run(host='0.0.0.0')
