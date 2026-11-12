from supabase import create_client, Client

from app.settings import settings

client: Client = create_client(settings.supabase_url, settings.supabase_key)