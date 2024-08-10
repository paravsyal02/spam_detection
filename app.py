from flask import Flask, request, jsonify
import numpy as np
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string

# Initialize Flask app
app = Flask(__name__)

# Load the model and vectorizer
model_mnb = pickle.load(open('model.sav', 'rb'))
tfidf = pickle.load(open('tfidf_vectorizer.sav', 'rb'))

# Initialize the PorterStemmer
ps = PorterStemmer()

def transform_sms(message):
    # Convert all characters to lowercase
    message = message.lower()

    # Break SMS record into words
    message = nltk.word_tokenize(message)

    # Remove special symbols (keeping only alphanumeric characters)
    temp = [i for i in message if i.isalnum()]

    # Removing stopwords and punctuations
    temp = [i for i in temp if i not in stopwords.words('english') and i not in string.punctuation]

    # Stemming
    temp = [ps.stem(i) for i in temp]

    # Return the transformed message as a single string
    return " ".join(temp)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_sms = data.get('message')
    
    if not input_sms:
        return jsonify({'error': 'No message provided'}), 400
    
    # Transform the input SMS
    input_sms = transform_sms(input_sms)

    # Convert the transformed SMS into TF-IDF vector
    input_sms_vectorized = tfidf.transform([input_sms])

    # Predict using the loaded model
    pred = model_mnb.predict(input_sms_vectorized)[0]
    
    # Return the prediction as JSON
    return jsonify({'prediction': 'Spam' if pred == 1 else 'Not Spam'})

if __name__ == '__main__':
    app.run(debug=True)
