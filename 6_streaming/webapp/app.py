from flask import Flask,jsonify,request
from flask import render_template
# from mpl_toolkits.basemap import Basemap
import geopandas
import ast
app = Flask(__name__)
labels = []
values = []

liberalData = []
conservativeData = []
ndpData = []

@app.route("/")
def get_chart_page():
    print("hi!!")
    global labels,values, liberalData, conservativeData, ndpData
    labels = []
    values = []
    liberalData = []
    conservativeData = []
    ndpData = []
    return render_template('chartTry.html', values=values, labels=labels,
                           liberalData=liberalData, conservativeData=conservativeData, ndpData=ndpData)


@app.route('/refreshData')
def refresh_graph_data():
    global labels,values, liberalData, conservativeData, ndpData
    print("hi!!refresh data")
    # print("labels now: " + str(labels))
    # print("data now: " + str(values))

    print("liberals now: " + str(liberalData))
    print("conservatives now: " + str(conservativeData))
    print("ndp now: " + str(ndpData))

    return jsonify(sLabel=labels, sData=values,
                   liberalData=liberalData, conservativeData=conservativeData, ndpData=ndpData)


@app.route('/updateData', methods=['POST'])
def update_data():
    print("hi!! data")
    global labels,values, liberalData, conservativeData, ndpData
    # if not request.form or 'data' not in request.form:
    #     return "error",400
    # labels = ast.literal_eval(request.form['label'])
    # values = ast.literal_eval(request.form['data'])
    # print("labels received: " + str(labels))
    # print("data received: " + str(values))

    liberalData = ast.literal_eval(request.form['liberal'])
    conservativeData = ast.literal_eval(request.form['conservative'])
    ndpData = ast.literal_eval(request.form['ndp'])
    print("liberals received: " + str(liberalData))
    print("conservatives received: " + str(conservativeData))
    print("ndp received: " + str(ndpData))
    refresh_graph_data()
    return "success",201


if __name__ == "__main__":
    app.run(host='192.168.0.11', port=5001)