from flask import Flask, jsonify
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

@app.route('/predict/<msg>',methods=['GET','POST'])
def predict(msg):
    l=msg.split(',')
    params = [[l[0], l[1], l[2], l[3]]]
    return model.predict(params)

if __name__ == '__main__':
    app.run(debug=True)
