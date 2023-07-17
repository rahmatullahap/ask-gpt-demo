from supabase import Client
from app.schema.api_schema import DocBody
from app.repository.supabase_repository import SupabaseRepository

class SupabaseService():
    """Supabase Service"""
    def __init__(self, supabase_repository: SupabaseRepository):
        self.supabase_repository = supabase_repository
        super().__init__()

    def get_document(self, client: Client, body: DocBody):
        data = self.supabase_repository.select_query(client, "documents_local", ["*"], ["id", body.id])
        print(data.data)
        return {
            "data": data.data,
            "count": len(data.data)
        }
