from fastmcp import FastMCP, Context
import os
import json
import httpx
import difflib
import copy
import time

# Create an MCP server
mcp = FastMCP("bus-finder")

@mcp.tool()
def get_bus_timetable(stop: int) -> dict:
    """Get a bus timetable for a given stop number"""
    try:
        response = httpx.get(
            f"https://itranvias.com/queryitr_v3.php?&dato={stop}&func=0&_={int(time.time() * 1000)}",
            timeout=60
        )
        response.raise_for_status()
        try:
            timetable = response.json()
        except Exception as e:
            timetable = {"error": f"Error parsing JSON: {e}", "raw": response.text}
    except Exception as e:
        timetable = {"error": f"Error during API analysis: {e}"}
    return map_line_numbers_to_friendly_names(timetable)

@mcp.tool()
def get_stop_code_by_location(location: str) -> dict:
    """Return stop code(s) given a location by searching all JSON files in the stops directory. Uses fuzzy matching for similar names."""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    stops_dir = os.path.join(BASE_DIR, "stops")
    results = []
    threshold = 0.7  # Similarity threshold for fuzzy matching
    location_lower = location.lower()
    for filename in os.listdir(stops_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(stops_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                for direction in data.get('directions', []):
                    for stop in direction.get('stops', []):
                        stop_name_lower = stop['name'].lower()
                        # Substring match (legacy behavior)
                        if location_lower in stop_name_lower:
                            results.append({
                                'code': stop['code'],
                                'name': stop['name'],
                                'file': filename,
                                'match_type': 'substring',
                                'similarity': 1.0
                            })
                        else:
                            # Fuzzy match
                            similarity = difflib.SequenceMatcher(None, location_lower, stop_name_lower).ratio()
                            if similarity >= threshold:
                                results.append({
                                    'code': stop['code'],
                                    'name': stop['name'],
                                    'file': filename,
                                    'match_type': 'fuzzy',
                                    'similarity': similarity
                                })
            except Exception as e:
                continue
    if not results:
        return {"error": f"No stop found for location: {location}"}
    # Optionally, sort by similarity (descending)
    results.sort(key=lambda x: x['similarity'], reverse=True)
    return {"matches": results}

def map_line_numbers_to_friendly_names(bus_json):
    line_map = {
        100: "Linea 1",
        1900: "Linea 1A",
        200: "Linea 2",
        800: "Linea 2A",
        300: "Linea 3",
        301: "Linea 3A",
        400: "Linea 4",
        500: "Linea 5",
        600: "Linea 6",
        601: "Linea 6A",
        700: "Linea 7",
        800: "Linea 8",
        1100: "Linea 11",
        1200: "Linea 12",
        1500: "Linea 12A",
        1400: "Linea 14",
        1700: "Linea 17",
        2000: "Linea 20",
        2100: "Linea 21",
        2200: "Linea 22",
        2300: "Linea 23",
        2301: "Linea 23A",
        2400: "Linea 24",
        1800: "Linea BUHO",
        1801: "Linea BUHO A",
        2450: "Linea Campus UDC",
        2451: "Linea Campus UDC"
    }
    # Make a deep copy to avoid mutating the input
    bus_json_copy = copy.deepcopy(bus_json)
    for line in bus_json_copy.get("buses", {}).get("lineas", []):
        linea_num = line.get("linea")
        friendly_name = line_map.get(linea_num, f"Line {linea_num}")
        line["friendly_name"] = friendly_name
    return bus_json_copy

if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run()