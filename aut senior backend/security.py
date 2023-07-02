import requests
from flask import Flask, request, jsonify
from flask_cors import CORS,cross_origin

app = Flask(__name__)
CORS(app)


@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file():
    
    file = request.files['file']

    url = "https://www.virustotal.com/api/v3/files"

    headers = {
        "x-apikey": "9edaf6f7a3e7a50d24ad1b66034b0d6ee0e046252e82e8508125ce42b9ffd75f" 
    }

    files = {
        'file': (file.filename, file.stream, file.mimetype)
    }

    response = requests.post(url, headers=headers, files=files)
    result = response.json()

    analysis_id = result['data']['id']
    analysis_url = result['data']['links']['self']

    analysis_results = get_analysis_results(analysis_id, headers)

    return jsonify({'analysis_id': analysis_id, 'analysis_url': analysis_url, 'analysis_results': analysis_results})


def get_analysis_results(analysis_id, headers):
    url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"

    response = requests.get(url, headers=headers)
    result = response.json()

  
    analysis_results = {
        'status': result['data']['attributes']['status'],
        'results': result['data']['attributes']['results']
    }

    return analysis_results


if __name__ == '__main__':
    app.run(port= 5004)