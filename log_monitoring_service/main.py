# log_monitor.py

import time
import requests
import os
import sys
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

class DNSLogHandler(FileSystemEventHandler):
    def __init__(self, logfile, api_url, blacklist_path):
        """
        Initializes the DNSLogHandler.

        :param logfile: Path to the Zeek DNS log file.
        :param api_url: URL of the Prediction Microservice API endpoint.
        :param blacklist_path: Path to the blacklist file where blocked domains are stored.
        """
        self.logfile = logfile
        self.api_url = api_url
        self.blacklist_path = blacklist_path
        self.file = open(logfile, 'r')
        self.file.seek(0, os.SEEK_END)  # Move to the end of the file
        logging.info(f"Started monitoring {self.logfile}")

    def on_modified(self, event):
        """
        Event handler for file modifications.

        :param event: File system event.
        """
        if event.src_path != self.logfile:
            return  # Ignore other files

        logging.debug(f"{self.logfile} has been modified.")

        for line in self.file:
            domain = self.extract_domain(line)
            if domain:
                logging.info(f"Detected new domain: {domain}")
                self.process_domain(domain)

    def extract_domain(self, log_line):
        """
        Extracts the queried domain from a Zeek DNS log line.

        :param log_line: A single line from the DNS log.
        :return: Extracted domain or None if extraction fails.
        """
        try:
            # Zeek DNS log fields are tab-separated. Adjust the index based on your Zeek version/config.
            fields = log_line.strip().split('\t')
            if len(fields) < 10:
                logging.warning(f"Unexpected log format: {log_line}")
                return None

            # Common Zeek dns.log format fields
            # Refer to Zeek documentation for exact field indices
            # Example Zeek 4.x dns.log fields:
            # ts, uid, id.orig_h, id.orig_p, id.resp_h, id.resp_p,
            # query, qclass, qtype, rcode, ... 

            # Adjust the index based on your actual Zeek dns.log format
            # Here, assuming 'query' is at index 6
            domain = fields[6].lower()
            return domain
        except Exception as e:
            logging.error(f"Error extracting domain from line: {e}")
            return None

    def process_domain(self, domain):
        """
        Sends the domain to the Prediction Microservice and handles the response.

        :param domain: The domain to be classified.
        """
        try:
            response = requests.post(
                self.api_url,
                json={"domain": domain},
                timeout=5  # Set a timeout to prevent hanging
            )
            response.raise_for_status()  # Raise an error for bad status codes

            result = response.json()
            prediction = result.get("prediction")

            if prediction == 1:
                logging.info(f"Domain '{domain}' classified as DGA. Blocking...")
                self.block_domain(domain)
            else:
                logging.debug(f"Domain '{domain}' is legitimate.")
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed for domain '{domain}': {e}")
        except ValueError:
            logging.error(f"Invalid JSON response for domain '{domain}': {response.text}")

    def block_domain(self, domain):
        """
        Adds the domain to the blacklist file if not already present.

        :param domain: The domain to be blocked.
        """
        try:
            # Check if the domain is already in the blacklist to prevent duplicates
            with open(self.blacklist_path, 'r+') as f:
                lines = f.read().splitlines()
                if domain in lines:
                    logging.debug(f"Domain '{domain}' is already in the blacklist.")
                    return

                f.write(f"{domain}\n")
                logging.info(f"Added '{domain}' to the blacklist.")
        except FileNotFoundError:
            # If the blacklist file doesn't exist, create it and add the domain
            with open(self.blacklist_path, 'w') as f:
                f.write(f"{domain}\n")
                logging.info(f"Created blacklist file and added '{domain}'.")
        except Exception as e:
            logging.error(f"Error writing to blacklist file: {e}")

def main():
    # Configuration - these can be parameterized or loaded from environment variables
    LOGFILE = "/var/log/zeek/dns.log"  # Path to Zeek's dns.log
    API_URL = "http://localhost:8000/predict"  # Prediction Microservice API endpoint
    BLACKLIST_PATH = "/etc/blacklist/domains.txt"  # Path to blacklist file

    # Validate that the logfile exists
    if not os.path.isfile(LOGFILE):
        logging.error(f"Log file '{LOGFILE}' does not exist. Exiting.")
        sys.exit(1)

    # Ensure the blacklist directory exists
    blacklist_dir = os.path.dirname(BLACKLIST_PATH)
    if not os.path.isdir(blacklist_dir):
        try:
            os.makedirs(blacklist_dir)
            logging.info(f"Created blacklist directory at '{blacklist_dir}'.")
        except Exception as e:
            logging.error(f"Failed to create blacklist directory '{blacklist_dir}': {e}")
            sys.exit(1)

    # Initialize event handler and observer
    event_handler = DNSLogHandler(LOGFILE, API_URL, BLACKLIST_PATH)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(LOGFILE), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        logging.info("Stopping log monitoring service...")
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
