
import tool
import requests
import json

def test_protein_tool():
    print("Testing protein tool...")
    min_protein = 10
    max_protein = 50
    page = 1
    
    url = "https://api.foodoscope.com/recipe2-api/protein/protein-range"
    params = {
        'min': min_protein,
        'max': max_protein,
        'page': page,
        'limit': 10
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer MlouHLGVuKNe2W3wwYDRtA8fg__ZWs5-Hi9DInvIv6Y5nODJ",
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        
        with open("debug_output.txt", "w", encoding="utf-8") as f:
            f.write(f"Status Code: {response.status_code}\n")
            f.write(f"Response Text Prefix: {response.text[:500]}\n") # First 500 chars
            
            try:
                json_response = response.json()
                f.write("JSON Response Full:\n")
                json.dump(json_response, f, indent=2)
            except Exception as e:
                f.write(f"Failed to parse JSON: {e}\n")
            
    except Exception as e:
        with open("debug_output.txt", "w") as f:
            f.write(f"Request failed: {e}\n")

if __name__ == "__main__":
    test_protein_tool()
