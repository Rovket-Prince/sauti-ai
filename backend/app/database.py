from supabase import create_client, Client
from app.config import settings

# Initialize the single shared Supabase client instance
supabase_client: Client = create_client(settings.supabase_url, settings.supabase_key)