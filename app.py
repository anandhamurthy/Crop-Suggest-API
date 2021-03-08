from flask import Flask, jsonify, request
import pickle

filename = 'crop_model.pkl'
model = pickle.load(open(filename, 'rb'))

result={'Rice': 1,
 'Maize': 2}

app = Flask(__name__)

def getDetails(crop_id):
    
    return jsonify(
        crop_name=list(result.keys())[crop_id],
        temperature='20 to 27',
        irrigation_pattern='5',
        disease='Bacterial leaf streak, Rice Bacterial blight, Leaf scald, Bakanae, Brown spot, Stem borers, Rice mealy bugs , Rice gall midge, Rice case worm'
    )

@app.route('/predict/',methods=['GET','POST'])
def predict():
    ph_value=request.args.get('ph_value', type = float)
    temperature=request.args.get('temperature', type = float)
    humidity=request.args.get('humidity', type = float)
    rainfall=request.args.get('rainfall', type = float)
    params = [[ph_value, temperature, humidity, rainfall]]
    return getDetails(int(model.predict(params)[0]))

if __name__ == '__main__':
    app.run(debug=True)
