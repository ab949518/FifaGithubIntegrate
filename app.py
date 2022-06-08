from flask import Flask, render_template, redirect, url_for, request

#import libraries
import numpy as np
import pickle
import os
#Initialize the flask App
app = Flask(__name__)
model = pickle.load(open('final_model.pkl', 'rb'))

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/home')
def home():
    return render_template('home.html')


def PredictRating(to_predict_list):
    to_predict = np.array(to_predict_list)
    load_model = pickle.load(open("final_model.pkl", "rb"))
    final_result = load_model.predict(to_predict)
    return final_result

@app.route('/results', methods = ['GET', 'POST'])
def results():
    #For rendering results on HTML GUI
    to_predict_list = [float(x) for x in request.form.values()]
    final_features = [np.array(to_predict_list)]
    end_rating = PredictRating(final_features) 
    return render_template('results.html', prediction_text='Estimated Player Rating :{}'.format(end_rating))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
    #app.run(debug=False)