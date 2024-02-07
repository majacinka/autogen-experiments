import os  
from dotenv import load_dotenv  
import requests  
  
def fetch_and_save_photo():  
    # Load environment variables from .env file  
    load_dotenv()  
    # Retrieve the PEXELS_API_KEY from the environment variables  
    pexels_api_key = os.getenv('PEXELS_API_KEY') 
    if not pexels_api_key:  
        print("PEXELS_API_KEY is not set in the .env file.")  
        return  
  
    # Pexels API endpoint for searching photos  
    search_url = "https://api.pexels.com/v1/search"  
  
    # Headers to authenticate the request  
    headers = {  
        "Authorization": pexels_api_key  
    }  
  
    # Parameters for the search query  
    params = {  
        "query": "cat",  # Search query example, users prompt will modify query 
        "per_page": 1,   # Number of results to return per page  example
        "page": 1        # Page number  
    }  
  
    try:  
        # Make the request to Pexels API  
        response = requests.get(search_url, headers=headers, params=params)  
        response.raise_for_status()  # Raise an error for bad responses  
  
        # Extract the first photo from the results  
        photos = response.json().get('photos', [])  
        if not photos:  
            print("No photos found.")  
            return  
  
        first_photo = photos[0]  
        photo_url = first_photo['src']['original']  
  
        # Fetch the photo  
        photo_response = requests.get(photo_url)  
        photo_response.raise_for_status()  
  
        # Save the photo to a file  
        with open("photo.jpg", "wb") as photo_file:  
            photo_file.write(photo_response.content)  
        print("Photo saved successfully.")  
  
    except requests.RequestException as e:  
        print(f"An error occurred: {e}")  
  
if __name__ == "__main__":  
    fetch_and_save_photo()  