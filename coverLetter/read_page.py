import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import chromedriver_autoinstaller
from flask_cors import CORS
import re
import os
import openai

app = Flask(__name__)
CORS(app)

# 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
api_key = "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"
chatgpt_api_url = "https://api.openai.com/v1/engines/davinci-codex/completions"

chromedriver_autoinstaller.install()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(
     options=chrome_options)


@app.route('/get_data')
def get_data():
    # Get the URL from the query parameter
    url = request.args.get('url')

    if url:
        try:
            # Send a GET request to the URL to fetch the page content
            response = requests.get(url)
            if response.status_code == 200:
                time.sleep(5)
                page_content = response.text
                # Parse the page content using BeautifulSoup
                soup = BeautifulSoup(page_content, 'html.parser')

                # Find the element with class "content"
                content_element = soup.find('div', class_='content')

                if content_element:
                    # Extract all the text content from the "content" element
                    all_text = content_element.get_text()
                    filtered_data = filter_data(all_text)
                    print("jsonify", filtered_data)
                    
                    # Create a dictionary to store the extracted data
                    job_data = {
                        "all_text": filtered_data
                    }           
                    print("job_data", job_data)

                    return jsonify(job_data)
                else:
                    return "Error: 'content' element not found on the page"
            else:
                return "Error fetching web page content: Status Code " + str(response.status_code)
        except Exception as e:
            return "Error fetching web page content: " + str(e)
    else:
        return "No URL found"


def filter_data(data):
    # Define a list of characters to remove
    chars_to_remove = ['\\u', '\\u0', '\\u00', '\\u00a', '\\xa0']

    # Iterate through the characters and replace them with an empty string
    for char in chars_to_remove:
        data = data.replace(char, "")
    print("data",data)
    return data


@app.route('/generate_cover_letter', methods=['POST', 'GET'])
def generate_cover_letter():
    # Receive job data from the client
    job_data = request.json.get('job_data', '')

    # Filter and clean the job data (you can keep your filter_data function)
    filtered_data = filter_data(job_data)

    # Create a prompt for ChatGPT
    prompt = f"Generate a cover letter for the following job description:\n{filtered_data}"

    try:
        # Make a request to the ChatGPT API
        response = requests.post(
            chatgpt_api_url,
            headers={
                "Authorization": f"Bearer {api_key}",
            },
            json={
                "prompt": prompt,
                "max_tokens": 150,  # Adjust the maximum response length as needed
            },
        )
        if response.status_code == 200:
            cover_letter = response.json()["choices"][0]["text"]

            # You can further process or customize the generated cover letter as needed

            return jsonify({"cover_letter": cover_letter})
        else:
            return "Error generating cover letter: " + response.text
    except Exception as e:
        return "Error generating cover letter: " + str(e)
if __name__ == '__main__':
    app.run(debug=True)
