from flask import Flask, request, jsonify
import numpy as np
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import joblib
import os
import urllib.request

# Initialize Flask app
app = Flask(__name__)

# URLs to your files
MODEL_URL = os.getenv('MODEL_URL', 'https://github.com/paravsyal02/spam_detection/releases/download/v1.0.0/model.sav')
TFIDF_URL = os.getenv('TFIDF_URL', 'https://github.com/paravsyal02/spam_detection/releases/download/v1.0.0/tfidf_vectorizer.sav')

# Download the model and vectorizer from the URLs if not already downloaded
def download_file(url, file_name):
    if not os.path.exists(file_name):
        try:
            urllib.request.urlretrieve(url, file_name)
            print(f'{file_name} downloaded successfully.')
        except Exception as e:
            print(f'Failed to download {file_name}: {e}')

download_file(MODEL_URL, 'model.sav')
download_file(TFIDF_URL, 'tfidf_vectorizer.sav')

# Load the model and vectorizer
model_mnb = joblib.load('model.sav')
tfidf = joblib.load('tfidf_vectorizer.sav')

# Initialize the PorterStemmer
ps = PorterStemmer()

# Initialize NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def transform_sms(message):
    """
    Transform the input SMS by converting to lowercase, removing special symbols, 
    removing stopwords and punctuations, and stemming.
    
    Args:
        message (str): The input SMS message.
    
    Returns:
        str: The transformed SMS message.
    """
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
    """
    Predict whether the input SMS is spam or not.
    
    Args:
        message (str): The input SMS message.
    
    Returns:
        JSON: The prediction result.
    """
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
    return jsonify({'prediction': 'Spam' if pred == 1 else 'Not Spam'})  # Assuming '1' is Spam, '0' is Not Spam

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
