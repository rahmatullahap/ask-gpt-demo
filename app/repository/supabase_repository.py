from typing import List
from supabase import Client


class SupabaseRepository():
    """Supabase Repository"""
    # def __init__(self):
    #     super().__init__()

    def select_query(self, client: Client, table: str, columns: List, condition: List):
        col = ','.join(columns)
        data = client.table(table).select(col).eq(condition[0], condition[1]).execute()
        return data
