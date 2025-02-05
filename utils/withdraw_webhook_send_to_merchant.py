import requests
import logging


def send_request(url, object_json):
    try:
        # Convert the serializer data to JSON
        json_data = object_json.data if hasattr(object_json, 'data') else object_json

        # Send a POST request with JSON data
        response = requests.post(url, json=json_data)

        # Check if the request was successful
        if response.status_code == 200:
            logging.info("Request sent successfully to %s", url)
            return True
        else:
            logging.error("Failed to send request to %s: %s", url, response.text)
            return False
    except requests.exceptions.RequestException as e:
        # Log any error that occurs during the request sending
        logging.error("An error occurred when sending request to %s: %s", url, str(e))
        return False
