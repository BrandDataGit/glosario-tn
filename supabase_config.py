import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv

# Attempt to load environment variables from .env file
load_dotenv()

# Function to get environment variable or secret
def get_env_or_secret(key: str) -> str:
    return st.secrets.get(key)    
    #return os.environ.get(key) or st.secrets.get(key)

# Get Supabase URL and Key
url: str = get_env_or_secret("SUPABASE_URL")
key: str = get_env_or_secret("SUPABASE_KEY")

# Check if the URL and key are available
if not url or not key:
    raise ValueError("Supabase URL and Key must be set in environment variables, .env file, or Streamlit secrets")

# Get Supabase URL and Key from environment variables
#url: str = os.environ.get("SUPABASE_URL")
#key: str = os.environ.get("SUPABASE_KEY")

# Check if the URL and key are available
if not url or not key:
    raise ValueError("Supabase URL and Key must be set in environment variables or .env file")

# Create Supabase client
supabase: Client = create_client(url, key)

def check_user_exists(email: str):
    response = supabase.from_('user_profile').select('email').eq('email', email).execute()
    return len(response.data) > 0

def sign_up(email: str, password: str):
    if check_user_exists(email):
        return {"error": "El usuario ya existe"}
    return supabase.auth.sign_up({"email": email, "password": password})

def sign_in(email: str, password: str):
    return supabase.auth.sign_in_with_password({"email": email, "password": password})

def sign_out():
    return supabase.auth.sign_out()

def get_user():
    return supabase.auth.get_user()

def insert_user_profile(email: str):
    try:
        response = supabase.table('user_profile').insert({"email": email}).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Error al insertar en user_profile: {str(e)}")
        return False