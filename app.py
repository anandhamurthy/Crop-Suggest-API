from flask import Flask, jsonify
import pickle
import werkzeug
import flask
import scipy.misc
from PIL import Image

filename = 'ph_model.pkl'
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

@app.route('/',methods=['GET','POST'])
def predict():
    imagefile = flask.request.files['image0']
    filename = werkzeug.utils.secure_filename(imagefile.filename)
    print("\nReceived image File name : " + imagefile.filename)
    imagefile.save(filename)
    im = Image.open(filename)
    immat = im.load()
    (X, Y) = im.size
    l=[]
    avg=0
    x,y=X-(X//2),Y-(Y//2)
    l.append([x,y])
    l.append([x-(X//2)//2,y-(Y//2)//2])
    l.append([x+(X//2)//2,y-(Y//2)//2])
    l.append([x-(X//2)//2,y+(Y//2)//2])
    l.append([x+(X//2)//2,y+(Y//2)//2])
    image_rgb = im.convert("RGB")
    for i in l:
        rgb_pixel_value = image_rgb.getpixel((i[0],i[1]))
        avg+=model.predict([[rgb_pixel_value[0],rgb_pixel_value[1],rgb_pixel_value[2]]])
    return getDetails((avg/5)[0])

if __name__ == '__main__':
    app.run(debug=True)
