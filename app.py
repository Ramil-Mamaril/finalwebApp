import pyrebase
from flask import Flask, render_template, request, redirect,url_for
from keras.models import load_model
import numpy as np
import os
import librosa
import json
import math

app = Flask(__name__)


model = load_model("model/Revised_Model_MFCC.h5")

with open("json/violin_MFCC.json", "r") as fp:
    data = json.load(fp)
    z = np.array(data['mapping'])


config = {
    'apiKey': "AIzaSyB9A21cBJPo35akpKEWKSKY6HsPTbNli7s",
    'authDomain': "finalwebapp-862ca.firebaseapp.com",
    'projectId': "finalwebapp-862ca",
    'storageBucket': "finalwebapp-862ca.appspot.com",
    'messagingSenderId': "914428481741",
    'appId': "1:914428481741:web:3f67c944b88f3d97029984",
    'databaseURL': 'https://finalwebapp-862ca-default-rtdb.firebaseio.com/'
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
storage = firebase.storage()
db = firebase.database()
person = {"is_logged_in": False, "name": "","lastname":"", "email": "", "uid": "", "image": "","technique":"","predicted":"","predicted1":"","predicted2":"","predicted3":"","predicted4":"","percent":"","percent1":"","percent2":"","percent3":"","percent4":""}
gUid = ""

@app.route('/')
def land():
    person["is_logged_in"] = False
    print(person["is_logged_in"])
    return render_template('/land.html')


@app.route('/login',methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        result = request.form
        email = result['email']
        password = result['password']

        try:
            # Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            # Insert the user data in the global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            # Get the name of the user
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            gUid = data.val()[person["uid"]]
            #person["image"] = data.val()[person["uid"]]["image"]
            # Redirect to welcome page
            return redirect(url_for('landingpage'))
        except:
            unsuccessful = 'You have entered an invalid email or password'
            return render_template('login.html', umessage=unsuccessful)
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('landingpage'))
        else:
            return render_template('login.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if (request.method == 'POST'):
        result = request.form
        email = result['email']
        password = result['password']
        name= result['username']
        lastname = result['lname']
        image = "static/img/default.png"
        try:
            # Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            # Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            # Add data to global person
            print(image)
            global person
            person['is_logged_in'] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            person["image"]= image
            person["lastname"] =lastname
            storage.child("users").child(person["uid"]).put(image)
            imageUrl = storage.child("users").child(person["uid"]).get_url(person["uid"])
            data = {"name": name,"lastname":lastname, "email": email,"image":imageUrl}
            predData={"predicted":"","predicted1":"","predicted2":"","predicted3":"","predicted4":"","percent":"","percent1":"","percent2":"","percent3":"","percent4":"","technique":""}
            db.child("users").child(person["uid"]).set(data)
            db.child("users").child(person["uid"]).child("Detache").set(predData)
            db.child("users").child(person["uid"]).child("Portato").set(predData)
            db.child("users").child(person["uid"]).child("Legato").set(predData)
            db.child("users").child(person["uid"]).child("SonFile").set(predData)
            db.child("users").child(person["uid"]).child("Chord").set(predData)
            return redirect(url_for('login'))
        except:
            unsuccessful = 'account already exist'
            return render_template('login.html', umessage=unsuccessful)
    else:
        if person["is_logged_in"] == True:
            return render_template("landingpage.html")
        else:
            return  render_template("login.html")



       # user = auth.create_user_with_email_and_password(email, password)
       # newUser = (user['localId'])
       # db.child(newUser).push(username)
        #return render_template('login.html')
    #return render_template('register.html')

@app.route('/update',methods=['GET', 'POST'])
def update():
    if (request.method == 'POST'):
        result = request.form
        name = result['username']
        lastname =result['lastname']
        try:
            # Add data to global person
            global person
            person['is_logged_in'] = True
            person["name"] = name
            person["lastname"] = lastname

            data = {"name": name, "lastname": lastname}
            db.child("users").child(person["uid"]).update(data)
            return redirect(url_for('landingpage'))
        except:
            unsuccessful = 'error'
            return render_template('update.html', umessage=unsuccessful)
    else:
        if person["is_logged_in"] == True:
            person["uid"] = person["uid"]
            data = db.child("users").get()
            person["image"] = data.val()[person["uid"]]["image"]
            return render_template("update.html",name=person["name"],image=person["image"])
        else:
            return render_template("update.html")
@app.route('/profileupdate',methods=['GET', 'POST'])
def profileupdate():
    if (request.method == 'POST'):
        image = request.files["avatar"]
        try:
            # Add data to global person
            global person
            person['is_logged_in'] = True
            print(image)
            storage.child("users").child(person["uid"]).put(image)
            imageUrl = storage.child("users").child(person["uid"]).get_url(person["uid"])
            print(imageUrl)
            data = {"image": imageUrl}
            db.child("users").child(person["uid"]).update(data)
            return redirect(url_for('landingpage'))
        except:
            unsuccessful = 'error'
            return render_template('update.html', umessage=unsuccessful)
    else:
        if person["is_logged_in"] == True:
            return render_template("update.html",email = person["email"] ,name = person["name"])
        else:
            return render_template("update.html")

@app.route('/landingpage')
def landingpage():
    global person
    person["is_logged_in"] = True
    person["uid"] = person["uid"]
    # Get the name of the user
    print(person["uid"])
    data = db.child("users").get()
    person["image"] = data.val()[person["uid"]]["image"]
    print(person["image"])
    return render_template("landingpage.html",email = person["email"] ,name = person["name"],image=person["image"])


@app.route('/technique')
def technique():
    global person
    person["is_logged_in"] = True
    person["uid"] = person["uid"]
    # Get the name of the user
    print(person["uid"])
    data = db.child("users").get()
    person["image"] = data.val()[person["uid"]]["image"]
    print(person["image"])
    return render_template("technique.html", email=person["email"], name=person["name"],image=person["image"])

@app.route('/profile')
def profile():
    person["is_logged_in"] = True
    person["uid"] = person["uid"]
    person["name"] = person["name"]
    person["lastname"]=person["lastname"]
    person["email"] = person["email"]
    person["percent"] = person["percent"]
    person["percent1"] = person["percent1"]
    person["percent2"] = person["percent2"]
    person["percent3"] = person["percent3"]
    person["percent4"] = person["percent4"]
    person["predicted"] = person["predicted"]
    person["predicted1"] = person["predicted1"]
    person["predicted2"] = person["predicted2"]
    person["predicted3"] = person["predicted3"]
    person["predicted4"] = person["predicted4"]


    # Get the name of the user

    data = db.child("users").get()
    person["image"] = data.val()[person["uid"]]["image"]
    #DETACHE
    predictData = db.child("users").child(person["uid"]).child("Detache").get()
    dpredict = predictData.val()["predicted"]
    dpredict1 = predictData.val()["predicted1"]
    dpredict2 = predictData.val()["predicted2"]
    dpredict3 = predictData.val()["predicted3"]
    dpredict4  = predictData.val()["predicted4"]
    dpercent = predictData.val()["percent"]
    dpercent1 = predictData.val()["percent1"]
    dpercent2 = predictData.val()["percent2"]
    dpercent3 = predictData.val()["percent3"]
    dpercent4 = predictData.val()["percent4"]
    dtechnique = predictData.val()["technique"]
    technique = (person["technique"])
    # Chord
    predictData1 = db.child("users").child(person["uid"]).child("Chord").get()
    cpredict = predictData1.val()["predicted"]
    cpredict1 = predictData1.val()["predicted1"]
    cpredict2 = predictData1.val()["predicted2"]
    cpredict3 = predictData1.val()["predicted3"]
    cpredict4 = predictData1.val()["predicted4"]
    cpercent = predictData1.val()["percent"]
    cpercent1 = predictData1.val()["percent1"]
    cpercent2 = predictData1.val()["percent2"]
    cpercent3 = predictData1.val()["percent3"]
    cpercent4 = predictData1.val()["percent4"]
    ctechnique = predictData1.val()["technique"]

    # portato
    predictData2 = db.child("users").child(person["uid"]).child("Portato").get()
    ppredict = predictData2.val()["predicted"]
    ppredict1 = predictData2.val()["predicted1"]
    ppredict2 = predictData2.val()["predicted2"]
    ppredict3 = predictData2.val()["predicted3"]
    ppredict4 = predictData2.val()["predicted4"]
    ppercent = predictData2.val()["percent"]
    ppercent1 = predictData2.val()["percent1"]
    ppercent2 = predictData2.val()["percent2"]
    ppercent3 = predictData2.val()["percent3"]
    ppercent4 = predictData2.val()["percent4"]
    ptechnique = predictData2.val()["technique"]

    # Legato
    predictData3 = db.child("users").child(person["uid"]).child("Legato").get()
    lpredict = predictData3.val()["predicted"]
    lpredict1 = predictData3.val()["predicted1"]
    lpredict2 = predictData3.val()["predicted2"]
    lpredict3 = predictData3.val()["predicted3"]
    lpredict4 = predictData3.val()["predicted4"]
    lpercent = predictData3.val()["percent"]
    lpercent1 = predictData3.val()["percent1"]
    lpercent2 = predictData3.val()["percent2"]
    lpercent3 = predictData3.val()["percent3"]
    lpercent4 = predictData3.val()["percent4"]
    ltechnique = predictData3.val()["technique"]

    # SONFILE
    predictData4 = db.child("users").child(person["uid"]).child("SonFile").get()
    spredict = predictData4.val()["predicted"]
    spredict1 = predictData4.val()["predicted1"]
    spredict2 = predictData4.val()["predicted2"]
    spredict3 = predictData4.val()["predicted3"]
    spredict4 = predictData4.val()["predicted4"]
    spercent = predictData4.val()["percent"]
    spercent1 = predictData4.val()["percent1"]
    spercent2 = predictData4.val()["percent2"]
    spercent3 = predictData4.val()["percent3"]
    spercent4 = predictData4.val()["percent4"]
    stechnique = predictData4.val()["technique"]

    return render_template("profile.html", email=person["email"], name=person["name"],lastname=person["lastname"],image=person["image"],
                          dtechnique=dtechnique,dpredict=dpredict,dpredict1=dpredict1,dpredict2=dpredict2
                           ,dpredict3=dpredict3,dpredict4=dpredict4,dpercent=dpercent
                           ,dpercent1=dpercent1,dpercent2=dpercent2,dpercent3=dpercent3
                           ,dpercent4=dpercent4,stechnique=stechnique,spredict=spredict,spredict1=spredict1,spredict2=spredict2
                           ,spredict3=spredict3,spredict4=spredict4,spercent=spercent
                           ,spercent1=spercent1,spercent2=spercent2,spercent3=spercent3
                           ,spercent4=spercent4,ptechnique=ptechnique,ppredict=ppredict,ppredict1=ppredict1,ppredict2=ppredict2
                           ,ppredict3=ppredict3,ppredict4=ppredict4,ppercent=ppercent
                           ,ppercent1=ppercent1,ppercent2=ppercent2,ppercent3=ppercent3
                           ,ppercent4=ppercent4,ltechnique=ltechnique,lpredict=lpredict,lpredict1=lpredict1,lpredict2=lpredict2
                           ,lpredict3=lpredict3,lpredict4=lpredict4,lpercent=lpercent
                           ,lpercent1=lpercent1,lpercent2=lpercent2,lpercent3=lpercent3
                           ,lpercent4=lpercent4,ctechnique=ctechnique,cpredict=cpredict,cpredict1=cpredict1,cpredict2=cpredict2
                           ,cpredict3=cpredict3,cpredict4=cpredict4,cpercent=cpercent
                           ,cpercent1=cpercent1,cpercent2=cpercent2,cpercent3=cpercent3
                           ,cpercent4=cpercent4,technique=technique)


@app.route('/predict')
def predict():

        global person
        person["is_logged_in"] = True
        person["uid"] = person["uid"]
        person["name"] = person["name"]
        person["email"] = person["email"]
        # Get the name of the user

        data = db.child("users").get()
        person["image"] = data.val()[person["uid"]]["image"]

        sad = ""


        return render_template("predict.html", email=person["email"], name=person["name"],image=person["image"],umessage=sad)


@app.route('/pred', methods=['POST'])
def pred():
    try:
        freq = 44100
        # get audio file
        Desire = request.form["technique"]
        audio_file = request.files["UploadedAudio"]
        path = r"\static"

        print(Desire)
        print(audio_file)

        with open('static/audio.wav', 'wb') as audio:
            audio_file.save(audio)
        print('file uploaded successfully')
        filename = "static/audio.wav"
        print(filename)
        # file_name = str(random.randint(0, 100000))
        # save the file locally
        # audio_file.save(file_name)
        # my_clip = mp.VideoFileClip(r"audio_file")

        # random string of digits for file name
        print("tang ina mo")

        # make prediction

        SAMPLE_RATE = 44100
        TRACK_DURATION = 3  # measured in seconds
        SAMPLES_PER_TRACK = SAMPLE_RATE * TRACK_DURATION
        num_mfcc = 40
        n_fft = 4096
        hop_length = 512
        num_segments = 6

        samples_per_segment = int(SAMPLES_PER_TRACK / num_segments)
        num_mfcc_vectors_per_segment = math.ceil(samples_per_segment / hop_length)
        signal, sample_rate = librosa.load(filename, sr=SAMPLE_RATE, res_type='kaiser_fast')

        for d in range(num_segments):
            start = samples_per_segment * d
            finish = start + samples_per_segment

        mfccs = librosa.feature.mfcc(signal[start:finish], sample_rate, n_mfcc=num_mfcc, n_fft=n_fft, hop_length=hop_length)
        mfccs = mfccs.T

        mfccs.shape
        mfccs = mfccs[..., np.newaxis]
        print(mfccs.shape)
        mfccs = mfccs[np.newaxis, ...]
        print(mfccs.shape)
        prediction = model.predict(mfccs)
        predicted_index = np.argmax(prediction, axis=1)
        predicted = z[predicted_index]
        percent = prediction[0, predicted_index] * 100
        print("Prediction Summary")
        print(predicted, ":", prediction[0, predicted_index])
        # 2nd
        prediction1 = prediction
        predicted_index1 = np.argmax(prediction1, axis=1)
        prediction1[0, predicted_index1] = 0
        predicted_index2 = np.argmax(prediction1, axis=1)
        predicted1 = z[predicted_index2]
        percent1 = prediction1[0, predicted_index2] * 100

        print(predicted1, ":", prediction1[0, predicted_index2])
        # 3rd
        prediction2 = prediction1
        prediction2[0, predicted_index2] = 0
        predicted_index3 = np.argmax(prediction2, axis=1)
        predicted2 = z[predicted_index3]
        percent2 = prediction2[0, predicted_index3] * 100
        print(predicted2, ": ", prediction2[0, predicted_index3])
        # 4th
        prediction3 = prediction2
        prediction3[0, predicted_index3] = 0
        predicted_index4 = np.argmax(prediction3, axis=1)
        predicted3 = z[predicted_index4]
        percent3 = prediction3[0, predicted_index4] * 100
        print(predicted3, ": ", prediction3[0, predicted_index4])
        # 5th
        prediction4 = prediction3
        prediction4[0, predicted_index4] = 0
        predicted_index5 = np.argmax(prediction4, axis=1)
        predicted4 = z[predicted_index5]
        percent4 = (prediction4[0, predicted_index5]) * 100
        print(predicted4, ": ", prediction4[0, predicted_index5])

        print_message = ' '.join([str(elem) for elem in predicted])
        print_message2 = ' '.join([str(elem) for elem in predicted1])
        print_message3 = ' '.join([str(elem) for elem in predicted2])
        print_message4 = ' '.join([str(elem) for elem in predicted3])
        print_message5 = ' '.join([str(elem) for elem in predicted4])

        percent_message = ' '.join([str(elem) for elem in percent])
        result = float(percent_message)
        result = math.trunc(result)
        percent_message = result
        percent_message2 = ' '.join([str(elem) for elem in percent1])
        result2 = float(percent_message2)
        result2 = math.trunc(result2)
        percent_message2 = result2
        percent_message3 = ' '.join([str(elem) for elem in percent2])
        result3 = float(percent_message3)
        result3 = math.trunc(result3)
        percent_message3 = result3
        percent_message4 = ' '.join([str(elem) for elem in percent3])
        result4 = float(percent_message4)
        result4 = math.trunc(result4)
        percent_message4 = result4
        percent_message5 = ' '.join([str(elem) for elem in percent4])
        result5 = float(percent_message5)
        result5 = math.trunc(result5)
        percent_message5 = result5

        result = print_message

        # remove the .wav file

        # message to be displayed on the html webpage
        prediction_message = print_message
        prediction_message1 = print_message2
        prediction_message2 = print_message3
        prediction_message3 = print_message4
        prediction_message4 = print_message5

        outputArray = [(prediction_message, percent_message), (prediction_message1, percent_message2),
                       (prediction_message2, percent_message3)
            , (prediction_message3, percent_message4), (prediction_message4, percent_message5)]
        print(outputArray)
        global person
        person["is_logged_in"] = True
        person["uid"] = person["uid"]
        person["name"] = person["name"]
        person["email"] = person["email"]
        # Get the name of the user

        data = db.child("users").get()
        person["image"] = data.val()[person["uid"]]["image"]

        # store audio
        # storage.child("users").child(person["uid"]).put(audio_file)
        # audioUrl = storage.child("users").child(person["uid"]).get_url(person["email"])
        # print(audioUrl)
        # audiodata = {"audio": audioUrl}
        # db.child("users").child(person["uid"]).update(audiodata)
        print(Desire)
        # save last input
        if Desire == "DETACHE":
            data = {"predicted": prediction_message, "predicted1": prediction_message1, "predicted2": prediction_message2,
                    "predicted3": prediction_message3, "predicted4": prediction_message4, "percent": percent_message,
                    "percent1": percent_message2, "percent2": percent_message3, "percent3": percent_message4,
                    "percent4": percent_message5, "technique": Desire}
            db.child("users").child(person["uid"]).child("Detache").update(data)
        elif Desire == "CHORDS":
            data = {"predicted": prediction_message, "predicted1": prediction_message1, "predicted2": prediction_message2,
                    "predicted3": prediction_message3, "predicted4": prediction_message4, "percent": percent_message,
                    "percent1": percent_message2, "percent2": percent_message3, "percent3": percent_message4,
                    "percent4": percent_message5, "technique": Desire}
            db.child("users").child(person["uid"]).child("Chord").update(data)
        elif Desire == "SON FILE":
            data = {"predicted": prediction_message, "predicted1": prediction_message1, "predicted2": prediction_message2,
                    "predicted3": prediction_message3, "predicted4": prediction_message4, "percent": percent_message,
                    "percent1": percent_message2, "percent2": percent_message3, "percent3": percent_message4,
                    "percent4": percent_message5, "technique": Desire}
            db.child("users").child(person["uid"]).child("SonFile").update(data)
        elif Desire == "PORTATO":
            data = {"predicted": prediction_message, "predicted1": prediction_message1, "predicted2": prediction_message2,
                    "predicted3": prediction_message3, "predicted4": prediction_message4, "percent": percent_message,
                    "percent1": percent_message2, "percent2": percent_message3, "percent3": percent_message4,
                    "percent4": percent_message5, "technique": Desire}
            db.child("users").child(person["uid"]).child("Portato").update(data)
        elif Desire == "LEGATO":
            data = {"predicted": prediction_message, "predicted1": prediction_message1, "predicted2": prediction_message2,
                    "predicted3": prediction_message3, "predicted4": prediction_message4, "percent": percent_message,
                    "percent1": percent_message2, "percent2": percent_message3, "percent3": percent_message4,
                    "percent4": percent_message5, "technique": Desire}
            db.child("users").child(person["uid"]).child("Legato").update(data)
            return render_template("output.html", prediction_text=prediction_message, prediction_text2=prediction_message1,
                                   prediction_text3=prediction_message2, prediction_text4=prediction_message3,
                                   prediction_text5=prediction_message4, percent_text=percent_message,
                                   percent_text2=percent_message2, percent_text3=percent_message3,
                                   percent_text4=percent_message4, percent_text5=percent_message5, show_modal=True,
                                   email=person["email"], name=person["name"], image=person["image"],
                                   audiofile="static/audio.wav", targetc=Desire)
    except:
        mensahe = "Invalid Input! User recordings should be 3 seconds for an optimal result"
        return render_template("predict.html", email=person["email"], name=person["name"], image=person["image"],umessage=mensahe)
    return render_template("output.html", prediction_text=prediction_message, prediction_text2=prediction_message1,
                           prediction_text3=prediction_message2, prediction_text4=prediction_message3,
                           prediction_text5=prediction_message4, percent_text=percent_message,
                           percent_text2=percent_message2, percent_text3=percent_message3,
                           percent_text4=percent_message4, percent_text5=percent_message5, show_modal=True,
                           email=person["email"], name=person["name"], image=person["image"],
                           audiofile="static/audio.wav", targetc=Desire)


if __name__ == '__main__':
    app.run()