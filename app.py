from flask import Flask, jsonify, request
import pickle

filename = 'crop_model.pkl'
model = pickle.load(open(filename, 'rb'))

app = Flask(__name__)

def getDetails(predict_list):
    crop_1 = {
        "crop_name": "Rice",
        "probability": predict_list[0],
        "temperature": '20 to 27',
        "irrigation_pattern": '5',
        "disease": 'Bacterial leaf streak, Rice Bacterial blight, Leaf scald, Bakanae, Brown spot, Stem borers, Rice mealy bugs , Rice gall midge, Rice case worm'
    }

    crop_2 = {
        "crop_name": "Maize",
        "probability": predict_list[1],
        "temperature": '20 to 27',
        "irrigation_pattern": '5',
        "disease": 'Bacterial leaf streak, Rice Bacterial blight, Leaf scald, Bakanae, Brown spot, Stem borers, Rice mealy bugs , Rice gall midge, Rice case worm'
    }
    response = {
        'status': 200,
        'message': 'OK',
        'crop_1': crop_1,
        'crop_2': crop_2
    }
    return jsonify(response)

@app.route('/predict/',methods=['GET','POST'])
def predict():
    ph_value=request.args.get('ph_value', type = float)
    temperature=request.args.get('temperature', type = float)
    humidity=request.args.get('humidity', type = float)
    rainfall=request.args.get('rainfall', type = float)
    params = [[ph_value, temperature, humidity, rainfall]]

    return getDetails(model.predict_proba(params)[0])

@app.route('/predict_alerts/',methods=['GET','POST'])
def predict_alerts():
    api_key = request.args.get('api_key', type=int)
    longitude = request.args.get('lon', type=float)
    latitude = request.args.get('lat', type=float)
    response = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat='+latitude+'&lon='+longitude+'&exclude=hourly,current,minutely&appid='+api_key)
    data = response.json()
    daily = list(data['daily'])
    rain_ids = [500, 501, 502, 503, 504, 511, 520, 521, 522, 531]
    drizzle_ids = [300, 301, 302, 310, 311, 312, 313, 314, 321]
    alerts = []
    for i in daily:
        if i['weather'][0]['id'] in rain_ids + drizzle_ids:
            alert = {"dt": i['dt'],
                     "alert": "There is a " + str(i['weather'][0]['description']).capitalize() + ". You can avoid Irrigating Crops!"}
            alerts.append(alert)
    response = {
        'status': 200,
        'message': 'OK',
        'alerts': alerts
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
