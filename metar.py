import json
import requests

def get_awc_metar(icao_code):
    url = "https://aviationweather.gov/api/data/metar"
    params = {
        'ids': icao_code.upper().strip(),
        'format': 'json'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        if response.status_code == 204 or not response.text.strip():
            return None

        return response.json()

    except json.JSONDecodeError:
        print("JSON Decode Error: Server returned non-JSON text.")
        print("--- START OF RAW RESPONSE ---")
        print(response.text)
        print("--- END OF RAW RESPONSE ---")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {e}")
        return None

def get_metar(airport):
    metar_json = get_awc_metar(airport[0].ident)

    return metar_json
