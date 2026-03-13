import os
import sys

# Add the current directory to sys.path so local modules can be found
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
from config import INSTAGRAM_ACCESS_TOKEN

def find_instagram_business_id():
    """
    Finds the Instagram Business ID associated with a Facebook Page linked to the access token.
    """
    print("Searching for connected Facebook Pages...")
    
    # 1. Get Accounts (Facebook Pages)
    pages_url = "https://graph.facebook.com/v19.0/me/accounts"
    params = {"access_token": INSTAGRAM_ACCESS_TOKEN}
    
    try:
        response = requests.get(pages_url, params=params).json()
        pages = response.get("data", [])
        
        if not pages:
            print("No Facebook Pages found associated with this token.")
            return
        
        for page in pages:
            page_name = page.get("name")
            page_id = page.get("id")
            print(f"Checking Page: {page_name} (ID: {page_id})...")
            
            # 2. Get Instagram Business Account for this Page
            ig_url = f"https://graph.facebook.com/v19.0/{page_id}"
            ig_params = {
                "fields": "instagram_business_account",
                "access_token": INSTAGRAM_ACCESS_TOKEN
            }
            ig_response = requests.get(ig_url, params=ig_params).json()
            ig_account = ig_response.get("instagram_business_account")
            
            if ig_account:
                ig_id = ig_account.get("id")
                print("\n" + "="*40)
                print(f"SUCCESS! FOUND INSTAGRAM BUSINESS ID")
                print(f"Page Name: {page_name}")
                print(f"Instagram ID: {ig_id}")
                print("="*40)
                print(f"\nUpdate your config.py with:")
                print(f'INSTAGRAM_BUSINESS_ID = "{ig_id}"')
                return
            
        print("\nNo Instagram Business Account linked to any of your Facebook Pages.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_instagram_business_id()
