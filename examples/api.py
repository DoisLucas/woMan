from flask import Flask, abort, request, jsonify
import json
import base64
import cvlib as cv
import cv2
import sys
import numpy as np
from resultado_class import resultado_class

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/genderBase64', methods=['POST'])
def toImg():
    if not request.json:
        abort(400)
    content = request.get_json()

    imgdata = base64.b64decode(content['base64'])
    npimg = np.fromstring(imgdata, dtype=np.uint8)

    # Salvar a imagem se necessario
    #filename = 'gerado.jpg'
    # with open(filename, 'wb') as f:
    #    f.write(imgdata)

    img = cv2.imdecode(npimg, 1)
    face, conf = cv.detect_face(img)

    f = face[0]

    (startX, startY) = f[0], f[1]
    (endX, endY) = f[2], f[3]

    cv2.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0), 2)

    face_crop = np.copy(img[startY:endY, startX:endX])

    label, confidence = cv.detect_gender(face_crop)

    # print(confidence)
    # print(label)

    retorno = resultado_class()

    retorno.men = format(confidence[0], '.10f')
    retorno.woman = format(confidence[1], '.10f')

    json_data = json.dumps(retorno.__dict__)

    return json_data, 200
