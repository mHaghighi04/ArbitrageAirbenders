import threading
import time
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Global variable to store the latest arbitrage opportunities
latest_arbitrage_opportunities = []

def fetch_dummy_odds():
    """
    Simulates fetching odds data from an external source.
    Returns a list of events, each with a name and a list of odds.
    """
    # Dummy data: two events with two outcomes each
    return [
        {"event": "Match 1", "odds": [2.10, 2.05]},
        {"event": "Match 2", "odds": [1.80, 2.20]}
    ]

def check_arbitrage(odds_list):
    """
    Checks if an arbitrage opportunity exists.
    
    Parameters:
      odds_list (list): List of odds for different outcomes.
      
    Returns:
      tuple: (arbitrage_exists (bool), inverse_sum (float))
    """
    inverse_sum = sum(1 / odd for odd in odds_list)
    return inverse_sum < 1, inverse_sum

def calculate_stakes(odds_list, total_stake):
    """
    Calculates the individual stakes for each outcome given a total stake.
    
    Parameters:
      odds_list (list): List of odds for different outcomes.
      total_stake (float): Total money to be bet.
      
    Returns:
      list or None: List of stakes for each outcome if arbitrage exists; otherwise, None.
    """
    arbitrage, inverse_sum = check_arbitrage(odds_list)
    if not arbitrage:
        return None
    stakes = [(total_stake * (1 / odd)) / inverse_sum for odd in odds_list]
    return stakes

def convert_to_american(decimal_odds):
    """
    Converts a decimal odd to American odds.
    
    Parameters:
      decimal_odds (float): The decimal odd to convert.
      
    Returns:
      int: The American odd rounded to the nearest integer.
    """
    if decimal_odds >= 2.0:
        american = (decimal_odds - 1) * 100
    else:
        american = -100 / (decimal_odds - 1)
    return round(american)

def update_odds_data():
    """
    Periodically fetches odds data, checks for arbitrage opportunities,
    calculates stakes, and updates the global opportunities list.
    """
    global latest_arbitrage_opportunities
    while True:
        events = fetch_dummy_odds()
        arbitrage_events = []
        for event in events:
            event_name = event["event"]
            odds = event["odds"]
            arbitrage, inv_sum = check_arbitrage(odds)
            if arbitrage:
                total_stake = 1351
                stakes = calculate_stakes(odds, total_stake)
                american_odds = [convert_to_american(o) for o in odds]
                arbitrage_events.append({
                    "event": event_name,
                    "odds": odds,
                    "american_odds": american_odds,
                    "stakes": stakes,
                    "total_stake": total_stake,
                    "profit_margin": round((1 - inv_sum) * 100, 2),  # profit margin in percentage
                    "total_profit": "{:.2f}".format(total_stake * (1 - inv_sum))
                })
        latest_arbitrage_opportunities = arbitrage_events
        time.sleep(60)  # Update every 60 seconds

@app.route("/")
def index():
    """
    Renders a simple HTML page displaying the arbitrage opportunities.
    """
    html = """
    <!doctype html>
    <html>
    <head>
        <title>Sports Betting Arbitrage Opportunities</title>
    </head>
    <body>
        <h1>Arbitrage Opportunities</h1>
        <ul>
        {% for op in opportunities %}
            <li>
                <strong>{{ op.event }}</strong><br>
                Decimal Odds: {{ op.odds }}<br>
                American Odds: {{ op.american_odds }}<br>
                Stakes (for total stake ${{ op.total_stake }}): {{ op.stakes }}<br>
                Profit Margin: {{ op.profit_margin }}%<br>
                Total Profit: ${{ op.total_profit }}
            </li>
        {% else %}
            <li>No arbitrage opportunities available at the moment.</li>
        {% endfor %}
        </ul>
    </body>
    </html>
    """
    return render_template_string(html, opportunities=latest_arbitrage_opportunities)

@app.route("/api/opportunities")
def opportunities():
    """
    API endpoint to return arbitrage opportunities as JSON.
    """
    return jsonify(latest_arbitrage_opportunities)

if __name__ == "__main__":
    # Start the background thread to update odds data
    updater = threading.Thread(target=update_odds_data, daemon=True)
    updater.start()
    # Run the Flask app
    app.run(debug=True)
