from flask import Flask,jsonify,request
from flask import render_template
# from mpl_toolkits.basemap import Basemap
import geopandas
import ast
app = Flask(__name__)
labels = []
values = []
@app.route("/")
def get_chart_page():
    print("hi!!")
    global labels,values
    labels = []
    values = []
    return render_template('chartTry.html', values=values, labels=labels)

if __name__ == "__main__":
    app.run(host='192.168.0.11', port=5001)