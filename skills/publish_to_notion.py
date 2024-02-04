import os  
import logging  
from dotenv import load_dotenv  
from notion_client import Client, errors  
  
# Setup basic logging  
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  
  
# Load environment variables  
load_dotenv()  
  
# Retrieve the Notion API secret and page ID from environment variables  
notion_secret = os.getenv("NOTION_SECRET")  
page_id = os.getenv("YOUR_PAGE_ID")  
  
# Validate environment variables  
if not notion_secret or not page_id:  
    logging.error("Missing NOTION_SECRET or YOUR_PAGE_ID in the environment variables.")  
    exit(1)  
  
# Initialize the Notion client  
notion = Client(auth=notion_secret)  
  
def append_text_to_notion_page(page_id, text):  
    """  
    Appends the given text to the specified Notion page.  
  
    Parameters:  
    - page_id (str): The ID of the Notion page to update.  
    - text (str): The text content to append to the Notion page.  
  
    This function makes a network request to the Notion API and appends  
    a paragraph block containing the provided text to the specified page.  
    """  
    try:  
        response = notion.pages.update(  
            page_id=page_id,  
            properties={},  
            children=[  
                {  
                    "object": "block",  
                    "type": "paragraph",  
                    "paragraph": {  
                        "text": [  
                            {  
                                "type": "text",  
                                "text": {  
                                    "content": text,  
                                },  
                            },  
                        ],  
                    },  
                },  
            ],  
        )  
        logging.info(f"Text appended successfully to the Notion page. Page ID: {page_id}")  
    except errors.APIResponseError as e:  
        logging.error(f"APIResponseError occurred: {e}")  
    except Exception as e:  
        logging.error(f"An unexpected error occurred: {e}")  
  