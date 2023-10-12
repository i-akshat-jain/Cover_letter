import requests
from bs4 import BeautifulSoup
from flask import Flask

app = Flask(__name)

@app.route('/get_data')

def get_data():
    # Get the URL from the query parameter
    url = request.args.get('url')
    console.log(url)

    if url:
        # Open the URL with a GET request
        resp = requests.get(url)

        if resp.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(resp.text, 'html.parser')

            # Find the specific div element containing the job description
            job_description_div = soup.find(
                "div", {"data-qa": "job-description"})

            if job_description_div:
                # Extract and return the text content of the div
                job_description = job_description_div.get_text()
                return job_description

    # If there's an issue, return an error message
    return "Error fetching job description"
