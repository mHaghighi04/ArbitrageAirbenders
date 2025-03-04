import threading
import time
import requests
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

# =======================
# Global Configuration
# =======================
api_key = '27e335d9311b8e173b54dfe65ba76352'
markets = 'h2h'
regions = 'us'
odds_format = 'decimal'

# =======================
# Arbitrage Logic Functions
# =======================
def check_arbitrage(odd1, odd2):
    """
    Checks if an arbitrage opportunity exists for a two-outcome event given two odds.
    Returns (bool, float) where the bool indicates if arbitrage exists,
    and float is the inverse sum.
    """
    inverse_sum = (1 / odd1) + (1 / odd2)
    return (inverse_sum < 1), inverse_sum

def calculate_stakes(odd1, odd2, total_stake):
    """
    Calculates individual stakes for each outcome given a total stake.
    Returns a list of two stakes if arbitrage exists, otherwise None.
    """
    arbitrage, inv_sum = check_arbitrage(odd1, odd2)
    if not arbitrage:
        return None
    stake1 = (total_stake * (1 / odd1)) / inv_sum
    stake2 = (total_stake * (1 / odd2)) / inv_sum
    return [stake1, stake2]

def convert_to_american(decimal_odds):
    """
    Converts decimal odds to American odds (rounded to nearest integer).
    """
    if decimal_odds >= 2.0:
        american = (decimal_odds - 1) * 100
    else:
        american = -100 / (decimal_odds - 1)
    return round(american)

# =======================
# Odds Fetching and Arbitrage Computation
# =======================
def fetch_odds(sport):
    """
    Fetches odds data from The Odds API for the given sport.
    Returns a list of events.
    """
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
    params = {
        "apiKey": api_key,
        "regions": regions,
        "markets": markets,
        "oddsFormat": odds_format
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Failed to get odds: status_code {response.status_code}, response body {response.text}")
        return []
    data = response.json()
    return data

def extract_bookmaker_odds(event):
    """
    For a given event, extracts odds from each bookmaker as a dictionary:
      {
         'bookmaker': <bookmaker title>,
         'home_odds': <decimal odd for home_team>,
         'away_odds': <decimal odd for away_team>
      }
    Returns a list of such dictionaries.
    """
    bookmakers_list = []
    home_team = event.get("home_team")
    away_team = event.get("away_team")
    for bookmaker in event.get("bookmakers", []):
        for market in bookmaker.get("markets", []):
            if market.get("key") == "h2h" and market.get("outcomes") and len(market["outcomes"]) >= 2:
                outcomes = market["outcomes"]
                if outcomes[0]["name"] == home_team:
                    home_odds = outcomes[0]["price"]
                    away_odds = outcomes[1]["price"]
                elif outcomes[1]["name"] == home_team:
                    home_odds = outcomes[1]["price"]
                    away_odds = outcomes[0]["price"]
                else:
                    continue  # Could not match team names.
                bookmakers_list.append({
                    "bookmaker": bookmaker["title"],
                    "home_odds": home_odds,
                    "away_odds": away_odds
                })
                break  # One market per bookmaker is enough.
    return bookmakers_list

def find_arbitrage_opportunities_for_event(event, total_stake=1000):
    """
    For a given event, checks all combinations of bookmakers (order matters)
    to see if an arbitrage opportunity exists.
    Returns a list of arbitrage opportunity dictionaries.
    """
    arbitrage_ops = []
    home_team = event.get("home_team")
    away_team = event.get("away_team")
    event_name = f"{home_team} vs {away_team}"
    
    bookmakers = extract_bookmaker_odds(event)
    n = len(bookmakers)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            # Case 1: bookmaker i's home odd and bookmaker j's away odd.
            odd_home = bookmakers[i]["home_odds"]
            odd_away = bookmakers[j]["away_odds"]
            arb_exists, inv_sum = check_arbitrage(odd_home, odd_away)
            if arb_exists:
                stakes = calculate_stakes(odd_home, odd_away, total_stake)
                profit_margin = round((1 - inv_sum) * 100, 2)
                total_profit = round(total_stake * (1 - inv_sum), 2)
                arbitrage_ops.append({
                    "event": event_name,
                    "home_team": home_team,
                    "away_team": away_team,
                    "home_book": bookmakers[i]["bookmaker"],
                    "away_book": bookmakers[j]["bookmaker"],
                    "home_odds": odd_home,
                    "away_odds": odd_away,
                    "home_american_odds": convert_to_american(odd_home),
                    "away_american_odds": convert_to_american(odd_away),
                    "stakes": [round(stakes[0], 2), round(stakes[1], 2)],
                    "total_stake": total_stake,
                    "profit_margin": profit_margin,
                    "total_profit": total_profit,
                    "combination": f"{bookmakers[i]['bookmaker']} (home) / {bookmakers[j]['bookmaker']} (away)"
                })
            # Case 2: bookmaker i's away odd and bookmaker j's home odd.
            odd_home = bookmakers[j]["home_odds"]
            odd_away = bookmakers[i]["away_odds"]
            arb_exists, inv_sum = check_arbitrage(odd_home, odd_away)
            if arb_exists:
                stakes = calculate_stakes(odd_home, odd_away, total_stake)
                profit_margin = round((1 - inv_sum) * 100, 2)
                total_profit = round(total_stake * (1 - inv_sum), 2)
                arbitrage_ops.append({
                    "event": event_name,
                    "home_team": home_team,
                    "away_team": away_team,
                    "home_book": bookmakers[j]["bookmaker"],
                    "away_book": bookmakers[i]["bookmaker"],
                    "home_odds": odd_home,
                    "away_odds": odd_away,
                    "home_american_odds": convert_to_american(odd_home),
                    "away_american_odds": convert_to_american(odd_away),
                    "stakes": [round(stakes[0], 2), round(stakes[1], 2)],
                    "total_stake": total_stake,
                    "profit_margin": profit_margin,
                    "total_profit": total_profit,
                    "combination": f"{bookmakers[j]['bookmaker']} (home) / {bookmakers[i]['bookmaker']} (away)"
                })
    return arbitrage_ops

def find_highest_arbitrage(sport, total_stake=1000):
    """
    Given a sport key (e.g., "basketball_nba"), fetches the odds, computes all arbitrage opportunities,
    and returns the one with the highest profit margin.
    """
    events = fetch_odds(sport)
    all_arbitrage_ops = []
    for event in events:
        if not event.get("bookmakers"):
            continue
        arb_ops = find_arbitrage_opportunities_for_event(event, total_stake)
        if arb_ops:
            all_arbitrage_ops.extend(arb_ops)
    if all_arbitrage_ops:
        highest = max(all_arbitrage_ops, key=lambda op: op["profit_margin"])
        return highest
    else:
        return {}

# =======================
# Flask API Endpoint
# =======================
@app.route("/api/check_arbitrage", methods=["POST", "OPTIONS"])
def get_opportunity():
    """
    Expects a JSON payload with a key "sport" (e.g., {"sport": "basketball_nba"}).
    Returns the highest arbitrage opportunity for that sport as JSON.
    """
    print("check_arbitrage_endpoint was called")

    if request.method == "OPTIONS":
        return jsonify({}), 200
    
    data = request.get_json()
    print("Received sport:", data.get("sport"))
    if not data or "sport" not in data:
        return jsonify({"error": "Please provide a sport key in the JSON body."}), 400

    sport = data["sport"]
    opportunity = find_highest_arbitrage(sport)
    print (opportunity)
    return jsonify(opportunity)

# =======================
# Main Entry
# =======================
if __name__ == "__main__":
    app.run(debug=True)