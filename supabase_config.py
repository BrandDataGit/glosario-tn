import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Attempt to load environment variables from .env file
load_dotenv()

# Get Supabase URL and Key from environment variables
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Check if the URL and key are available
if not url or not key:
    raise ValueError("Supabase URL and Key must be set in environment variables or .env file")

# Create Supabase client
supabase: Client = create_client(url, key)

def sign_up(email: str, password: str):
    return supabase.auth.sign_up({"email": email, "password": password})

def sign_in(email: str, password: str):
    return supabase.auth.sign_in_with_password({"email": email, "password": password})

def sign_out():
    return supabase.auth.sign_out()

def get_user():
    return supabase.auth.get_user()