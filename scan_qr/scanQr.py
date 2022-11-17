import json,base64
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
from flask import Flask,render_template,request

# NOTE: this program have been made to work only in mobile .. if you want it to work with PC you gotta change the JS file (run the program on PC and connect to server through your phone)



CAMERA = cv2.VideoCapture(0)
LOADJSON = json.loads(open("registered.json").read())
DETECTOR = cv2.QRCodeDetector()
app = Flask(__name__)

def decodeImage(image:str):
    return base64.b64decode(image)

def isItOnJson(message):
    try:
        data = message.split(";")
        if (data[2] in LOADJSON["members"]) and f"{data[0]};{data[1]}" == base64.b64decode(data[2]).decode("utf-8"):
            pass
        else:
            raise Exception
        return True
    except Exception as e:
        print("error :",e)
        return False

@app.route("/",methods = ["GET"])
def index():
    return render_template("index.html")

@app.route('/check_qr',methods=['POST','GET'])
def getQR():
    if request.method == "POST":
        try:
            # catch a FRAME and check QR CODE from it
            try:_frame = json.loads(request.get_data().decode("utf-8"))["image"].split("data:image/jpeg;base64,")[1]
            except: _frame = json.loads(request.get_data().decode("utf-8"))["image"]
            print(type(_frame))
            toStore = BytesIO()
            toStore.write(decodeImage(_frame))
            toStore.seek(0)
            frame = np.array(Image.open(toStore))
            values, points,straight = DETECTOR.detectAndDecode(frame)
            print(values)
            if values != "":
                if isItOnJson(values): 
                    print("here a bruh")
                    return "1"
            else:
                raise Exception
        except Exception as e:
            print(e)
            return "0"
    else:
        return "<p> i hate feminists </p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, port=8100, ssl_context='adhoc')