# Spam Detection API

This is a simple spam detection API that classifies SMS messages as "Spam" or "Not Spam" using a machine learning model.

## Overview

The Spam Detection API provides a POST endpoint where you can submit SMS messages for classification. The API is built with Flask and deployed on Render.

**Base URL:** `https://spam-detection-wdd4.onrender.com`

## Endpoints

### `POST /predict`

**Description:** Predict whether the input SMS message is spam or not.

**Request:**

- **Headers:**
  - `Content-Type: application/json`

- **Body:**

  ```json
  {
    "message": "Your SMS message here"
  }


Response:
{
  "prediction": "Spam"  // or "Not Spam"
}
