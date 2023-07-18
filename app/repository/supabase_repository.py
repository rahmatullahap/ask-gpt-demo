import requests

from app.core.config import configs


class SupabaseRepository():
    """Supabase Repository"""
    # def __init__(self):
    #     super().__init__()

    def match_documents(self, params):
        headers = {
            "Authorization": "Bearer " + configs.SUPABASE_KEY,
            "apiKey": configs.SUPABASE_KEY,
            "Content-Type": "application/json"
        }
        func_name = "match_" + configs.SUPABASE_DB
        url = configs.SUPABASE_URL + "/rest/v1/rpc/" + func_name
        response_api = requests.post(url, headers=headers, json=params, timeout=60)
        data = response_api.json()

        return data
