import os
import requests

dune_api_key = os.getenv("DUNE_API_KEY")

if not dune_api_key:
    raise ValueError("API key not found in environment variables")

query_ids = [5779439, 5783623, 5785491, 5779698, 5781579, 5783320, 5783967, 5784210, 5784215, 5785149, 5785066, 5792313]  

headers = {"X-DUNE-API-KEY": dune_api_key}

for query_id in query_ids:
    url = f"https://api.dune.com/api/v1/query/{query_id}/execute"
    response = requests.post(url, headers=headers)
    print(f"Query {query_id}: {response.status_code} - {response.text}")