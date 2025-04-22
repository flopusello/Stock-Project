import requests


class APIClient:
    def __init__(self):
        self.name = "API Client"

    def get_request(self, base_url, params: dict, headers=None):
        self.base_url = base_url
        self.params = params
        self.headers = headers
        response = requests.get(base_url, headers=headers, params=params)

        # Request Status Control
        if response.status_code == 200:
            data = response.json()

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            print(response.text)
        return data
