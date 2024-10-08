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
            raise

try:
    download_file(MODEL_URL, 'model.sav')
    download_file(TFIDF_URL, 'tfidf_vectorizer.sav')
except Exception as e:
    print(f"Error during file download: {e}")
    raise SystemExit(e)

# Load the model and vectorizer
try:
    model_mnb = joblib.load('model.sav')
    tfidf = joblib.load('tfidf_vectorizer.sav')
except Exception as e:
    print(f"Error loading model or vectorizer: {e}")
    raise SystemExit(e)

# Initialize the PorterStemmer
ps = PorterStemmer()

# Initialize NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Ensure the 'punkt' resource is available
nltk.download('punkt_tab')

def transform_sms(message):
    try:
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
    
    except Exception as e:
        print(f"Error in SMS transformation: {e}")
        return None

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_sms = data.get('message')
        
        if not input_sms:
            return jsonify({'error': 'No message provided'}), 400
        
        # Transform the input SMS
        input_sms = transform_sms(input_sms)
        if input_sms is None:
            return jsonify({'error': 'Failed to process the message'}), 500

        # Convert the transformed SMS into TF-IDF vector
        input_sms_vectorized = tfidf.transform([input_sms])

        # Predict using the loaded model
        pred = model_mnb.predict(input_sms_vectorized)[0]
        
        # Return the prediction as JSON
        return jsonify({'prediction': 'Spam' if pred == 1 else 'Not Spam'})

    except Exception as e:
        print(f"Error in prediction: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
