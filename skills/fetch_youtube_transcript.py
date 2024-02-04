
import os
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')

if not API_KEY:
    print("Failed to load YOUTUBE_API_KEY from .env file.")
    exit(1)

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

def search_videos(hours, query, max_res):
    # Calculate the date 10 hours ago in the required format
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    time_threshold = time_threshold.isoformat("T") + "Z"

    try:
        # Search for videos
        search_response = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=50,
            publishedAfter=time_threshold,
            order="viewCount",
            type="video"
        ).execute()

        # Filter top 3 videos
        videos = []
        for item in search_response.get("items", []):
            if len(videos) < max_res:
                videos.append(item)
            else:
                break

        return videos
    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
        return []

def get_transcripts(videos):
    transcripts = []
    for video in videos:
        video_id = video["id"]["videoId"]
        video_title = video["snippet"]["title"]
        try:
            # Fetch the transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = ' '.join([t['text'] for t in transcript])
            transcripts.append((video_title, transcript_text))
        except TranscriptsDisabled:
            print(f"Transcript is disabled for video: {video_title}")
        except Exception as e:
            print(f"An error occurred: {e}")

    return transcripts

def main():
    videos = search_videos()
    if videos:
        transcripts = get_transcripts(videos)
        for title, transcript in transcripts:
            print(f"Title: {title}\nTranscript: {transcript}\n")
    else:
        print("No videos found or an error occurred.")

if __name__ == "__main__":
    main()
