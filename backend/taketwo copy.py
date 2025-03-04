import threading
import time
import requests
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# =======================
# Global Config & Variables
# =======================
# For testing, you might change this to "mma_mixed_martial_arts" if NBA odds produce no opportunities.
api_key = '27e335d9311b8e173b54dfe65ba76352'
sport_key = 'mma_mixed_martial_arts'
markets = 'h2h'
regions = 'us'
odds_format = 'decimal'

# This global variable will hold the highest arbitrage opportunity we find.
latest_arbitrage_opportunity = {}

# =======================
# Arbitrage Logic
# =======================
def check_arbitrage(odd1, odd2):
    """
    Checks if an arbitrage opportunity exists for a two-outcome event given two odds.
    
    Returns:
      (bool, float) -> (arbitrage_exists, inverse_sum)
    """
    inverse_sum = (1 / odd1) + (1 / odd2)
    return (inverse_sum < 1), inverse_sum

def calculate_stakes(odd1, odd2, total_stake):
    """
    Calculates individual stakes for each outcome given a total stake.
    If no arbitrage exists, returns None.
    """
    arbitrage, inv_sum = check_arbitrage(odd1, odd2)
    if not arbitrage:
        return None

    stake1 = (total_stake * (1 / odd1)) / inv_sum
    stake2 = (total_stake * (1 / odd2)) / inv_sum
    return [stake1, stake2]

def convert_to_american(decimal_odds):
    """
    Converts decimal odds to American odds, rounded to the nearest integer.
    """
    if decimal_odds >= 2.0:
        american = (decimal_odds - 1) * 100
    else:
        american = -100 / (decimal_odds - 1)
    return round(american)

# =======================
# Fetching Odds and Generating Arbitrage Combinations
# =======================
def fetch_mma_odds():
    """
    Fetches odds from The Odds API and returns the raw events list.
    """
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds"
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
    print("Number of events:", len(data))
    print("Remaining requests:", response.headers.get('x-requests-remaining', 'N/A'))
    print("Used requests:", response.headers.get('x-requests-used', 'N/A'))
    return data

def extract_bookmaker_odds(event):
    """
    For a given event, extract odds from each bookmaker as a dictionary:
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
                # Determine which outcome is for home and which for away.
                if outcomes[0]["name"] == home_team:
                    home_odds = outcomes[0]["price"]
                    away_odds = outcomes[1]["price"]
                elif outcomes[1]["name"] == home_team:
                    home_odds = outcomes[1]["price"]
                    away_odds = outcomes[0]["price"]
                else:
                    continue  # Can't match names.
                bookmakers_list.append({
                    "bookmaker": bookmaker["title"],
                    "home_odds": home_odds,
                    "away_odds": away_odds
                })
                break  # One market per bookmaker is enough.
    return bookmakers_list

def find_arbitrage_opportunities_for_event(event, total_stake=1000):
    """
    For the given event, check all combinations of bookmakers (order matters)
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
            # Case 1: Use bookmaker i's home odd and bookmaker j's away odd.
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
            # Case 2: Use bookmaker i's away odd and bookmaker j's home odd.
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

# =======================
# Background Thread to Update Odds
# =======================
def update_odds_data():
    """
    Periodically fetches odds data, checks all combinations for arbitrage opportunities,
    and updates the global variable with only the highest percentage return opportunity.
    """
    global latest_arbitrage_opportunity
    while True:
        events = fetch_mma_odds()
        all_arbitrage_ops = []
        for event in events:
            if not event.get("bookmakers"):
                continue
            arb_ops = find_arbitrage_opportunities_for_event(event, total_stake=1000)
            if arb_ops:
                all_arbitrage_ops.extend(arb_ops)
        print("Total arbitrage opportunities found:", len(all_arbitrage_ops))
        if all_arbitrage_ops:
            highest_opportunity = max(all_arbitrage_ops, key=lambda op: op["profit_margin"])
            latest_arbitrage_opportunity = highest_opportunity
            print("Highest arbitrage opportunity:", highest_opportunity)
        else:
            latest_arbitrage_opportunity = {}
            print("No arbitrage opportunity found in this update cycle.")
        # Use a shorter sleep for debugging; adjust as needed.
        time.sleep(5000)

# =======================
# Flask Routes
# =======================
@app.route("/")
def index():
    """
    Renders a simple HTML page displaying the highest arbitrage opportunity.
    """
    html = """
    <!doctype html>
    <html>
    <head>
        <title>NBA Arbitrage Opportunity</title>
    </head>
    <body>
        <h1>Highest NBA Arbitrage Opportunity</h1>
        {% if opportunity %}
            <strong>{{ opportunity.event }}</strong><br>
            <b>Bookmakers:</b> {{ opportunity.home_book }} ({{ opportunity.home_team }}) for home 
            &amp; {{ opportunity.away_book }} ({{ opportunity.away_team }}) for away<br>
            <b>Combination:</b> {{ opportunity.combination }}<br>
            <b>Decimal Odds:</b> [{{ opportunity.home_odds }}, {{ opportunity.away_odds }}]<br>
            <b>American Odds:</b> [{{ opportunity.home_american_odds }}, {{ opportunity.away_american_odds }}]<br>
            <b>Stakes</b> (for total stake ${{ opportunity.total_stake }}): 
            [${{ opportunity.stakes[0] }}, ${{ opportunity.stakes[1] }}]<br>
            <b>Profit Margin:</b> {{ opportunity.profit_margin }}%<br>
            <b>Total Profit:</b> ${{ opportunity.total_profit }}
        {% else %}
            <p>No arbitrage opportunities available at the moment.</p>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(html, opportunity=latest_arbitrage_opportunity)

@app.route("/api/opportunities")
def opportunities():
    """
    API endpoint to return the highest arbitrage opportunity as JSON.
    """
    return jsonify(latest_arbitrage_opportunity)

# =======================
# Main Entry
# =======================
if __name__ == "__main__":
    # Start the background thread to update odds data.
    updater = threading.Thread(target=update_odds_data, daemon=True)
    updater.start()
    # Run the Flask app.
    app.run(debug=True)
