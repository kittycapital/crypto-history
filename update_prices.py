#!/usr/bin/env python3
"""
Daily cryptocurrency data updater
Fetches last 365 days from CoinGecko API and merges with historical CSV files
"""

import os
import csv
import requests
from datetime import datetime, timezone
from pathlib import Path
import time

# CoinGecko coin IDs
COINS = {
    'bitcoin': 'bitcoin',
    'ethereum': 'ethereum',
    'solana': 'solana',
    'xrp': 'ripple',
    'bnb': 'binancecoin'
}

DATA_DIR = Path(__file__).parent / 'data'

def fetch_coingecko_data(coin_id):
    """Fetch last 365 days of price data from CoinGecko"""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': '365',
        'interval': 'daily'
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        prices = []
        for item in data.get('prices', []):
            timestamp_ms = item[0]
            price = item[1]
            dt = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
            date_str = dt.strftime('%Y-%m-%d 00:00:00 UTC')
            prices.append({
                'date': date_str,
                'price': price,
                'date_obj': dt.date()
            })
        
        return prices
    except Exception as e:
        print(f"Error fetching {coin_id}: {e}")
        return []

def load_csv(filepath):
    """Load existing CSV data"""
    data = []
    if not filepath.exists():
        return data
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date_str = row['snapped_at']
                price = float(row['price'])
                # Parse date for comparison
                date_part = date_str.split(' ')[0]
                date_obj = datetime.strptime(date_part, '%Y-%m-%d').date()
                data.append({
                    'date': date_str,
                    'price': price,
                    'market_cap': row.get('market_cap', '0'),
                    'total_volume': row.get('total_volume', '0'),
                    'date_obj': date_obj
                })
            except (ValueError, KeyError) as e:
                continue
    
    return data

def merge_data(existing, new_data):
    """Merge existing data with new API data, keeping latest for duplicates"""
    # Create dict keyed by date
    merged = {}
    
    # Add existing data
    for item in existing:
        merged[item['date_obj']] = {
            'date': item['date'],
            'price': item['price'],
            'market_cap': item.get('market_cap', '0'),
            'total_volume': item.get('total_volume', '0')
        }
    
    # Update/add new data (API data takes precedence for recent dates)
    for item in new_data:
        merged[item['date_obj']] = {
            'date': item['date'],
            'price': item['price'],
            'market_cap': '0',
            'total_volume': '0'
        }
    
    # Sort by date
    sorted_dates = sorted(merged.keys())
    result = [merged[d] for d in sorted_dates]
    
    return result

def save_csv(filepath, data):
    """Save data to CSV"""
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['snapped_at', 'price', 'market_cap', 'total_volume'])
        for item in data:
            writer.writerow([
                item['date'],
                item['price'],
                item['market_cap'],
                item['total_volume']
            ])

def update_coin(coin_name, coin_id):
    """Update a single coin's data"""
    filepath = DATA_DIR / f"{coin_name}.csv"
    
    print(f"Updating {coin_name}...")
    
    # Load existing data
    existing = load_csv(filepath)
    print(f"  Loaded {len(existing)} existing records")
    
    # Fetch new data from API
    new_data = fetch_coingecko_data(coin_id)
    print(f"  Fetched {len(new_data)} records from API")
    
    if not new_data:
        print(f"  Skipping {coin_name} - no new data")
        return
    
    # Merge data
    merged = merge_data(existing, new_data)
    print(f"  Merged total: {len(merged)} records")
    
    # Save updated data
    save_csv(filepath, merged)
    print(f"  Saved to {filepath}")

def main():
    print(f"Starting data update at {datetime.now(timezone.utc).isoformat()}")
    print(f"Data directory: {DATA_DIR}")
    print()
    
    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Update each coin with delay to respect rate limits
    for coin_name, coin_id in COINS.items():
        update_coin(coin_name, coin_id)
        time.sleep(2)  # Respect CoinGecko rate limits
        print()
    
    print("Update complete!")

if __name__ == '__main__':
    main()
