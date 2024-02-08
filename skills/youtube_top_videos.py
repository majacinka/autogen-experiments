
"""python script that fetches X number of most viewed videos, 
their titles and total number of views of all times froma 
youtube channel with ID Y

YOUTUBE_API_KEY should be saved as an environment
variable"""

import os  
from googleapiclient.discovery import build  
from googleapiclient.errors import HttpError  
from dotenv import load_dotenv  
  
# Load the API key from the .env file  
load_dotenv()  
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')  
  
if not YOUTUBE_API_KEY:  
    raise ValueError("Missing YOUTUBE_API_KEY in the environment variables.")  
  
# Set up the YouTube API service  
try:  
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)  
except HttpError as e:  
    print(f"An error occurred: {e}")  
    exit(1)  
  
def get_most_viewed_videos(channel_id, topic, max_results=10):  
    try:  
        # Use the search endpoint to find videos about AI within the channel  
        search_response = youtube.search().list(  
            q=topic,  
            channelId=channel_id,  
            part='id',  
            type='video',  
            maxResults=50,  
            order='viewCount'  
        ).execute()  
  
        video_ids = [item['id']['videoId'] for item in search_response['items']]  
  
        # Fetch video details  
        videos_response = youtube.videos().list(id=','.join(video_ids), part='snippet,statistics').execute()  
        videos_info = []  
        for video in videos_response['items']:  
            videos_info.append({  
                'title': video['snippet']['title'],  
                'views': int(video['statistics']['viewCount']),  
                'videoId': video['id']  
            })  
  
        # Sort videos by view count just in case  
        videos_info.sort(key=lambda x: x['views'], reverse=True)  
  
        # Return the top N videos  
        return videos_info[:max_results]  
    except HttpError as e:  
        print(f"An error occurred: {e}")  
        return []  
  
# Channel ID for the specified YouTube channel  
channel_id = 'UCbY9xX3_jW5c2fjlZVBI4cg'  
topic = 'AI'  
  
# Fetch and display the most viewed videos about AI  
most_viewed_videos = get_most_viewed_videos(channel_id, topic)  
for video in most_viewed_videos:  
    print(f"Title: {video['title']}, Views: {video['views']}, Link: https://www.youtube.com/watch?v={video['videoId']}")  