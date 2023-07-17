from typing import List
from supabase import Client
import requests

from app.core.config import configs


class SupabaseRepository():
    """Supabase Repository"""
    # def __init__(self):
    #     super().__init__()

    def match_documents(self, func_name: str, params):
        headers = {
            "Authorization": "Bearer " + configs.SUPABASE_KEY,
            "apiKey": configs.SUPABASE_KEY,
            "Content-Type": "application/json"
        }
        url = configs.SUPABASE_URL + "/rest/v1/rpc/" + func_name
        response_api = requests.post(url, headers=headers, json=params, timeout=60)
        data = response_api.json()

        return data

    def select_query(self, client: Client, table: str, columns: List, condition: List):
        col = ','.join(columns)
        data = client.table(table).select(col).eq(
            condition[0], condition[1]).execute()
        return data
