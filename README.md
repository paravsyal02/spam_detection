# Spam Detection API

## Overview

The Spam Detection API is a RESTful service that classifies SMS messages as either "Spam" or "Not Spam" using a pre-trained machine learning model. The API is built using Flask and is deployed on Render.

**Base URL:** `https://spam-detection-wdd4.onrender.com`

## Features

- **Classify SMS messages**: Determine if a given SMS message is spam or not.
- **Pre-trained Model**: Utilizes a machine learning model for classification.
- **TF-IDF Vectorizer**: Converts text into features for the model.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
  - [Predict](#predict)
- [Testing with Postman](#testing-with-postman)
- [Local Development](#local-development)
- [Model and Data](#model-and-data)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

To use this API, follow these steps to clone and set up the project locally:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/spam_detection.git
   cd spam_detection
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Flask application:**

   ```bash
   python app.py
   ```

   The application will start and be available at `http://localhost:5000`.

## API Endpoints

### Predict

**Endpoint:** `/predict`

**Method:** `POST`

**Description:** Classify the input SMS message as "Spam" or "Not Spam".

**Request:**

- **Headers:**
  - `Content-Type: application/json`

- **Body:**

  ```json
  {
    "message": "Your SMS message here"
  }
  ```

**Response:**

- **Success (200 OK):**

  ```json
  {
    "prediction": "Spam"  // or "Not Spam"
  }
  ```

- **Error (400 Bad Request):**

  ```json
  {
    "error": "No message provided"
  }
  ```

- **Error (500 Internal Server Error):**

  ```json
  {
    "error": "Failed to process the message"
  }
  ```

## Testing with Postman

1. **Open Postman and create a new POST request.**
2. **Enter the URL:** `https://spam-detection-wdd4.onrender.com/predict`
3. **Set the header `Content-Type` to `application/json`.**
4. **In the body tab, select `raw` and `JSON` format, then enter:**

   ```json
   {
     "message": "Congratulations! You've won a $1000 gift card."
   }
   ```

5. **Click "Send" to submit the request and view the response.**

## Local Development

To run the API locally:

1. **Ensure all dependencies are installed as described in the [Installation](#installation) section.**
2. **Run the Flask application using:**

   ```bash
   python app.py
   ```

3. **The application will be accessible at `http://localhost:5000`.**

## Model and Data

The API uses a pre-trained machine learning model and TF-IDF vectorizer. These are fetched from:

- **Model:** [model.sav](https://github.com/paravsyal02/spam_detection/releases/download/v1.0.0/model.sav)
- **TF-IDF Vectorizer:** [tfidf_vectorizer.sav](https://github.com/paravsyal02/spam_detection/releases/download/v1.0.0/tfidf_vectorizer.sav)

## Contributing

Contributions are welcome! Please open issues or submit pull requests if you have suggestions or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please contact [Your Name](mailto:your.email@example.com).
```

You can copy this directly into your `README.md` file. Adjust any placeholders like `your-username`, `your.email@example.com`, or other specifics as needed.
