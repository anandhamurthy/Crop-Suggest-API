from flask import Flask, jsonify, request
import pickle

filename = 'crop_model.pkl'
model = pickle.load(open(filename, 'rb'))

app = Flask(__name__)

def getDetails(predict_list):


    crop_1 = {
        "crop_name": "Rice",
        "crop_image": "https://firebasestorage.googleapis.com/v0/b/project-farmer-5f498.appspot.com/o/Crop_Images%2Fpaddy.jpg?alt=media&token=2a11d45d-fb5f-4aae-acb6-39f41b625a66",
        "probability": predict_list[0],
        "temperature": '20°C to 27°C',
        "irrigation_pattern": 5,
        "growth_period": "120−140 days",
        "disease_model": 'https://crop-disease-predict-api.herokuapp.com/rice/',
        "disease": '1. Bacterial leaf streak, 2. Rice Bacterial blight, 3. Leaf scald, Bakanae, 4. Brown spot, 5. Stem borers, 6. Rice mealy bugs , 7. Rice gall midge, 8. Rice case worm'
    }

    crop_2 = {
        "crop_name": "Maize",
        "crop_image": "https://firebasestorage.googleapis.com/v0/b/project-farmer-5f498.appspot.com/o/Crop_Images%2Fmaize.jpg?alt=media&token=c0696384-0d1b-4b35-8b4b-0e3704ca4a75",
        "probability": predict_list[1],
        "temperature": '21°C to 27°C',
        "irrigation_pattern": 7,
        "growth_period": "90-120 days",
        "disease_model": 'https://crop-disease-predict-api.herokuapp.com/maize/',
        "disease": '1. Anthracnose , 2. Cercospora leaf spot (Gray leaf spot), 3. Charcoal rot, 4. Common rust, 5. Common smut 6. Downy Mildew'
    }

    crop_3 = {
        "crop_name": "Chick Pea",
        "crop_image": "https://firebasestorage.googleapis.com/v0/b/project-farmer-5f498.appspot.com/o/Crop_Images%2Fchickpea.jpg?alt=media&token=3962ffc6-5c64-4e10-a434-9a6abb08aa44",
        "probability": predict_list[2],
        "temperature": 'below 15°C',
        "irrigation_pattern": 7,
        "growth_period": "90-100 days",
        "disease_model": 'None',
        "disease": '1. Fusarium Wilt, 2. Powdery Mildew, 3. White Mold Stem & Crown Rot of Chickpea, 4.	Black Root Rot, 5. Pythium Seedling, 6.	Downy Mildew.Rust'
    }

    crop_4 = {
        "crop_name": "Kidney Beans",
        "crop_image": "https://firebasestorage.googleapis.com/v0/b/project-farmer-5f498.appspot.com/o/Crop_Images%2Fkidneybeans.jpg?alt=media&token=7ee3cff6-01ce-4b7c-bb97-d4cedd50764c",
        "probability": predict_list[3],
        "temperature": '15°C to 25°C',
        "irrigation_pattern": 7,
        "growth_period": "90-150 days",
        "disease_model": 'None',
        "disease": '1. Anthracnose, 2. Rust, 3. Root rot, 4. Bean common mosaic disease, 5.	Watery Soft Rot, 6.	Angular leaf spot'
    }

    crop_5 = {
        "crop_name": "Pigeon Peas",
        "crop_image": "https://firebasestorage.googleapis.com/v0/b/project-farmer-5f498.appspot.com/o/Crop_Images%2Fpigeonpeas.png?alt=media&token=5e2ae6bd-fef5-4026-bc04-514b8f12c231",
        "probability": predict_list[4],
        "temperature": '26°C to 30°C',
        "irrigation_pattern": 7,
        "growth_period": "90-120 days",
        "disease_model": 'None',
        "disease": '1. Alternaria Blight, 2. Anthracnose, 3. Cercospora leaf sopt, 4. White mold, 5. Wilt, 6. Aphids, 7. Army worms'
    }
    response = {
        'status': 200,
        'message': 'OK',
        'crop_1': crop_1,
        'crop_2': crop_2,
        'crop_3': crop_3,
        'crop_4': crop_4,
        'crop_5': crop_5
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
    api_key = request.args.get('api_key', type=str)
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
