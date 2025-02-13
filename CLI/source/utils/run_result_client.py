import http
import sys
import time
import requests
import logging


class RunResultClient:
    def __init__(self, config):
        self.api_url = config.get("GENERAL", "run_result_server_url")
        self.retries = config.getint("GENERAL", "retries", fallback=3)
        self.retry_backoff = config.getint("GENERAL", "retry_backoff", fallback=5)

        if not self.api_url:
            logging.error("API URL not configured.")
            sys.exit(1)

    def send_data(self, publish_request):

        attempt = 0
        while attempt < self.retries:
            try:
                response = requests.post(self.api_url, json=publish_request.to_json())
                if response.status_code == http.HTTPStatus.BAD_REQUEST:
                    logging.error("Error: %s", response.json().get('error', 'Unknown error'))
                    break
                response.raise_for_status()
                logging.info("Data uploaded successfully, it should be exposed in our UI shortly.")
                break
            except requests.exceptions.RequestException as e:
                logging.error("Error sending request: %s", e)
                time.sleep(self.retry_backoff)
                attempt += 1
        else:
            logging.error("Failed to send request after %d attempts.", self.retries)
            sys.exit(1)