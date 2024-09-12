from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

ESPN_API_BASE_URL = "https://fantasy.espn.com/apis/v3/games/ffl"

FETCH_ALL_LEAGUES_URL = f"https://fan.api.espn.com/apis/v2/fans/{{}}?displayHiddenPrefs=true&context=fantasy&useCookieAuth=true&source=fantasyapp-ios&featureFlags=challengeEntries"

@app.route('/api/all-leagues', methods=['GET'])
def get_all_leagues():
    swid = request.headers.get('X-SWID')
    espn_s2 = request.headers.get('X-ESPN-S2')
    
    if not swid or not espn_s2:
        return jsonify({"error": "Missing authentication headers"}), 400

    cookies = {
        'SWID': swid,
        'espn_s2': espn_s2
    }

    url = FETCH_ALL_LEAGUES_URL.format(swid)
    
    response = requests.get(url, cookies=cookies)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch all leagues from ESPN"}), response.status_code

@app.route('/api/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Test route is working"}), 200

@app.route('/api/leagues', methods=['GET'])
def get_leagues():
    

    swid = request.headers.get('X-SWID')
    espn_s2 = request.headers.get('X-ESPN-S2')
    
    if not swid or not espn_s2:
        return jsonify({"error": "Missing authentication cookies"}), 400

    cookies = {
        'SWID': swid,
        'espn_s2': espn_s2
    }

    response = requests.get(f"{ESPN_API_BASE_URL}/seasons/2023/segments/0/leagues?view=mTeam", cookies=cookies)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch leagues from ESPN"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)