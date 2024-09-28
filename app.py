from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from espn_api.football import League

app = Flask(__name__)
CORS(app)

ESPN_API_BASE_URL = "https://fantasy.espn.com/apis/v3/games/ffl"

FETCH_ALL_LEAGUES_URL = f"https://fan.api.espn.com/apis/v2/fans/{{}}?displayHiddenPrefs=true&context=fantasy&useCookieAuth=true&source=fantasyapp-ios&featureFlags=challengeEntries"

@app.route('/api/user-leagues', methods=['GET'])
def get_user_leagues():
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

@app.route('/api/user-leagues/details/<int:league_id>', defaults={'year': 2024}, methods=['GET'])
@app.route('/api/user-leagues/details/<int:league_id>/<int:year>', methods=['GET'])
def get_user_league_details(league_id, year = 2024):
    swid = request.headers.get('X-SWID')
    espn_s2 = request.headers.get('X-ESPN-S2')
    
    if not swid or not espn_s2:
        return jsonify({"error": "Missing authentication cookies"}), 400
    
    try: 
        year = int(year)
        league_id = int(league_id)
        league = League(league_id = league_id, year = year, espn_s2 = espn_s2, swid = swid, debug = True)
        standings = league.standings()
        league_data = {
            "league_id": league.league_id,
            "year": league.year,
            "current_fantasy_week": league.current_week,
            "current_nfl_week": league.nfl_week,
            "name": league.settings.name,
            "teams": [{'team_id': team.team_id,'team_abbrev': team.team_abbrev,'team_name': team.team_name, "wins": team.wins, "losses": team.losses, "ties": team.ties, "points_for": team.points_for, "points_against": team.points_against, "logo": team.logo_url} for team in league.teams],
            "standings": [{'team_name': team.team_name, "wins": team.wins, "losses": team.losses, "ties": team.ties, "points_for": team.points_for, "points_against": team.points_against, "logo": team.logo_url} for team in standings]
        }
        return jsonify(league_data), 200
    except Exception as e:
        return jsonify({"FLASK API error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)