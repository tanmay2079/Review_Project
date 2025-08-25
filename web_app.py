from flask import Flask , request,render_template
import numpy as np
import pickle
import tensorflow as tf
import keras

app = Flask(__name__)

f1=open('cv_pickle','rb')
cv=pickle.load(f1)
f1.close()

model = keras.models.load_model('review_RNN_model.keras')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''

    if request.method == 'POST':
        text = request.form['Review']
        data = [text]
        data_cv = cv.transform(data).toarray()
        new1=data_cv.reshape(data_cv.shape[0], 1, data_cv.shape[1])
        prediction = model.predict(new1)
        prediction=prediction[0]
        print(prediction)
        if prediction>0.5:
            prediction=1
        else:
            prediction=0
        if ("not" in text) or ("no" in text) or ("n't" in text):
            prediction= abs(prediction - 1)
    if prediction==1:
        return render_template('index.html', prediction_text='The review is Positive')
    else:
        return render_template('index.html', prediction_text='The review is Negative.')



if __name__ == "__main__":
    app.run(debug=True)
