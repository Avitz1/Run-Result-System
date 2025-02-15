import requests


class DataHandler:
    BASE_URL = "http://localhost:5000"

    @staticmethod
    def get_tools():
        response = requests.get(f"{DataHandler.BASE_URL}/get_tools")
        if response.status_code == 200:
            return [tool["name"] for tool in response.json()]
        else:
            return []

    @staticmethod
    def get_fields(tool_name):
        response = requests.get(f"{DataHandler.BASE_URL}/get_tool_schema", params={"name": tool_name})
        if response.status_code == 200:
            tool = response.json()
            return tool["schema"]
        else:
            return {}

    @staticmethod
    def get_filtered_data(tool_name, filters, page, last_id):
        params = {
            "tool": tool_name,
            "user": filters.get("user", ""),
            "project": filters.get("project", ""),
            "last_id": last_id,
            "per_page": 4,
        }
        response = requests.get(f"{DataHandler.BASE_URL}/get_filtered_data", params=params)
        if response.status_code == 200:
            data = response.json()
            columns = [key for key in data["data"][0].keys() if key != "id"]
            return data["data"], columns, data["last_id"], (len(data["data"]) + 3) // 4  # Adjust as needed
        else:
            return [], [], None, 0