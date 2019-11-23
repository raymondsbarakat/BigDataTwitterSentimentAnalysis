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
    return render_template('chart.html', values=values, labels=labels)
@app.route('/refreshData')
def refresh_graph_data():
    global labels, values
    print("hi!!refresh data")
    print("labels now: " + str(labels))
    print("data now: " + str(values))
    return jsonify(sLabel=labels, sData=values)
@app.route('/updateData', methods=['POST'])
def update_data():
    print("hi!! data")
    global labels, values
    if not request.form or 'data' not in request.form:
        return "error",400
    labels = ast.literal_eval(request.form['label'])
    values = ast.literal_eval(request.form['data'])
    print("labels received: " + str(labels))
    print("data received: " + str(values))
    refresh_graph_data()
    return "success",201


if __name__ == "__main__":
    app.run(host='192.168.0.11', port=5001)