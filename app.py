from flask import Flask,request,render_template,jsonify
import os
import io
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
# app.config['GOOGLE_APPLICATION_CREDENTIALS']=r"./fresh-park-426004-b1-d3fd28f9f7ed.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = app.config['GOOGLE_APPLICATION_CREDENTIALS']
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

import base64 
from google.cloud import vision
from google.cloud.vision_v1 import types


import re
def convertfile(textlist):
    
    print("cc",textlist) 
    amountvalues= ["one","two","three","four","five","six","seven","eight","nine", "ten","eleven","twelve","thirteen",
    "fourteen", "fifteen","sixteen","seventeen","eighteen","nineteen","twenty","thirty","forty","fifty","sixty"]
    namelist=[]
    wordamount = None
    date = None
    digitamount = None

    for words in textlist.split("\n"):
        if not words.isdigit() and words.lower() not in amountvalues and not any(char.isdigit() for char in words):
            print("hjdhfdbfhfbhjghju",words)
            namelist.append(words)
        if any(amount in words.lower() for amount in amountvalues):
            wordamount = words.strip()
        if any( d.isdigit() or d == "."  for d in words):
            date = words.strip() 
            break 
    for amountnumber in textlist.split("\n"):
        if any( an.isdigit() or an=="." or an == "," for an in amountnumber):
            for j in amountnumber: 
                if "." in j or "," in j :
                    digitamount = re.sub(r'[^\d.]', '', amountnumber)
    
    print("nl",namelist)
    if len(namelist)==3:
        name= namelist[1] 
    else:
        name= namelist[0]
   
    
    return name, date, wordamount, digitamount

@app.route("/upload", methods=["GET","POST"])
def upload_image():
    textlist = []
    if request.method == "POST":
        data = request.get_json()
        image_data = data['image'].split(",")[1]
        image = vision.Image(content=base64.b64decode(image_data))
        client = vision.ImageAnnotatorClient()
        response = client.text_detection(image=image)
        texts = response.text_annotations
      
    
        if texts:
            for text in texts:
                textlist.append(text.description)
        print("tl",textlist)
        if textlist:
            name, date, wordamount, digitamount = convertfile(textlist[0])
            print("name",name)
            print("date",date) 
            print("wordamount",wordamount) 
            print("digitamount3455",digitamount)
          
            return jsonify({"name": name, "date": date, "wordamount": wordamount, "digitamount": digitamount})
    return render_template("upload.html") 


@app.route("/", methods=["GET","POST"])
def upload():
    textlist = []
    if request.method == "POST": 
        file = request.files['file'] 
        if file: 
            filename = file.filename 
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            client = vision.ImageAnnotatorClient()
            with io.open(file_path, 'rb') as image_file:
                content = image_file.read()

            image = types.Image(content=content)

            
            response = client.text_detection(image=image)
            texts = response.text_annotations
            if texts:
                for text in texts:
                    textlist.append(text.description)
            if textlist:
                name, date, wordamount, digitamount = convertfile(textlist[0])
                print("name",name)
                print("date",date) 
                print("wordamount",wordamount) 
                print("digitamountbbbbb",digitamount)
                return render_template("index.html", date=date, name=name,wordamount=wordamount,amountnumber=digitamount)

    return render_template("index.html")


if __name__=='__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'],exist_ok=True)
    app.run(debug=True)
   