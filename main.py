from flask import Flask, render_template, jsonify, request, Response, redirect, url_for
from pymongo import MongoClient, DESCENDING
import csv
from io import StringIO
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'your_secret_key'

mongo_uri = 'mongodb+srv://rafyeffendy772:65798834@jumpheightrecord.tlt343i.mongodb.net/'
database_name = 'test'
collection_name = 'revisi' 

client = MongoClient(mongo_uri)
db = client[database_name]
revisi_collection = db[collection_name]  

def insert_ultrasonic_data(visual_data, sensor_data):
    timestamp = datetime.utcnow()
    revisi_collection.insert_one({
        'UltrasonicVisualData': visual_data,
        'UltrasonicSensorData': sensor_data,
        'timestamp': timestamp
    })
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/insert_ultrasonic_data', methods=['POST'])
def insert_ultrasonic_data_route():
    visual_data = request.form.get('UltrasonicVisualData')
    sensor_data = request.form.get('UltrasonicSensorData')

    if visual_data is not None and sensor_data is not None:
        if insert_ultrasonic_data(visual_data, sensor_data):
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to insert data'}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Invalid input data'}), 400

@app.route('/get_ultrasonic_data')
def get_ultrasonic_data():
    try:
        data = list(revisi_collection.find({}, {'_id': 0, 'UltrasonicVisualData': 1, 'UltrasonicSensorData': 1, 'timestamp': 1}).sort('timestamp', DESCENDING))
        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/delete_data', methods=['POST'])
def delete_data():
    revisi_collection.delete_many({})
    return jsonify({'status': 'success', 'message': 'Data deleted successfully'})

@app.route('/export_data')
def export_data():
    si = StringIO()
    cw = csv.writer(si)
    data_cursor = revisi_collection.find({})
    data_list = list(data_cursor)
    cw.writerow([str(key) for key in data_list[0].keys()])

    if data_list:
        cw.writerow(data_list[0].keys())
        for item in data_list:
            cw.writerow([str(value).replace(',', ';') for value in item.values()])        
        output = si.getvalue()
        si.close()
        return Response(
            output,
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=jump_data.csv"})
    else:
        return "Tidak ada data yang tersedia", 404  
    
@app.route('/tohistory')
def tohistory():
    return redirect(url_for('history'))

@app.route('/toindex')
def toindex():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='192.168.169.1', port=5000)
