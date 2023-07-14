from supabase import Client
from app.schema.ask_schema import DocBody

class SupabaseService():
    """Supabase Service"""
    # def __init__(self):
    #     super().__init__()

    def get_document(self, client: Client, body: DocBody):
        data = client.table('documents_local').select("*").eq("id", body.id).execute()
        print(data.data)
        return {
            "data": data.data,
            "count": len(data.data)
        }
