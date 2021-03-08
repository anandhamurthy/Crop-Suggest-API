from flask import Flask, jsonify, request
import pickle

filename = 'crop_model.pkl'
model = pickle.load(open(filename, 'rb'))

app = Flask(__name__)

def getDetails(ph_value):
    desc=''
    if ph_value>=6.0 and ph_value<=7.5:
        desc="Your Argiculture Land is ready to grown Crops."
    elif ph_value<6.0:
        desc="Land is Acidic, Some nutrients such as nitrogen, phosphorus, and potassium are less available."
    elif ph_value>7.5:
        desc="Land is very Alkaline, Iron, manganese, and phosphorus are less available."
    return jsonify(
        ph_value=ph_value,
        description=desc
    )

@app.route('/predict/',methods=['GET','POST'])
def predict():
    ph_value=request.args.get('ph_value', type = float)
    temperature=request.args.get('temperature', type = float)
    humidity=request.args.get('humidity', type = float)
    rainfall=request.args.get('rainfall', type = float)
    params = [[ph_value, temperature, humidity, rainfall]]
    return model.predict(params)

if __name__ == '__main__':
    app.run(debug=True)
